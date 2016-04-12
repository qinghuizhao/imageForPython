# -*- coding: utf-8 -*-
'''
Created on 2015.12.21

@author: Zhao Qinghui

功能：实现背景差分，检测人体。

'''
import cv2
from  cv2 import cv
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
filename=r"F:/multi_angle/BaseData/12"
backfilename=r"F:/multi_angle/BK/BaseData"
'''
**************************************************************************
'''

def getFilePicture(folder):
    assert os.path.exists(folder)
    assert os.path.isdir(folder)
    PictureList = os.listdir(folder)
    PictureList = [str(folder)+'/'+item for item in PictureList]
    return PictureList

if __name__ == "__main__":
    for i in range(1,42,1):
       filename=r"F:/multi_angle/BaseData/"
       backfilename=r"F:/multi_angle/BK/BaseData"
       filename=filename+str(i)
       FileNum=os.path.basename(filename)
       print "********************************************************************"
       print "                    "+filename
       print "********************************************************************"
       backName=backfilename+'/'+str(FileNum)+'.png'
       backImage=cv2.imread(backName)
       img_back= cv2.cvtColor(backImage,cv2.COLOR_BGR2GRAY)
       m_picNum=0
       #创建图片的保存地址
       saveName= os.path.dirname(filename)+'/Sub'+str(FileNum)
       if os.path.exists(saveName):
           pass
       else:
           os.mkdir(saveName)
       for imageList in getFilePicture(filename):
           m_picNum=m_picNum+1
           dateImage=cv2.imread(imageList)
           img_gray = cv2.cvtColor(dateImage,cv2.COLOR_BGR2GRAY)
           #将两幅图像相减
           subImage = cv2.absdiff(img_gray,img_back)
           #上面得到的结果是灰度图，将其二值化以便更清楚的观察结果  
           retval, subImage = cv2.threshold(subImage, 50, 255, cv2.THRESH_BINARY);   
           #反色，即对二值图每个像素取反  
           #subImage = cv2.bitwise_not(subImage);
           #膨胀腐蚀
           element = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))  
          # subImage = cv2.dilate(subImage, element)  
         #  subImage = cv2.erode(subImage, element)
           #保存图片       
           saveResult=saveName+'/'+str(m_picNum)+'.png'
           print 'Save '+str(m_picNum)+'.png  !!!'
           cv2.imwrite(saveResult,subImage)
           #显示图像
           cv2.imshow("result",subImage);   
           cv2.waitKey(10)
    print "********************************************************************"
    print "                    "+u"数据全部处理完成   ！！！！！！"
    print "********************************************************************" 
    cv2.destroyAllWindows() 
      
        
    
