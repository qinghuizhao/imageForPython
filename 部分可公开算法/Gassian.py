# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
Created on 2015.12.15

@author: Zhao Qinghui

功能：实现能量图高斯滤波。

'''

#可修改文件夹名称
'''
**************************************************************************
'''
PicturePath=r"E:/Users/zhao/Desktop/test01.bmp";
'''
**************************************************************************
'''
import cv2
from cv2 import cv 
import numpy as np
import math 
import os
import matplotlib.pyplot as plt
global HEIGHT #y,rows归一化后图片的规格，可修改  
global WIDTH  #x,cols
HEIGHT = 100
WIDTH = 100

if __name__ == "__main__":
    img=cv2.imread(PicturePath,0)
    #sigma = 0.3*((ksize-1)*0.5 - 1) + 0.8
    sigma=0
    ksize=int(round(float(((sigma-0.8)/0.3+1)*2+1),2))
    print ksize
    blur=cv2.GaussianBlur(img,(ksize,ksize),1,30)
    plt.subplot(1,2,1)
    plt.imshow(img,'gray')#默认彩色，另一种彩色bgr
    plt.subplot(1,2,2)
    plt.imshow(blur,'gray')
    plt.show() 




    
