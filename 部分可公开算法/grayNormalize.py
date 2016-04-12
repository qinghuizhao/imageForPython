# -*- coding: utf-8 -*-
'''
Created on 2015.12.10

@author: Zhao Qinghui

功能：实现图片灰度化，二值化，归一化,得到静态特征图，得到动态特征图。

'''
import cv2

import numpy as np
import os
global HEIGHT #y,rows归一化后图片的规格，可修改
global WIDTH  #x,cols
HEIGHT = 90
WIDTH = 60
#可修改文件夹名称
'''
**************************************************************************
'''
#filename=r"E:/Users/zhao/Desktop/ww/Nor41"
filename=r"E:/Users/zhao/Desktop/90_1"
#filename=r"E:/Users/zhao/Desktop/gaitjpg"#需要归一化图片所在文件夹
#filename=r"E:/Users/zhao/Desktop/11"#需要归一化图片所在文件夹
#filename=r"E:/Users/zhao/Desktop/01_00/01_00_a"
#filename=r"E:/Users/zhao/Desktop/depth";
'''
**************************************************************************
'''

#若轮廓数大于1则将其合并
def GetFinalContour(contour,num):
    C = np.array([[[]]])
    x = 1
    for x in contour:
        C = np.concatenate((contour[0],x),axis=0)#将两个数组加到一起
    contour[0] = C
    return contour[0]

#读取图片
def ReadImg(img):
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(img_gray,100,255,0)
    return thresh

#求质心
def GetMeans(thresh):
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    ContourNum = len(contours)
    if(ContourNum>1):
        cnt = GetFinalContour(contours,ContourNum)
    else:
        cnt = contours[0]
    
    M = cv2.moments(cnt)
    #求质心
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return cx,cy,cnt

