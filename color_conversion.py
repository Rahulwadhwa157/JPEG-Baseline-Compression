# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 12:55:08 2022

@author: HP
"""

import cv2
import numpy as np
import math

def rgbtoycbcr(img):
    n=img.shape[0]
    m=img.shape[1]
    
    print(n,m)
    
    
    image=np.zeros((n,m,3))
    
    
    x=np.array([[0.299,0.587,0.114],[-0.169,-0.331,-0.5],[0.5,-0.419,-0.081]])
    v=np.array([0,128,128])
    
    for i in range(n):
        for j in range(m):
            temp=img[i][j]
            t=np.array([temp[2],temp[1],temp[0]])
            image[i][j]=np.dot(x,t)+v
    
    return image


def ycbcrtorgb(img):
    n=img.shape[0]
    m=img.shape[1]
    
    print(n,m)
    
    
    image=np.zeros((n,m,3))
    
    
   
    x=np.array([[0.299,0.587,0.114],[-0.169,-0.331,-0.5],[0.5,-0.419,-0.081]])
    x=np.linalg.inv(x)
    
    for i in range(n):
        for j in range(m):
            temp=img[i][j]
            t=np.array([temp[0],temp[1]-128,temp[2]-128])
            t1=np.dot(x,t)
            for k in range(3):
                t1[k]=round(t1[k])
                t1[k]=min(t1[k],255)
                t1[k]=max(t1[k],0)
            image[i][j]=np.array([t1[2],t1[1],t1[0]])
            #image[i][j]=t1
    
    return image
            