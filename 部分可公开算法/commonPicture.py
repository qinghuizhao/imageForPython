# -*- coding: utf-8 -*-
'''
Created on 2016.01.26

@author: Zhao Qinghui

功能：实现图片公共部分。

'''
import cv2
import numpy as np
import os
global HEIGHT #y,rows归一化后图片的规格，可修改
global WIDTH  #x,cols
HEIGHT = 100
WIDTH = 50
'''
**************************************************************************
'''
filename=r"E:/Users/zhao/Desktop/40"
'''
**************************************************************************
'''

#读取文件夹下所有图片
def getAllImages(folder):
    assert os.path.exists(folder)
    assert os.path.isdir(folder)
    imageList = os.listdir(folder)
    imageList = [str(filename)+'/'+item for item in imageList ]
    return imageList

#读取图片
def ReadImg(img):
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(img_gray,100,255,0)
    return thresh

#若轮廓数大于1则将其合并
def GetFinalContour(contour,num):
    C = np.array([[[]]])
    x = 1
    for x in contour:
        C = np.concatenate((contour[0],x),axis=0)#将两个数组加到一起
    contour[0] = C
    return contour[0]


#求质心
def GetMeans(thresh):
    i_y=0
    j_x=0
    count=0
    min_y=100
    max_y=0  
    for j in range(0,WIDTH):
        for i in range(0,HEIGHT):
            if i==91 and imgList[i,j]==255:
                print i,j
            if imgList[j,i]>0:
               i_y=i+i_y
               j_x=j+j_x
               count=count+1
               if min_y>=i:
                   min_y=i
               if max_y<=i:
                   max_y=i
    imgy=i_y/count
    imgx=j_x/count
    imgh=max_y-min_y
    return imgx,imgy,max_y,min_y
      
def GetNormalPic(imgm):
    global HEIGHT
    global WIDTH 
    img = imgm.copy()
    img1=imgm.copy()
    A = img.shape 
    rows = A[0]
    cols = A[1]
    #print A
    Cx,Cy,Cmax,Cmin = GetMeans(img)#质心
    print Cx,Cy,Cmax,Cmin
    #人的身高(detrows)
    Height = Cmax - Cmin
    print Height
    New_X = Cx - Height*(float(1))/3 #剪切开始的坐标x
    NewWidth = Height*float(2.0)/3 #剪切的人的宽度
    M = np.float32([[1,0,0],[0,1,0]])#初始化需要移动的矩阵
   # print New_X,NewWidth
    if(New_X+NewWidth>cols):#需要左移
        delt_X = cols-(New_X + NewWidth)
        M[0][2] = float(delt_X)
        dst = cv2.warpAffine(img1,M,(cols,rows))
        Person = dst[Cmin:Cmax,(New_X+delt_X):cols]#y,x 需要剪切的人的范围
    elif(New_X<0):#需要右移
        M[0][2] = float(abs(New_X))
        dst = cv2.warpAffine(img1,M,(cols,rows))
        Person = dst[Cmin:Cmax,0:NewWidth]
    else:#不需要移动
        dst = img1
        Person = dst[Cmin:Cmax,New_X:(New_X+NewWidth)]
    res = cv2.resize(Person,(WIDTH,HEIGHT))
    return res

if __name__ == "__main__":
    #创建图片的保存地址
    saveName= os.path.dirname(filename)+'/commonPicture'
    if os.path.exists(saveName):
       pass
    else:
       os.mkdir(saveName)
    #创建像素点为255的图片
    emptyImage = np.zeros([HEIGHT, WIDTH],np.uint8)
    for i in range(0,HEIGHT):
        for j in range(0,WIDTH):
            emptyImage[i,j]=0
    #遍历图片
    nkk=0
    for imageList in getAllImages(filename):
       nkk=nkk+1 
    for imageList in getAllImages(filename):
        imgListTemp=cv2.imread(imageList)
        imgList=ReadImg(imgListTemp)
        '''
        #寻找归一化后图片的公共特征
        for i in range(0,HEIGHT):
             for j in range(0,WIDTH):
                 if imgList[i,j]>0:
                    emptyImage[i,j]=emptyImage[i,j]*1 #公共特征像素点
                 else:
                    emptyImage[i,j]=emptyImage[i,j]*0#非公共特征像素点
                 '''
                 #寻找归一化后图片的公共特征
        for i in range(0,HEIGHT):
            for j in range(0,WIDTH):
                if imgList[i,j]>0:
                    emptyImage[i,j]=emptyImage[i,j]+1
    for imageList in getAllImages(filename):
        for i in range(0,HEIGHT):
            for j in range(0,WIDTH):
                if emptyImage[i,j]>=nkk*3/4:
                    emptyImage[i,j]=0
                else:
                    emptyImage[i,j]=255
    '''
    ret, binary = cv2.threshold(emptyImage,127,255,cv2.THRESH_BINARY)  
    contours, hierarchy = cv2.findContours(emptyImage, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
    cv2.drawContours(emptyImage,contours,1,(0,255,0),3)
    cv2.imshow("",emptyImage)
    cv2.waitKey(10)
    '''
    saveNamePicture=saveName+"/commom.bmp"
    cv2.imwrite(saveNamePicture,emptyImage)
    emptyImage= GetNormalPic(emptyImage)
        
        
