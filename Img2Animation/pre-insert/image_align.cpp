/*************************************************************************
    > File Name: image_align.cpp
    > Author: li_pengju
    > Mail: li_pengju@vobile.cn 
    > Copyright (c) Vobile Inc. All Rights Reserved
    > Created Time: 2017-06-22 10:52:35
 ************************************************************************/

#include<iostream>
#include "opencv2/opencv.hpp"
#define USE_ROI 1
using namespace cv;
using namespace std;

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

int main(int argc, char* argv[])
{
    if(argc < 4)
    {
        cout<< "Align img2 to img1."<<endl;
        cout<< "Usage : "<< argv[0] << "<img1> <img2> <out_name.jpg>"<<endl;
        return -1;
    }
    // Read the images to be aligned
    Mat im1 = imread(argv[1], 1);
    Mat im2 = imread(argv[2], 1);
    if(im1.empty())
    {
        cout<< "Cannot open image ["<<argv[1]<<"]"<<endl;
        return -1;
    }
    if(im2.empty())
    {
        cout<< "Cannot open image ["<<argv[2]<<"]"<<endl;
        return -1;
    }
    
    if(im1.size() != im2.size())
    {
        cout<<"Warning, Image should be of equal sizes!"<<endl;
        cout<<"Resize the "<<argv[2]<<" to the same size of "<<argv[1]<<endl;
        resize(im2, im2, im1.size());
    }
    
    // Convert images to gray scale;
    Mat im1_gray, im2_gray;
    if ( USE_ROI )
    {
        int roi_height = 200;
        int roi_width = 200;
        Mat roiImage1, roiImage2;
        int sy = im2.rows / 4 + 20; //start height of roi
        int sx = im2.cols / 3 + 50; //start width of roi

        cout<<"height="<<roi_height<<"; width="<<roi_width<<" "<<sy<<" "<<sx<<endl;
        if( sy + roi_height > im2.rows || sx + roi_width > im2.cols ){
            cout<< "ERROR: "<<"Region overstep border!"<<endl;
            return -1;
        }
        Rect rect(sx, sy, roi_width, roi_height);
        im1(rect).copyTo(roiImage1);
        im2(rect).copyTo(roiImage2);
        cvtColor(roiImage1, im1_gray, CV_BGR2GRAY);
        cvtColor(roiImage2, im2_gray, CV_BGR2GRAY);

    }
    else
    {
        cvtColor(im1, im1_gray, CV_BGR2GRAY);
        cvtColor(im2, im2_gray, CV_BGR2GRAY);
    }

    // Define the motion model
    /*
     * MOTION_AFFINE
     * MOTION_EUCLIDEAN
     * MOTION_TRANSLATION
     * MOTION_HOMOGRAPHY 
     * */
    const int warp_mode = MOTION_EUCLIDEAN;

    // Set a 2x3 or 3x3 warp matrix depending on the motion model.
    Mat warp_matrix;
    
    // Initialize the matrix to identity
    if ( warp_mode == MOTION_HOMOGRAPHY )
        warp_matrix = Mat::eye(3, 3, CV_32F);
    else
        warp_matrix = Mat::eye(2, 3, CV_32F);

    // Specify the number of iterations.
    int number_of_iterations = 50;
    
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

    // Storage for warped image.
    Mat im2_aligned;

    if (warp_mode != MOTION_HOMOGRAPHY)
        // Use warpAffine for Translation, Euclidean and Affine
        warpAffine(im2, im2_aligned, warp_matrix, im2.size(), INTER_LINEAR + WARP_INVERSE_MAP);
    else
        // Use warpPerspective for Homography
        warpPerspective (im2, im2_aligned, warp_matrix, im2.size(),INTER_LINEAR + WARP_INVERSE_MAP);

    // Show final result
    //imshow("Image 1", im1);
    //imshow("Image 2", im2);
    //imshow("Image 2 Aligned", im2_aligned);
    //waitKey(0);
    imwrite(argv[3], im2_aligned);
    return 0;
}
