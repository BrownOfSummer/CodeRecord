/*************************************************************************
    > File Name: align_image_list.cpp
    > Author: li_pengju
    > Mail: li_pengju@vobile.cn 
    > Copyright (c) Vobile Inc. All Rights Reserved
    > Created Time: 2017-08-24 09:38:21
 ************************************************************************/

#include<iostream>
#include<opencv2/opencv.hpp>

#define USE_ROI 1
using namespace std;
using namespace cv;

Mat GetGradient(Mat src_gray)
{ 
	Mat grad_x, grad_y;
	Mat abs_grad_x, abs_grad_y;

	int scale = 1; 	
	int delta = 0; 
	int ddepth = CV_32FC1; ;
    
    // Calculate the x and y gradients using Sobel operator

	Sobel( src_gray, grad_x, ddepth, 1, 0, 3, scale, delta, BORDER_DEFAULT );
	convertScaleAbs( grad_x, abs_grad_x );

	Sobel( src_gray, grad_y, ddepth, 0, 1, 3, scale, delta, BORDER_DEFAULT );
	convertScaleAbs( grad_y, abs_grad_y );

    // Combine the two gradients
    Mat grad;
	addWeighted( abs_grad_x, 0.5, abs_grad_y, 0.5, 0, grad );

	return grad; 

} 

Mat GetWarpMatrix(Mat im1_gray, Mat im2_gray, const int warp_mode) {

    // Define the motion model
    /*
     * MOTION_AFFINE
     * MOTION_EUCLIDEAN
     * MOTION_TRANSLATION
     * MOTION_HOMOGRAPHY 
     * */
    //const int warp_mode = MOTION_TRANSLATION;

    // Set a 2x3 or 3x3 warp matrix depending on the motion model.
    Mat warp_matrix;
    // Initialize the matrix to identity
    if ( warp_mode == MOTION_HOMOGRAPHY )
        warp_matrix = Mat::eye(3, 3, CV_32F);
    else
        warp_matrix = Mat::eye(2, 3, CV_32F);

    // Specify the number of iterations.
    int number_of_iterations = 100;
    
    // Specify the threshold of the increment
    // in the correlation coefficient between two iterations
    double termination_eps = 1e-10;
    
    // Define termination criteria
    TermCriteria criteria (TermCriteria::COUNT+TermCriteria::EPS, number_of_iterations, termination_eps);

    // Run the ECC algorithm. The results are stored in warp_matrix.
    findTransformECC(
                     GetGradient(im1_gray),
                     GetGradient(im2_gray),
                     warp_matrix,
                     warp_mode,
                     criteria
                 );
    return warp_matrix;
}

int main(int argc, char *argv[])
{
    if( argc != 2 ) {
        cout<<"Usage: "<<argv[0]<<" image.list"<<endl;
        return -1;
    }
    int roi_height = 250;
    int roi_width = 250;
    int roi_sx = 530;
    int roi_sy = 150;
    int count = 0;
    int img_height, img_width;
    Mat im1, im2, roiImage, roiGray;
    vector<Mat> rois;

    string ImgNamesLists[1000];
    char str[200];
    FILE *fImgList = fopen(argv[1], "r");
    if(NULL == fImgList) {
        cout<<"Read file error!"<<endl;
        cout<<argv[1]<<" is not valid !"<<endl;
        return -1;
    }

    while (fgets(str, 200, fImgList) != NULL && count < 1000) {
        memset(str + strlen(str)-1, 0, 1);
        ImgNamesLists[count] = str;
        count ++;
    }
    bool is_first_read = true;
    for(int i = 0; i < count; i ++) {
        im1 = imread(ImgNamesLists[i], 1);
        if( is_first_read ){
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
        if( USE_ROI ) {
            Rect rect(roi_sx, roi_sy, roi_width, roi_height);
            im1(rect).copyTo(roiImage);
            cvtColor(roiImage, roiGray, CV_BGR2GRAY);
            rois.push_back(roiGray.clone());
        }
        else {
            cvtColor(im1, roiGray, CV_BGR2GRAY);
            rois.push_back(roiGray.clone());
        }
        imshow("rois", roiGray);
        imshow("roi-Gradient", GetGradient(roiGray));
        waitKey();
    }

    int template_index = (rois.size() + 1) / 2 - 1;
    cout<<"Select "<<ImgNamesLists[template_index]<<" as template !"<<endl;

    const int warp_mode = MOTION_TRANSLATION;
    // to record the max overlapping area
    //int right = 1280, left = 0, bottom = 720, top = 0;
    int right = img_width, left = 0, bottom = img_height, top = 0;
    // move pixels to align template image
    vector<int> xmove; // + for leftmove, - for rightmove
    vector<int> ymove; // + for upmove, - for downmove
    for(int i = 0; i < rois.size(); i ++) {
        if( i == template_index ) {
            xmove.push_back(0);
            ymove.push_back(0);
            continue;
        }
        Mat warp_matrix = GetWarpMatrix(rois[template_index], rois[i], warp_mode);
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
    cout<<"Area height: "<<area_height<<"; Area width: "<<area_width<<endl;

    // Align and resize
    for(int j = 0; j < 20; j ++) {
        // for show
        for(int i = 0; i < rois.size(); i ++) {
            int startx = left + xmove[i];
            int endx = startx + area_width; //left + xmove[i] + right - left = right + xmove[i]
            int starty = top + ymove[i];
            int endy = starty + area_height; // top + ymove[i] + bottom - top = bottom + ymove[i]
            cout<<"( startx: "<<startx<<", starty: "<<starty<<" )"<<endl;    

            im1 = imread(ImgNamesLists[i], 1);
            Rect rect(startx, starty, area_width, area_height);
            im1(rect).copyTo(roiImage);
            resize(roiImage, im1, Size(640, 360));

            // ori image
            im2 = imread(ImgNamesLists[i], 1);
            resize(im2, im2, Size(640, 360));
            Mat rowshow, colshow;
            hconcat(im2, im1, rowshow);
            //vconcat(im2, im1, colshow);
            imshow("aligned", rowshow);
            waitKey(50);
        }
        cout<<endl;
        waitKey(500);
    }

    return 0;
}