def PictureTrueOrFlase(truePicture):
    truePicture = ReadImg(truePicture)
    m_contours,m_hierarchy = cv2.findContours(truePicture,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    m_ContourNum = len(m_contours)
    if(m_ContourNum>1):
        m_cnt = GetFinalContour(m_contours,m_ContourNum)
    else:
        m_cnt = m_contours[0]   
    m_M = cv2.moments(m_cnt)
    return m_M['m00']

#此处的x表示cols即320,y表示rows即240
def GetNormalPic(imgm):
    global HEIGHT
    global WIDTH 
    img = ReadImg(imgm)
    img1=img.copy()
    A = img.shape #320*240图片 rows=240 cols=320
    rows = A[0]
    cols = A[1]
    Cx,Cy,cnt = GetMeans(img)#质心cx=278(cols) cy=127(rows)
    #求取最高点和最低点
    topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
    bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
    #人的身高(detrows)
    Height = bottommost[1] - topmost[1]
    New_X = Cx - Height*(float(1))/3 #剪切开始的坐标x
    NewWidth = Height*float(2.0)/3 #剪切的人的宽度
    M = np.float32([[1,0,0],[0,1,0]])#初始化需要移动的矩阵
    if(New_X+NewWidth>cols):#需要左移
        delt_X = cols-(New_X + NewWidth)
        M[0][2] = float(delt_X)
        dst = cv2.warpAffine(img1,M,(cols,rows))
        Person = dst[topmost[1]:bottommost[1],(New_X+delt_X):cols]#y,x 需要剪切的人的范围
    elif(New_X<0):#需要右移
        M[0][2] = float(abs(New_X))
        dst = cv2.warpAffine(img1,M,(cols,rows))
        Person = dst[topmost[1]:bottommost[1],0:NewWidth]
    else:#不需要移动
        dst = img1
        Person = dst[topmost[1]:bottommost[1],New_X:(New_X+NewWidth)]
    res = cv2.resize(Person,(WIDTH,HEIGHT))
    return res

#读取文件夹下所有图片
def getAllImages(folder):
    assert os.path.exists(folder)
    assert os.path.isdir(folder)
    imageList = os.listdir(folder)
    imageList = [str(filename)+'/'+item for item in imageList ]
    return imageList

#读取剪切图片的文件夹
def getCutImages(folder):
    assert os.path.exists(folder)
    assert os.path.isdir(folder)
    pictureList = os.listdir(folder)
    pictureList  = [str(folder)+'/'+item for item in pictureList]
    return pictureList 

#得到最小的静态特征
def minStaticFeature(saveName,m_OGEIimg,saveSingleName):
    min_k=0
    minStaticPath=saveSingleName+'/minSatic.bmp'
    minStatic_RunPath=saveSingleName+'/minSatic_RunOGEI.bmp'
    #创建像素点为255的图片
    minEmptyImage = np.zeros([HEIGHT, WIDTH],np.uint8)
    for i in range(0,HEIGHT):
        for j in range(0,WIDTH):
            minEmptyImage[i,j]=255
    for minImageList in getCutImages(saveName):
       min_k=min_k+1    
       minStaticList0=cv2.imread(minImageList)
       minStaticList=ReadImg(minStaticList0)
       #寻找归一化后图片的公共特征
       for i in range(0,HEIGHT):
            for j in range(0,WIDTH):
                if minStaticList[i,j]>0:
                   minEmptyImage[i,j]=minEmptyImage[i,j]*1#公共特征像素点
                else:
                   minEmptyImage[i,j]=minEmptyImage[i,j]*0#非公共特征像素点
    cv2.imwrite(minStaticPath,minEmptyImage)
    #进去最小公共特征
    for i in range(0,HEIGHT):
            for j in range(0,WIDTH):
                if minEmptyImage[i,j]>0:
                   m_OGEIimg[i,j]=m_OGEIimg[i,j]+minEmptyImage[i,j]/min_k* 4
    cv2.imwrite(minStatic_RunPath,m_OGEIimg)
    print '**********run  and static feature be done success!**********'
 
#得到二值图减去公共特征
def catPicture(saveName,emptyImage,pictureSavePath):
    pic_k=0
    for pictureList in getCutImages(saveName):
        pic_k=pic_k+1
        roiImg=cv2.imread(pictureList)
        for i in range(0,HEIGHT):
            for j in range(0,WIDTH):
                roiImg[i,j]=abs(roiImg[i,j]-emptyImage[i,j])
        pictureFeatureName=pictureSavePath+'/cutFeature'+str(pic_k)+'.bmp'
        cv2.imwrite( pictureFeatureName,roiImg)#保存公共特征图
        print 'Image '+str(pic_k)+' Save!'

#得到能量图
def OGEI(pictureSavePath,saveSingleName):
    pic_i=0
    #创建像素点为255的图片
    emptyGEIImage = np.zeros([HEIGHT, WIDTH],np.uint8)
    for GeiList in getCutImages(pictureSavePath):
        pic_i=pic_i+1
    for GeiList in getCutImages(pictureSavePath):
        imgGEIList=cv2.imread(GeiList)
        imgOGEIList=ReadImg(imgGEIList)
        for i in range(0,HEIGHT):
            for j in range(0,WIDTH):
                if imgOGEIList[i,j]>0:
                   emptyGEIImage[i,j]=emptyGEIImage[i,j]+imgOGEIList[i,j]/pic_i
    saveOGEI=saveSingleName+'/OGEI.bmp'
    cv2.imwrite(saveOGEI,emptyGEIImage)
    print 'Save OGEI  success    !'
    return emptyGEIImage
              
#调用该函数传入图片地址和最后存储图片地址即可得到归一化后的图
if __name__ == "__main__":
    #创建图片的保存地址
    saveName= os.path.dirname(filename)+'/normarlize'
    if os.path.exists(saveName):
       pass
    else:
       os.mkdir(saveName)
    saveSingleName= os.path.dirname(filename)+'/Feature'
    if os.path.exists(saveSingleName):
       pass
    else:
       os.mkdir(saveSingleName)
    k=0
    #创建像素点为255的图片
    emptyImage = np.zeros([HEIGHT, WIDTH],np.uint8)
    #遍历图片
    nkk=0
    for imageList in getAllImages(filename):
       nkk=nkk+1 
    for imageList in getAllImages(filename):
       k=k+1    
       imgList=cv2.imread(imageList)  
       print imageList
       valueTemp,imgList = cv2.threshold(imgList,40,255,0)
       if PictureTrueOrFlase(imgList)==0.0:
           continue
       img = GetNormalPic(imgList)
       valueTemp,img = cv2.threshold(img,100,255,0)
       print  str(k)+' normalize success!';
       saveFileName=saveName+'/'+str(k)+'.bmp'#保存归一化图片路径
       cv2.imshow('img',img)
       cv2.waitKey(10)
       cv2.imwrite(saveFileName,img)#保存归一化后的图片
       #寻找归一化后图片的公共特征
       for i in range(0,HEIGHT):
            for j in range(0,WIDTH):
                if img[i,j]>0:
                   emptyImage[i,j]=emptyImage[i,j]+1 
    for imageList in getAllImages(filename):
        for i in range(0,HEIGHT):
            for j in range(0,WIDTH):
                if emptyImage[i,j]>=nkk*3/4:
                    emptyImage[i,j]=255
                else:
                    emptyImage[i,j]=0
    saveFeatureName=saveSingleName+'/staticFeature.bmp'
    cv2.imwrite(saveFeatureName,emptyImage)#保存公共特征图
    cv2.imshow("staticFeature",emptyImage);
    cv2.waitKey(10)
    cv2.destroyAllWindows()
   
############################减去静态部分############################   
    #动态特征图路径
    pictureSavePath= os.path.dirname(filename)+'/cutpicture'
    if os.path.exists(pictureSavePath):
       pass
    else:
       os.mkdir(pictureSavePath)
    catPicture(saveName,emptyImage,pictureSavePath)#得到动态特征图
    m_OGEIimg=OGEI(pictureSavePath,saveSingleName)#得到能量图
    minStaticFeature(saveName,m_OGEIimg,saveSingleName)#得到最小动态和最小静态图

    

        
                
                
            
        

    
    
    
    
    

