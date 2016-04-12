'''
Created on 2015.12.21

@author: Zhao Qinghui

功能：实现sift特征提取。

'''
import cv2  
import numpy as np
#img = cv2.imread('c:/12.bmp')
img=cv2.imread('E:/Users/zhao/Desktop/OGEI.bmp')
gray=img.copy()
cv2.imshow('origin',img);  
#SIFT  
detector = cv2.SIFT()  
keypoints = detector.detect(gray,None)  
img = cv2.drawKeypoints(gray,keypoints)  
#img = cv2.drawKeypoints(gray,keypoints,flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  
cv2.imwrite('E:/Users/zhao/Desktop/test/test85.bmp',img)
cv2.imshow('test',img);
cv2.waitKey(0)  
cv2.destroyAllWindows() 
