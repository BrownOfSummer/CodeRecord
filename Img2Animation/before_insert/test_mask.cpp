/*************************************************************************
    > File Name: test_mask.cpp
    > Author: li_pengju
    > Mail: li_pengju@vobile.cn
    > Copyright (c) Vobile Inc. All Rights Reserved
    > Created Time: 2017-12-15 10:14:00
 ************************************************************************/

#include<iostream>
#include<opencv2/opencv.hpp>
#include "utils.h"
using namespace std;
using namespace cv;

int main(int argc, char *argv[])
{
    // input image after segment
    Mat src = imread(argv[1], 1);
    Mat src_gray, mask;
    cvtColor(src, src_gray, CV_BGR2GRAY);
    src_gray = Erosion(src_gray, 0, 5);
    src_gray = Dilation(src_gray, 0, 5);
    bool flag = generate_mask(src_gray, mask, 255);
    if( !flag ) return -1;
    else {
        imshow("src", src);
        imshow("mask", mask);
        waitKey();
    }
    return 0;
}
