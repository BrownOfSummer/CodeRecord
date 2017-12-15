/*************************************************************************
    > File Name: utils.h
    > Author: li_pengju
    > Mail: li_pengju@vobile.cn
    > Copyright (c) Vobile Inc. All Rights Reserved
    > Created Time: 2017-12-14 21:35:32
 ************************************************************************/

#include<iostream>
#include<vector>
#include<string>
#include<opencv2/opencv.hpp>
using namespace std;
using namespace cv;

#define HOMO_BLUR 1
#define GAUSSION_BLUR 2
#define MEDIAN_BLUR 3
#define BILATERA_BULR 4
bool generate_mask(Mat seg_src, Mat &mask, unsigned char mask_value);
Mat Erosion( Mat src, int erosion_elem, int erosion_size );
Mat Dilation( Mat src, int dilation_elem, int dilation_size);
int blurImg(Mat img, int kernel_size, int blur_type);
