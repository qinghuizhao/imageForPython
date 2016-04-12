'''
Created on 2015.12.21

@author: Zhao Qinghui

���ܣ�ʵ��������⡣

'''
import cv2
import numpy as np
cv2.namedWindow("test")#����һ������
cap=cv2.VideoCapture(0)#��1������ͷ
success, frame = cap.read()#��ȡһ��ͼ��ǰһ������ֵ���Ƿ�ɹ�����һ������ֵ��ͼ����
color = (0,0,0)#�������������ɫ
classfier=cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")#���������
while success:
    success, frame = cap.read()
    size=frame.shape[:2]#��õ�ǰ���ɫͼ��Ĵ�С
    image=np.zeros(size,dtype=np.float16)#����һ���뵱ǰ��ͼ���С��ͬ�ĵĻҶ�ͼ�����
    image = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)#����ǰ��ͼ��ת���ɻҶ�ͼ��
    cv2.equalizeHist(image, image)#�Ҷ�ͼ�����ֱ��ͼ�Ⱦ໯
    #�����������趨��Сͼ��Ĵ�С
    divisor=8
    h, w = size
    minSize=(w/divisor, h/divisor)
    faceRects = classfier.detectMultiScale(image, 1.2, 2, cv2.CASCADE_SCALE_IMAGE,minSize)#�������
    if len(faceRects)>0:#����������鳤�ȴ���0
        for faceRect in faceRects: #��ÿһ�����������ο�
                x, y, w, h = faceRect
                cv2.rectangle(frame, (x, y), (x+w, y+h), color)
    cv2.imshow("test", frame)#��ʾͼ��
    key=cv2.waitKey(10)
    c = chr(key & 255)
    if c in ['q', 'Q', chr(27)]:
        break
cv2.destroyWindow("test")


