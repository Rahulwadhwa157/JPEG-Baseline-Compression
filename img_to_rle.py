# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 11:37:59 2022

@author: HP
"""

import cv2
import numpy as np
import math

# import zigzag functions
from zigzag import *

def get_category(x):
    x=abs(x)
    ans=-1
    for i in range(31,-1,-1):
       
        if ((x>>i)&1)==1:
            ans=i
            break
    return ans+1


def bitstream(arr,prev):
    n=arr.shape[0]
    
    s=""
    x=arr[0]-prev
    s=s+str(x)+" "
    a=[]
    a.append(x)
    
    cnt=0
    
    for i in range(1,n):
        if(arr[i]!=0):
            a.append((cnt,get_category(abs(arr[i])),arr[i]))
            s=s+str(cnt)+" "+str(get_category(abs(arr[i])))+" "+str(arr[i])+" "
            cnt=0
        else:
            cnt=cnt+1
    
    a.append((0,0))
    s=s+str(0)+" "+str(0)
    a=np.array(a,dtype='object')
    return a,s

'''
arr=[-6,-6,6,-5,0,2,0,-1,0,0,0,0,0,-1,0,0,-1,1,0,0,0,0,0]

arr=np.array(arr)
v,s=bitstream(arr, -4)
#print(v)


'''


            
            
    
    