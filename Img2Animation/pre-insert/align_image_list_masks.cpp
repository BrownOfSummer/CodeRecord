/*************************************************************************
    > File Name: align_image_list_masks.cpp
    > Author: li_pengju
    > Mail: li_pengju@vobile.cn
    > Copyright (c) Vobile Inc. All Rights Reserved
    > Created Time: 2017-12-27 15:31:19
 ************************************************************************/

#include<iostream>
#include<opencv2/opencv.hpp>
#include "utils.h"

using namespace std;
using namespace cv;

void help()
{
    cout<<"\nThis program intend to align a list of images with help of masks or not";
    cout<<"\nIf the mask.list do not provided, with align the image list using whole area.";
    cout<<"\nParas:";
    cout<<"\n\t./bin image.list [mask.list]\n";
}
int main(int argc, char *argv[])
{
    if( argc != 2 && argc !=3 ) {
        help();
        return -1;
    }
    bool use_mask = true;
    string ImgNamesLists[100];
    string MaskNamesLists[100];
    char str[200];
    FILE *fImgList = fopen(argv[1], "r");
    if( fImgList == NULL ) {
        cout<<"Read "<<argv[1]<<" error !"<<endl;
        return -1;
    }
    FILE *fMaskList = NULL;
    if( argc == 2 ) use_mask = false;
    if( use_mask ) {
        fMaskList = fopen(argv[2], "r");
        if( fMaskList == NULL ) {
            cout<<"Read "<<argv[2]<<" error !"<<endl;
            return -1;
        }
    }

    int cnt1 = 0, cnt2 = 0;
    while( fgets(str, 200, fImgList) != NULL && cnt1 < 100) {
        memset(str + strlen(str)-1, 0, 1);
        ImgNamesLists[cnt1] = str;
        cnt1 ++;
    }
    if( use_mask ) {
        while( fgets(str, 200, fMaskList) != NULL && cnt2 < 100) {
            memset(str + strlen(str)-1, 0, 1);
            MaskNamesLists[cnt2] = str;
            cnt2 ++;
        }
        if( cnt1 != cnt2 ) {
            cout<<"image number should equal to masks!"<<endl;
            return -1;
        }
    }
    vector<Mat> image_vec;
    Mat im1, im2, gray, mask;
    int img_width=0, img_height=0;
    bool is_first_read = true;
    for ( int i = 0; i < cnt1; i ++ ) {
        im1 = imread(ImgNamesLists[i], 1);
        if( is_first_read ) {
            img_height = im1.rows;
            img_width = im1.cols;
            is_first_read = false;
        }
        else {
            if( img_height != im1.rows || img_width != im1.cols ) {
                cout<<"ERROR, all image should be same size !"<<endl;
                return -1;
            }
        }

        if( use_mask ) {
            im2 = imread(MaskNamesLists[i], 0);
            if(im2.cols != img_width || im2.rows != img_height) {
                cout<<"ERROR, mask should be same size with input image !"<<endl;
                return -1;
            }

            threshold(im2, mask, 1, 1, THRESH_BINARY);
            mask = Erosion(mask, 0, 5);
            mask = Dilation(mask, 0, 5);
            blurImg(mask, 31, GAUSSION_BLUR);
            cvtColor(im1, gray, CV_BGR2GRAY);
            mask.convertTo(mask, CV_32FC1);
            gray.convertTo(gray, CV_32FC1, 1.0 / 255.0);
            gray = gray.mul(mask);
            gray.convertTo(gray, CV_8UC1, 255);
            image_vec.push_back(gray.clone());
        }
        else {
            cvtColor(im1, gray, CV_BGR2GRAY);
            image_vec.push_back(gray.clone());
        }
        
    }

    /* align image list to one template */

    int template_index = ( image_vec.size() + 1 ) / 2 - 1;
    cout<<"Select "<<ImgNamesLists[template_index]<<" as template !"<<endl;

    const int warp_mode = MOTION_TRANSLATION;
    // to record the max overlapping area
    //int right = 1280, left = 0, bottom = 720, top = 0;
    int right = img_width, left = 0, bottom = img_height, top = 0;
    // move pixels to align template image
    vector<int> xmove; // + for leftmove, - for rightmove
    vector<int> ymove; // + for upmove, - for downmove
    for(int i = 0; i < image_vec.size(); i ++) {
        if( i == template_index ) {
            xmove.push_back(0);
            ymove.push_back(0);
            continue;
        }
        Mat warp_matrix = GetWarpMatrix(image_vec[template_index], image_vec[i], warp_mode);
        float xx = warp_matrix.at<float>(0,2);
        float yy = warp_matrix.at<float>(1,2);
        // Get integer move steps
        int xstep = xx > 0 ? (int)(xx + 0.5) : -(int)(-xx + 0.5);
        int ystep = yy > 0 ? (int)(yy + 0.5) : -(int)(-yy + 0.5);
        //cout<<i<<"<-->"<<template_index<<": xstep = "<<xstep<<"; ystep = "<<ystep<<endl;
        xmove.push_back(xstep);
        ymove.push_back(ystep);

        // Get max overlapping area
        int endx = xstep > 0 ? img_width - xstep : img_width;
        int endy = ystep > 0 ? img_height - ystep : img_height;
        int sx = xstep > 0 ? 0 : -xstep;
        int sy = ystep > 0 ? 0 : -ystep;

        // max overlapping area in template record in left right bottom top
        right = endx < right ? endx : right;
        left = sx > left ? sx : left;
        bottom = endy < bottom ? endy : bottom;
        top = sy > top ? sy : top;
    }
    int area_width = right - left;
    int area_height = bottom - top;
    cout<<"Overlaping area in template: left-up( "<<left<<", "<<top<<" ); right-bottom:( "<<right<<", "<<bottom<<" )"<<endl;
    cout<<"Common area height: "<<area_height<<"; Common area width: "<<area_width<<endl;

    for(int i = 0; i < image_vec.size(); i ++) {
        int startx = left + xmove[i];
        int endx = right + xmove[i];
        int starty = top + ymove[i];
        int endy = bottom + ymove[i];
        cout<<"( startx, starty ): ( "<<startx<<", "<<starty<<" ); ( endx, endy ): ( "<<endx<<", "<<endy<<" )"<<endl;    
    }
    // Align and resize
    for(int j = 0; j < 200; j ++) {
        // for show
        for(int i = 0; i < image_vec.size(); i ++) {
            int startx = left + xmove[i];
            int endx = startx + area_width; //left + xmove[i] + right - left = right + xmove[i]
            int starty = top + ymove[i];
            int endy = starty + area_height; // top + ymove[i] + bottom - top = bottom + ymove[i]
            //cout<<"( startx: "<<startx<<", starty: "<<starty<<" )"<<endl;    

            im1 = imread(ImgNamesLists[i], 1);
            Rect rect(startx, starty, area_width, area_height);
            im1(rect).copyTo(im1);
            resize(im1, im1, Size(640, 360));

            // ori image
            im2 = imread(ImgNamesLists[i], 1);
            resize(im2, im2, Size(640, 360));
            Mat rowshow, colshow;
            hconcat(im2, im1, rowshow);
            //vconcat(im2, im1, colshow);
            imshow("aligned", rowshow);
            waitKey(50);
        }
        char c = waitKey(500);
        if( c == 27 ) break;
    }
    return 0;
}
