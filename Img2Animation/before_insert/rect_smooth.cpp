/*************************************************************************
    > File Name: rect_smooth.cpp
    > Author: li_pengju
    > Mail: li_pengju@vobile.cn
    > Copyright (c) Vobile Inc. All Rights Reserved
    > Created Time: 2017-12-13 21:30:18
 ************************************************************************/

#include<iostream>
#include<opencv2/opencv.hpp>
#include "utils.h"
using namespace std;
using namespace cv;
int main(int argc, char *argv[])
{
    Mat src = imread(argv[1], IMREAD_COLOR);
    if( src.empty() ) {
        cout<<"Read image"<<argv[1]<<" error !\n";
        return -1;
    }
    int x1, x2, y1, y2;
    x1 = src.cols / 5;
    x2 = src.cols - src.cols / 5;
    y1 = src.rows / 5;
    y2 = src.rows - src.rows / 5;
    Mat dst = src.clone();
    
    Rect rect_top(0, 0, src.cols, y1);
    Rect rect_bottom(0, y2, src.cols, src.rows - y2);
    Rect rect_left(0, y1, x1, y2 - y1);
    Rect rect_right(x2, y1, src.cols - x2, y2 - y1);

    rectangle(src, Point(x1, y1), Point(x2, y2), Scalar(0, 0, 255), 2, 8, 0);

    blurImg(dst(rect_top), 31, 1);
    rectangle(dst, Point(0, 0), Point(src.cols, y1), Scalar(0, 255, 0), 2, 8, 0);

    blurImg(dst(rect_bottom), 31, 1);
    rectangle(dst, Point(0, y2), Point(src.cols, src.rows), Scalar(255, 0, 0), 2, 8, 0);

    blurImg(dst(rect_left), 31, 1);
    rectangle(dst, Point(0, y1), Point(x1, y2), Scalar(255, 255, 0), 2, 8, 0);

    blurImg(dst(rect_right), 31, 1);
    rectangle(dst, Point(x2, y1), Point(src.cols, y2), Scalar(0, 255, 255), 2, 8, 0);


    // blur another rects
    int bar = 20;
    Rect rect_top_in(x1 - bar, y1 - bar, x2 - x1 + bar * 2, bar * 2);
    Rect rect_bottom_in(x1 - bar, y2 - bar, x2 - x1 + bar * 2, bar * 2);
    Rect rect_left_in(x1 - bar, y1 + bar, bar * 2, y2 - y1 - bar * 2);
    Rect rect_right_in(x2 - bar, y1 + bar, bar * 2, y2 - y1 - bar * 2);
    blurImg(dst(rect_top_in), 11, 2);
    blurImg(dst(rect_bottom_in), 11, 2);
    blurImg(dst(rect_left_in), 11, 2);
    blurImg(dst(rect_right_in), 11, 2);
    rectangle(dst, Point(x1, y1), Point(x2, y2), Scalar(0, 0, 255), 2, 8, 0);
    imshow("src", src);
    imshow("dst", dst);
    waitKey();
    imwrite("result.jpg", dst);
    return 0;
}

