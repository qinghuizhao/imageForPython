# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015.12.15

@author: Zhao Qinghui

功能：实现点云数据也映射到二维空间，生成灰度图。

'''
import cv2
from cv2 import cv 
import numpy as np
import math 
import os
global HEIGHT #y,rows归一化后图片的规格，可修改  
global WIDTH  #x,cols
HEIGHT = 100
WIDTH = 100

#可修改文件夹名称
'''
**************************************************************************
'''
PointCloudPath=r"E:/Users/zhao/Desktop/pointCloud90";
'''
**************************************************************************
'''

#遍历文件夹里的所有Txt文件
def getFilePointCloud(folder):
    assert os.path.exists(folder)
    assert os.path.isdir(folder)
    PointCloudList = os.listdir(folder)
    PointCloudList = [str(folder)+'/'+item for item in PointCloudList]
    return PointCloudList

#将点云映射到XOY坐标系   
def PointCloudToImage(PointCloud,nPicture):
    coordNum=0#点云个数
    TemplMax = 0+0.000001#像素值
    TempNum=0#总像素点
    #创建图片
    ImagePix = np.zeros([HEIGHT, WIDTH],np.uint8)
    #E_density =  (PointNum-1)/float(WIDTH*HEIGHT);#每小格的平均密度
    #创建二维列表
    CloudLists = [ [0 for Num_i in range(HEIGHT)]for Num_j in range(WIDTH)]
    m_frame=0
    #读出坐标值
    for line in open(PointCloud):
        x_coord = 0;y_coord = 0#XY坐标值
        m_frame=m_frame+1
        x_coord = int(round(WIDTH*float(line.split(' ')[0]),2))
        y_coord = int(round(HEIGHT*float(line.split(' ')[1]),2))
        if (x_coord >WIDTH-1):
            x_coord = WIDTH-1
        if (x_coord <0):
            x_coord =0
        if (y_coord >HEIGHT-1):
            y_coord = HEIGHT-1
        if (y_coord <0):
            y_coord = 0
        CloudLists[x_coord][y_coord]=CloudLists[x_coord][y_coord]+1
        coordNum=coordNum+1
    #计算像素点
    for j in range(0,HEIGHT):
        for i in range(0,WIDTH):
            if CloudLists[i][j]==0:
                continue
            TemplMax=TemplMax+CloudLists[i][j]
            TempNum=TempNum+1
    TemplMax = TemplMax/TempNum
    #得到灰度值
    for x_i in range(0,HEIGHT):
        for y_j in range(0,WIDTH):
            ImagePix[x_i][y_j]=CloudLists[y_j][x_i]/TemplMax*255
            if ImagePix[x_i][y_j]>255:
                ImagePix[x_i][y_j]=255
    ImageRotate=cv2.flip(ImagePix,0)#图片翻转
    ret, ImagePixGray = cv2.threshold(ImageRotate,0,255,cv2.THRESH_BINARY)
    #ImagePixGray = cv2.dilate(ImagePixGray, None, iterations=2)
    (contours, _) = cv2.findContours(ImagePixGray.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)   
    cv2.drawContours(ImagePixGray,contours,-1,(255,0,255),-1)#填充轮廓
    #cv2.drawContours(ImagePixGray,contours,-1,(255,0,255),1)#光滑轮廓
    #创建图片的保存地址
    saveName= os.path.dirname(PointCloudPath)+'/CloudToImage'
    if os.path.exists(saveName):
       pass
    else:
       os.mkdir(saveName)
    savePicturePath=saveName+'/'+str(nPicture)+'.bmp'
    cv2.imwrite(savePicturePath,ImagePixGray)
    cv2.imshow("",ImagePixGray)
    cv2.waitKey(10)
       
if __name__ == "__main__":
    nPicture=0
    #遍历文件夹下点云数据并按文件文字顺序读取
    for PointCloud in getFilePointCloud(PointCloudPath):
        nPicture=nPicture+1
        PointCloudToImage(PointCloud,nPicture)#点云映射成图片
    cv2.destroyAllWindows()
        
    
