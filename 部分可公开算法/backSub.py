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
global NORHEIGHT
global NORWIDTH
NORHEIGHT = 90
NORWIDTH = 60
global MaxFile
global MinFile
MaxFile = 42
MinFile = 1
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

#若轮廓数大于1则将其合并
def GetFinalContour(contour,num):
    C = np.array([[[]]])
    x = 1
    for x in contour:
        C = np.concatenate((contour[0],x),axis=0)#将两个数组加到一起
    contour[0] = C
    return contour[0]

def PictureTrueOrFlase(truePicture):
    truePicture1=truePicture.copy()
    m_contours,m_hierarchy = cv2.findContours(truePicture1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    m_ContourNum = len(m_contours)
    if(m_ContourNum>1):
        m_cnt = GetFinalContour(m_contours,m_ContourNum)
    else:
        m_cnt = 0  
    m_M = cv2.moments(m_cnt)
    return m_M['m00']

#此处的x表示cols即320,y表示rows即240
def GetNormalPic(img):
    global NORHEIGHT
    global NORWIDTH 
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
    res = cv2.resize(Person,(NORWIDTH,NORHEIGHT))
    return res

#得到能量图
def OGEIPicture(pictureSavePath):
    pic_i=0
    mH=0
    mW=0
    mC=0
    for GeiList in getFilePicture(pictureSavePath):
        if pic_i==0:
            whImage=cv2.imread(GeiList)
            mH,mW,mC=whImage.shape
        pic_i=pic_i+1
     #创建像素点为255的图片
    emptyGEIImage = np.zeros([mH,mW],np.uint8)
    for GeiList in getFilePicture(pictureSavePath):
        imgGEIList=cv2.imread(GeiList)
        imgGEIList = cv2.cvtColor(imgGEIList,cv2.COLOR_BGR2GRAY)
        ret,imgOGEIList = cv2.threshold(imgGEIList,100,255,0)
        for i in range(0,mH):
            for j in range(0,mW):
                if imgOGEIList[i,j]>0:
                   emptyGEIImage[i,j]=emptyGEIImage[i,j]+imgOGEIList[i,j]/pic_i
    return emptyGEIImage

def OGEI(OGEIpath):
    for m_file in range(MinFile,MaxFile,1):
        OGEIpathName=OGEIpath+str(m_file)
        print "********************************************************************"
        print "                    "+OGEIpathName+u"开始归一化！"
        print "********************************************************************" 

        #创建图片的保存地址
        saveNorName= os.path.dirname(filename)+'/Nor'+str(m_file)
        m_NorPic=0
        '''
        if os.path.exists(saveNorName):
           pass
        else:
           os.mkdir(saveNorName)
        for imgList in getFilePicture(OGEIpathName):
            m_NorPic=m_NorPic+1
            mImage=cv2.imread(imgList)
            mImage = cv2.cvtColor(mImage,cv2.COLOR_BGR2GRAY)
            if PictureTrueOrFlase(mImage)==0:
                continue
            mNorImage=GetNormalPic(mImage)
            saveNorImg=saveNorName+'/'+str(m_NorPic)+'.bmp'
            cv2.imwrite(saveNorImg,mNorImage)
            print u'保存图片'+str(m_NorPic)+'.bmp'+u'  完成！！！'
            cv2.imshow("NorImage",mNorImage)
            cv2.waitKey(10)
        cv2.destroyAllWindows()
    '''
        OGEISaveImg=OGEIPicture(saveNorName)
        saveOGEIName= os.path.dirname(filename)+'/OGEI'
        if os.path.exists(saveOGEIName):
           pass
        else:
           os.mkdir(saveOGEIName)
        OGEIfileName=saveOGEIName+'/'+str(m_file)+'.bmp'           
        cv2.imwrite(OGEIfileName,OGEISaveImg)
    print "********************************************************************"
    print "                    "+u"能量图生成完毕   ！！！！！！"
    print "********************************************************************" 

       
            
            
'''
if __name__ == "__main__":
    FileNum=os.path.basename(filename)
    backName=backfilename+'/'+str(FileNum)+'.png'
    backImage=cv2.imread(backName)
    print backImage.shape
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
        subImage = cv2.dilate(subImage, element)  
        subImage = cv2.erode(subImage, element)
        #保存图片       
        saveResult=saveName+'/'+str(m_picNum)+'.png'
        print 'Save '+str(m_picNum)+'.png  !!!'
        cv2.imwrite(saveResult,subImage)
        #显示图像
        cv2.imshow("result",subImage);   
        cv2.waitKey(10)
    cv2.destroyAllWindows()
'''    
if __name__ == "__main__":
    '''
    for i in range(MinFile,MaxFile,1):
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
    '''
    filename=r"F:/multi_angle/BaseData/"
    OGEIpath=filename+'Sub'
    OGEI(OGEIpath)
    

    
        
    
