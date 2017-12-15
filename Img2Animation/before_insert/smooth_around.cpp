/*************************************************************************
    > File Name: smooth_around.cpp
    > Author: li_pengju
    > Mail: li_pengju@vobile.cn
    > Copyright (c) Vobile Inc. All Rights Reserved
    > Created Time: 2017-12-14 22:07:15
 ************************************************************************/

#include<iostream>
#include<vector>
#include<opencv2/opencv.hpp>
#include "utils.h"
using namespace std;
using namespace cv;
int main(int argc, char *argv[])
{
    if( argc !=3 ) {
        cout<<"ERROR, inputs must be ori-img and mask-img. \n";
        return -1;
    }
    Mat src, src_smooth, mask, dst;
    src = imread(argv[1], 1);
    if( src.empty() ) {
        cout<<"ERROR, read "<<argv[1]<<" failed.\n";
        return -1;
    }
    mask = imread(argv[2], 0);
    if( mask.empty() ) {
        cout<<"ERROR, read "<<argv[2]<<" failed. \n";
        return -1;
    }
    threshold( mask, mask, 1, 1, THRESH_BINARY );
    mask.convertTo( mask, CV_32FC1 );
    blurImg(mask, 31, GAUSSION_BLUR);
    Mat inv_mask = 1.0 - mask;

    src.copyTo(src_smooth);
    src.convertTo(src, CV_32FC3, 1.0 / 255);
    src_smooth.convertTo(src_smooth, CV_32FC3, 1.0 / 255);
    //blurImg(src_smooth, 31, GAUSSION_BLUR);
    blurImg(src_smooth, 31, HOMO_BLUR);
    
    vector<Mat> chs(3);
    vector<Mat> chs_smooth(3);
    split(src, chs);
    split(src_smooth, chs_smooth);

    chs[0] = chs[0].mul(mask) + chs_smooth[0].mul(inv_mask);
    chs[1] = chs[1].mul(mask) + chs_smooth[1].mul(inv_mask);
    chs[2] = chs[2].mul(mask) + chs_smooth[2].mul(inv_mask);

    merge(chs, dst);
    imshow("src", src);
    imshow("mask", mask);
    imshow("inv_mask", inv_mask);
    imshow("dst", dst);
    waitKey();
    dst.convertTo(dst, CV_8UC3, 255);
    imwrite("around_smooth.jpg", dst);
    return 0;
}
