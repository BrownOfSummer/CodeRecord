/*************************************************************************
    > File Name: utils.cpp
    > Author: li_pengju
    > Mail: li_pengju@vobile.cn
    > Copyright (c) Vobile Inc. All Rights Reserved
    > Created Time: 2017-12-14 21:23:47
 ************************************************************************/

#include<iostream>
#include<vector>
#include<string>
#include<opencv2/opencv.hpp>
#include "utils.h"
using namespace std;
using namespace cv;

/*
 * Paras:
 *      seg_src: An image after seg, background is 0, foreground is non-zero, 1 channels;
 *      mask: An empty Mat or same with seg
 *      mask_value: the mask is binary, with 0 and mask_value
 *      */
bool generate_mask(Mat seg_src, Mat &mask, unsigned char mask_value)
{
    CV_Assert(seg_src.depth() == CV_8U);
    if( seg_src.channels() != 1 ) return false;
    //if( mask.channels() != 1 ) return false;
    int nCols = seg_src.cols;
    int nRows = seg_src.rows;
    if( mask.empty() )
        seg_src.copyTo(mask);
    if( seg_src.size() != mask.size() ) return false;
    Mat mask1(mask.size(), CV_8UC1, Scalar(0));
    Mat mask2(mask.size(), CV_8UC1, Scalar(0));
    //mask.setTo(Scalar(0));
    
    /*  deal with horiztal area */
    for(int y = 0; y < nRows; ++y) {
        int start_index = nCols + 1;
        int end_index = 0;
        for(int x = 0; x < nCols; ++x) {
            if(seg_src.at<uchar>(y, x) > 0) {
                start_index = x;
                break;
            }
        }
        if( start_index > nCols - 1 )
            continue;
        for(int x = nCols - 1; x > start_index; --x) {
            if(seg_src.at<uchar>(y, x) > 0) {
                end_index = x;
                break;
            }
        }
        if( end_index - start_index < 1)
            continue;
        else {
            for(int x = start_index; x <= end_index; x++)
                mask1.at<uchar>(y, x) = 1;
        }

    }

    /* deal with vertical area */
    for(int x = 0; x < nCols; ++x) {
        int start_index = nRows + 1;
        int end_index = 0;
        for(int y = 0; y < nRows; ++y) {
            if( seg_src.at<uchar>(y, x) > 0 ) {
                start_index = y;
                break;
            }
        }
        if(start_index > nRows - 1)
            continue;
        for(int y = nRows - 1; y > start_index; --y) {
            if( seg_src.at<uchar>(y, x) > 0 ) {
                end_index = y;
                break;
            }
        }
        if( end_index - start_index < 1 )
            continue;
        else {
            for( int y = start_index; y <= end_index; ++y )
                mask2.at<uchar>(y, x) = 1;
        }
    }
    mask=(mask1 & mask2) * mask_value;
    cout<<"Generate done !\n";
    return true;
}
/*
 * Morphological operation: Erosion
 * Paras: src mat
 *        erosion_elem: type of enrosion, 1 0f 3;
 *        erosion_size*/
Mat Erosion( Mat src, int erosion_elem, int erosion_size )
{
  int erosion_type;
  Mat erosion_dst;
  if( erosion_elem == 0 ){ erosion_type = MORPH_RECT; }
  else if( erosion_elem == 1 ){ erosion_type = MORPH_CROSS; }
  else if( erosion_elem == 2) { erosion_type = MORPH_ELLIPSE; }

  Mat element = getStructuringElement( erosion_type,
                                       Size( 2*erosion_size + 1, 2*erosion_size+1 ),
                                       Point( erosion_size, erosion_size ) );

  /// Apply the erosion operation
  erode( src, erosion_dst, element );
  //imshow( "Erosion Demo", erosion_dst );
  return erosion_dst;
}

/*
 * Morphological operation: Dilation
 * Paras: src mat
 *        dilation_elem: type of dilation, 1 of 3
 *        dilation_size
 */
Mat Dilation( Mat src, int dilation_elem, int dilation_size)
{
  int dilation_type;
  Mat dilation_dst;
  if( dilation_elem == 0 ){ dilation_type = MORPH_RECT; }
  else if( dilation_elem == 1 ){ dilation_type = MORPH_CROSS; }
  else if( dilation_elem == 2) { dilation_type = MORPH_ELLIPSE; }

  Mat element = getStructuringElement( dilation_type,
                                       Size( 2*dilation_size + 1, 2*dilation_size+1 ),
                                       Point( dilation_size, dilation_size ) );
  /// Apply the dilation operation
  dilate( src, dilation_dst, element );
  //imshow( "Dilation Demo", dilation_dst );
  return dilation_dst;
}

/*
 * Do blur in different methods
 * Paras:
 *      kernel_size: odd num, kernel size
 *      blur_type: select for Homogeneous, GaussianBlur, or Median
 *      */
int blurImg(Mat img, int kernel_size, int blur_type)
{
    switch(blur_type){
        case 1:
            cout<<"Do Homogeneous Blur.\n";
            blur( img, img, Size(kernel_size, kernel_size), Point(-1, -1) );
            break;
        case 2:
            cout<<"Do Gaussion Blur.\n";
            GaussianBlur(img, img, Size(kernel_size, kernel_size), 0, 0);
            break;
        case 3:
            cout<<"Do Median Blur.\n";
            medianBlur(img, img, kernel_size);
            break;
        case 4:
            cout<<"Do bilateralFilter Blur. \n";
            bilateralFilter(img, img, kernel_size, kernel_size*2, kernel_size/2 );
        default:
            cout<<"Do Gaussion Blur for default.\n";
            GaussianBlur(img, img, Size(kernel_size, kernel_size), 0, 0);
            return -1;
    }
    return 0;
}
