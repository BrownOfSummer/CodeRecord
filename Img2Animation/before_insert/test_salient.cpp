
#include<iostream>
#include<opencv2/opencv.hpp>
using namespace std;
using namespace cv;
Mat SalientRegionDetectionBasedonLC(Mat &src);
Mat SalientRegionDetectionBasedonAC(Mat &src,int MinR2, int MaxR2,int Scale);
Mat SalientRegionDetectionBasedonFT(Mat &src);
int main(int argc, char *argv[])
{
    Mat src = imread(argv[1], 1);
    imshow("src", src);
    waitKey();
    Mat satLC = SalientRegionDetectionBasedonLC(src);
    Mat satFT = SalientRegionDetectionBasedonFT(src);
    Mat satAC = SalientRegionDetectionBasedonAC(src, src.rows/8, src.rows/2, 3);
    imshow("LC", satLC);
    imshow("FT", satFT);
    imshow("AC", satAC);
    waitKey();
    return 0;
}

Mat SalientRegionDetectionBasedonLC(Mat &src){  
    int HistGram[256]={0};  
    int row=src.rows,col=src.cols;  
    int gray[row][col];  
    //int Sal_org[row][col];  
    int val;  
    Mat Sal=Mat::zeros(src.size(),CV_8UC1 );  
    Point3_<uchar>* p;  
    for (int i=0;i<row;i++){  
        for (int j=0;j<col;j++){  
            p=src.ptr<Point3_<uchar> > (i,j);  
            val=(p->x + (p->y) *2 + p->z)/4;  
            HistGram[val]++;  
            gray[i][j]=val;  
        }  
    }  
  
    int Dist[256];  
    int Y,X;
    int max_gray=0;  
    int min_gray=1<<28;  
    for (Y = 0; Y < 256; Y++)  
    {  
        val = 0;  
        for (X = 0; X < 256; X++)   
            val += abs(Y - X) * HistGram[X];                //    论文公式（9），灰度的距离只有绝对值，这里其实可以优化速度，但计算量不大，没必要了  
        Dist[Y] = val;  
        max_gray=max(max_gray,val);  
        min_gray=min(min_gray,val);  
    }  
  
      
    for (Y = 0; Y < row; Y++)  
    {  
        for (X = 0; X < col; X++)  
        {  
            Sal.at<uchar>(Y,X) = (Dist[gray[Y][X]] - min_gray)*255/(max_gray - min_gray);        //    计算全图每个像素的显著性  
            //Sal.at<uchar>(Y,X) = (Dist[gray[Y][X]])*255/(max_gray);        //    计算全图每个像素的显著性  
          
        }  
    }  
    //imshow("sal",Sal);  
    //waitKey(0);  
    return Sal;
}  

Mat SalientRegionDetectionBasedonAC(Mat &src,int MinR2, int MaxR2,int Scale){
	Mat Lab;
	cvtColor(src, Lab, CV_BGR2Lab); 

	int row=src.rows,col=src.cols;
	int Sal_org[row][col];
	memset(Sal_org,0,sizeof(Sal_org));
	
	Mat Sal=Mat::zeros(src.size(),CV_8UC1 );

	Point3_<uchar>* p;
	Point3_<uchar>* p1;
	int val;
	Mat filter;

	int max_v=0;
	int min_v=1<<28;
	for (int k=0;k<Scale;k++){
		int len=(MaxR2 - MinR2) * k / (Scale - 1) + MinR2;
		blur(Lab, filter, Size(len,len ));
		for (int i=0;i<row;i++){
			for (int j=0;j<col;j++){
				p=Lab.ptr<Point3_<uchar> > (i,j);
				p1=filter.ptr<Point3_<uchar> > (i,j);
				//cout<<(p->x - p1->x)*(p->x - p1->x)+ (p->y - p1->y)*(p->y-p1->y) + (p->z - p1->z)*(p->z - p1->z) <<" ";
				
				val=sqrt( (p->x - p1->x)*(p->x - p1->x)+ (p->y - p1->y)*(p->y-p1->y) + (p->z - p1->z)*(p->z - p1->z) );
				Sal_org[i][j]+=val;
				if(k==Scale-1){
					max_v=max(max_v,Sal_org[i][j]);
					min_v=min(min_v,Sal_org[i][j]);
				}
			}
		}
	}
	
	cout<<max_v<<" "<<min_v<<endl;
	int X,Y;
    for (Y = 0; Y < row; Y++)
    {
        for (X = 0; X < col; X++)
        {
            Sal.at<uchar>(Y,X) = (Sal_org[Y][X] - min_v)*255/(max_v - min_v);        //    计算全图每个像素的显著性
        	//Sal.at<uchar>(Y,X) = (Dist[gray[Y][X]])*255/(max_gray);        //    计算全图每个像素的显著性
        }
    }
    //imshow("sal",Sal);
    //waitKey(0);
    return Sal;
}

Mat SalientRegionDetectionBasedonFT(Mat &src){
	Mat Lab;
	cvtColor(src, Lab, CV_BGR2Lab); 

	int row=src.rows,col=src.cols;

	int Sal_org[row][col];
	memset(Sal_org,0,sizeof(Sal_org));
	
	Point3_<uchar>* p;

	int MeanL=0,Meana=0,Meanb=0;
	for (int i=0;i<row;i++){
		for (int j=0;j<col;j++){
			p=Lab.ptr<Point3_<uchar> > (i,j);
			MeanL+=p->x;
			Meana+=p->y;
			Meanb+=p->z;
		}
	}
	MeanL/=(row*col);
	Meana/=(row*col);
	Meanb/=(row*col);

	GaussianBlur(Lab,Lab,Size(3,3),0,0);

	Mat Sal=Mat::zeros(src.size(),CV_8UC1 );

	int val;

	int max_v=0;
	int min_v=1<<28;

	for (int i=0;i<row;i++){
		for (int j=0;j<col;j++){
			p=Lab.ptr<Point3_<uchar> > (i,j);
			val=sqrt( (MeanL - p->x)*(MeanL - p->x)+ (p->y - Meana)*(p->y-Meana) + (p->z - Meanb)*(p->z - Meanb) );
			Sal_org[i][j]=val;
			max_v=max(max_v,val);
			min_v=min(min_v,val);		
		}
	}
	
	cout<<max_v<<" "<<min_v<<endl;
	int X,Y;
    for (Y = 0; Y < row; Y++)
    {
        for (X = 0; X < col; X++)
        {
            Sal.at<uchar>(Y,X) = (Sal_org[Y][X] - min_v)*255/(max_v - min_v);        //    计算全图每个像素的显著性
        	//Sal.at<uchar>(Y,X) = (Dist[gray[Y][X]])*255/(max_gray);        //    计算全图每个像素的显著性
        }
    }
    //imshow("sal",Sal);
    //waitKey(0);
    return Sal;
}
