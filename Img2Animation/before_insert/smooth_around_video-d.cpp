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

#define SKIP_FRAMES 0
#define SKIP_START_SEC 0
#define MOVE_SPLIT_AT_SEC1 0
#define MOVE_SPLIT_AT_SEC2 105
#define MOVE_SPLIT_AT_SEC3 121.5
#define MOVE_SPLIT_AT_SEC4 235 
using namespace std;
using namespace cv;
void help()
{
    cout<<"\nThis Program demostrated smooth frame background with help of mask image.";
    cout<<"\nThe mask image must be a binary image with black background.";
    cout<<"\nCall";
    cout<<"\n\t./smooth_around_video mask.jpg video.mp4 [Y | y | N | n]\n";
}
int main(int argc, char *argv[])
{
    if( argc != 7 ) {
        cout<<"ERROR, Inputs Error. \n";
        help();
        return -1;
    }

    for(int i = 0; i < 7; i ++) {
        cout<<argv[i]<<endl;
    }
    const bool askOutputOrNot = argv[6][0] =='Y' || argv[6][0] == 'y';  // If false it will use the inputs codec type
    Mat frame, mask;

    mask = imread(argv[1], 0);
    if( mask.empty() ) {
        cout<<"ERROR, read "<<argv[1]<<" failed. \n";
        help();
        return -1;
    }
    threshold( mask, mask, 1, 1, THRESH_BINARY );
    mask.convertTo( mask, CV_32FC1 );
    blurImg(mask, 31, GAUSSION_BLUR);
    Mat inv_mask = 1.0 - mask;

    Mat mask2, mask3, mask4, inv_mask2, inv_mask3, inv_mask4;
    mask2 = imread(argv[2], 0);
    mask3 = imread(argv[3], 0);
    mask4 = imread(argv[4], 0);
    threshold( mask2, mask2, 1, 1, THRESH_BINARY );
    threshold( mask3, mask3, 1, 1, THRESH_BINARY );
    threshold( mask4, mask4, 1, 1, THRESH_BINARY );
    mask2.convertTo(mask2, CV_32FC1);
    mask3.convertTo(mask3, CV_32FC1);
    mask4.convertTo(mask4, CV_32FC1);
    blurImg(mask2, 31, GAUSSION_BLUR);
    blurImg(mask3, 31, GAUSSION_BLUR);
    blurImg(mask4, 31, GAUSSION_BLUR);
    inv_mask2 = 1.0 - mask2;
    inv_mask3 = 1.0 - mask3;
    inv_mask4 = 1.0 - mask4;


    bool change_to_mask2 = true;
    bool change_to_mask3 = true;
    bool change_to_mask4 = true;

    VideoCapture cap(argv[5], CAP_FFMPEG);
    if( !cap.isOpened() ) {
        cout<<"ERROR: Open video failed !\n";
        help();
        return -1;
    }
    int video_width, video_height, total_frames;
    double frame_rate, video_length_sec;
    GetVideoInfo(cap, video_height, video_width, total_frames, frame_rate);
    video_length_sec = total_frames / frame_rate;
    int move_split2 = (int)(MOVE_SPLIT_AT_SEC2 * frame_rate);
    int move_split3 = (int)(MOVE_SPLIT_AT_SEC3 * frame_rate);
    int move_split4 = (int)(MOVE_SPLIT_AT_SEC4 * frame_rate);
    cout<<"Video Size: [ "<<video_width<<"x"<<video_height<<" ]\n";
    cout<<"Video length(s): "<<video_length_sec<<"s; "<<total_frames<<" frames\n";
    cout<<"Frame rate: "<<frame_rate<<endl;
    int ex = static_cast<int>(cap.get(CV_CAP_PROP_FOURCC));
    char EXT[] = { (char)(ex & 0XFF), (char)((ex & 0XFF00) >> 8),(char)((ex & 0XFF0000) >> 16),(char)((ex & 0XFF000000) >> 24), 0};
    cout<<"Video Codec: "<<EXT<<endl;
    if(video_width != mask.cols || video_height != mask.rows) {
        cout<<"Error: mask and video must be same size !\n";
        help();
        return -1;
    }

    VideoWriter outputVideo;
    if( askOutputOrNot ) {
        const string source = argv[5];
        string::size_type pAt = source.find_last_of('.');
        const string output_video_name = source.substr(0, pAt) + "-smoothed" + ".mp4";
        outputVideo.open(output_video_name, ex, frame_rate, Size(video_width, video_height), true);
        if( !outputVideo.isOpened() ) {
            cout<<"Failed to open outputVideo !\n";
            return -1;
        }
        cout<<"Output Video file: "<<output_video_name<<endl;
    }

    int skips = 0;
    int skip_start_frames = (int)(SKIP_START_SEC * frame_rate);
    Mat frame_smooth;
    vector<Mat> chs(3);
    vector<Mat> chs_smooth(3);
    for(int i = 0; i< total_frames; i ++)
    {
        if( i < skip_start_frames ) {
            cap.grab();
            continue;
        }
        if( skips < SKIP_FRAMES ) {
            skips ++;
            cap.grab();
            continue;
        }
        skips = 0;
        if( i > move_split2 && change_to_mask2 ) {
            change_to_mask2 = false;
            mask2.copyTo(mask);
            inv_mask2.copyTo(inv_mask);
        }
        else if( i > move_split3 && change_to_mask3 ) {
            change_to_mask3 = false;
            mask3.copyTo(mask);
            inv_mask3.copyTo(inv_mask);
        }
        else if( i > move_split4 && change_to_mask4 ) {
            change_to_mask4 = false;
            mask4.copyTo(mask);
            inv_mask4.copyTo(inv_mask);
        }  //
        cap.grab();
        cap.retrieve(frame);

        frame.convertTo(frame_smooth, CV_32FC3, 1.0 / 255.0);
        frame.convertTo(frame, CV_32FC3, 1.0 / 255.0);
        blurImg( frame_smooth, 31, HOMO_BLUR );
        split(frame, chs);
        split(frame_smooth, chs_smooth);
        chs[0] = chs[0].mul(mask) + chs_smooth[0].mul(inv_mask);
        chs[1] = chs[1].mul(mask) + chs_smooth[1].mul(inv_mask);
        chs[2] = chs[2].mul(mask) + chs_smooth[2].mul(inv_mask);
        merge(chs, frame);
        frame.convertTo(frame, CV_8UC3, 255);
        if( askOutputOrNot )
            outputVideo.write(frame);
        else {
            imshow("video", frame);
            char key = (char)waitKey(30);
            if(key == 27) break;
        }
    }

    return 0;
}
