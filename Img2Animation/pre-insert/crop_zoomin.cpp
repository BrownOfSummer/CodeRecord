/*************************************************************************
    > File Name: crop_zoomin.cpp
    > Author: li_pengju
    > Mail: li_pengju@vobile.cn
    > Copyright (c) Vobile Inc. All Rights Reserved
    > Created Time: 2018-02-09 16:18:00
 ************************************************************************/

#include<iostream>
#include<opencv2/opencv.hpp>
using namespace std;
using namespace cv;

void help()
{
    //
}

int main(int argc, char *argv[])
{
    if ( argc != 6 ) {
        help();
        return -1;
    }
    Mat src, crop, zoomin;
    src = imread(argv[1]);
    int startx = atoi(argv[2]);
    int starty = atoi(argv[3]);
    int width = atoi(argv[4]);
    int height = atoi(argv[5]);
    cout<<startx<<", "<<starty<<", "<<width<<", "<<height<<endl;
    if( startx + width > src.cols ) {
        cout<<"sx and width error!"<<endl;
        return -1;
    }
    if( starty + height > src.rows ) {
        cout<<"sy and height error!"<<endl;
        return -1;
    }
    Rect rect( startx, starty, width, height );
    src(rect).copyTo(crop);
    resize( crop, crop, src.size() );
    /*zoomin*/
    int sx = int(src.cols * 0.2 / 2);
    int sy = int(src.rows * 0.1 / 2);
    Rect rect2(sx, sy, int(src.cols * 0.8), int(src.rows * 0.8));
    cout<<rect2<<endl;
    crop(rect2).copyTo(zoomin);
    resize(zoomin, zoomin, src.size());
    imshow("src", src);
    imshow("crop", crop);
    imshow("zoomin", zoomin);
    waitKey();

    vector<int> compression_params;
    compression_params.push_back(CV_IMWRITE_JPEG_QUALITY);
    compression_params.push_back(20);
    imwrite("crop.jpg",crop, compression_params);
    imwrite("zoomin.jpg",zoomin, compression_params);
    return 0;
}
