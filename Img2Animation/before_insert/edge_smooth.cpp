/*************************************************************************
    > File Name: edge_smooth.cpp
    > Author: li_pengju
    > Mail: li_pengju@vobile.cn
    > Copyright (c) Vobile Inc. All Rights Reserved
    > Created Time: 2017-12-14 15:19:13
 ************************************************************************/

#include<iostream>
#include<vector>
#include<string>
#include<opencv2/opencv.hpp>
#include "utils.h"
using namespace std;
using namespace cv;
int main(int argc, char *argv[])
{
    Mat src, seg_src, mask, seg_img, dst;
    src = imread(argv[1], 1);
    seg_src = imread(argv[2], 1);
    seg_src.copyTo(mask);
    cvtColor(mask, mask, CV_BGR2GRAY);
    cvtColor(seg_src, seg_img, CV_BGR2GRAY);
    seg_img = Erosion(seg_img, 0, 5);
    seg_img = Dilation(seg_img, 0, 5);
    bool flag = generate_mask(seg_img, mask, 255);
    if( !flag ) return -1;
    else imwrite("mask.jpg", mask);
    //threshold(mask, mask, 1, 255, THRESH_BINARY_INV);
    //threshold(mask, mask, 0, 255, CV_THRESH_BINARY | CV_THRESH_OTSU);
    //floodFill(mask, cv::Point(src.cols/2, src.rows/2), Scalar(255));
    Mat mul_mask;
    threshold(mask, mul_mask, 1, 1, THRESH_BINARY);
    mul_mask.convertTo(mul_mask, CV_32FC1);
    GaussianBlur( mul_mask, mul_mask, Size(21, 21), 11.0 );
    imshow("seg_src", seg_src);
    imshow("mask", mask);
    imshow("mul_mask", mul_mask);
    waitKey();
    vector<Mat> chs(3);
    src.convertTo(src, CV_32FC3, 1.0 / 255);
    split(src, chs);
    chs[0] = chs[0].mul(mul_mask);
    chs[1] = chs[1].mul(mul_mask);
    chs[2] = chs[2].mul(mul_mask);
    merge(chs, dst);
    imshow("dst", dst);
    waitKey();
    return 0;
}
