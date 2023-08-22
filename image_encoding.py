# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 12:47:36 2022

@author: HP
"""

import cv2
import numpy as np
import math


from dct import *
from encoding import *
from color_conversion import *

block_size = 8

img=cv2.imread('image.jpg')
img=rgbtoycbcr(img)

[h , w, _] = img.shape



# No of blocks needed : Calculation

height = h
width = w
h = np.float32(h) 
w = np.float32(w) 

nbh = math.ceil(h/block_size)
nbh = np.int32(nbh)

nbw = math.ceil(w/block_size)
nbw = np.int32(nbw)

H =  block_size * nbh

# width of padded image
W =  block_size * nbw


padded_img = np.zeros((H,W,3))



padded_img[0:height,0:width] = img[0:height,0:width]


QDCT1=[[16,11,10,16,24,40,51,61], [12,12,14,19,26,58,60,55],
        [14,13,16,24,40,57,69,56],
       [14,17,22,29,51,87,80,62],[18,22,37,56,68,109,103,77],
       [24,35,55,64,81,104,113,92],[49,64,78,87,103,121,120,101],
       [72,92,95,98,112,100,103,99]]

QDCT2=[[17,18,24,47,99,99,99,99],[18,21,26,66,99,99,99,99],
       [24,26,56,99,99,99,99,99],[47,66,99,99,99,99,99,99],
       [99,99,99,99,99,99,99,99],[99,99,99,99,99,99,99,99],
       [99,99,99,99,99,99,99,99],[99,99,99,99,99,99,99,99]]


QDCT1=np.array(QDCT1)
QDCT2=np.array(QDCT2)

QDCT=np.array([QDCT1,QDCT2,QDCT2])

def img_break(img):
    n=img.shape[0]
    m=img.shape[1]
    
    img1=np.zeros((n,m))
    img2=np.zeros((n,m))
    img3=np.zeros((n,m))
    
    for i in range(n):
        for j in range(m):
            img1[i][j],img2[i][j],img3[i][j]=img[i][j]
    return img1,img2,img3

def img_join(img1,img2,img3):
    n=img1.shape[0]
    m=img1.shape[1]
    
    img=np.zeros((n,m,3))
   
    
    for i in range(n):
        for j in range(m):
            img[i][j][0]=img1[i][j]
            img[i][j][1]=img2[i][j]
            img[i][j][2]=img3[i][j]
            
    return img


imY,imcr,imcb=img_break(padded_img)

def zigzag_scan(img,qdct):
    n=img.shape[0]
    m=img.shape[1]
    v=[]
    n1=n//block_size
    m1=m//block_size
    
    for i in range(n1):
        row_ind_1 = i*block_size                
        row_ind_2 = row_ind_1+block_size
        
        for j in range(m1):
            col_ind_1 = j*block_size                       
            col_ind_2 = col_ind_1+block_size
                        
            block = img[ row_ind_1 : row_ind_2 , col_ind_1 : col_ind_2 ]
            #print(block.shape,i,j)
            block=dct(block)
            block = np.divide(block,qdct).astype(int)
            vtemp=zigzagscan(block)
            v.append(np.array(vtemp))
    
    v=np.array(v)
    return v


v1=zigzag_scan(imY, QDCT[0])

v2=zigzag_scan(imcr, QDCT[1])
v3=zigzag_scan(imcb, QDCT[2])      


def intermediate_symbols(v):
    v_dc=[]
    v_ac=[]
    n=v.shape[0]
    prev=0
    
    for i in range(n):
        temp,_=bitstream(v[i], prev)
        prev=v[i][0]
        v_dc.append(temp[0])
        for j in range(1,temp.shape[0]):
            v_ac.append(temp[j])
    
    v_dc=np.array(v_dc,dtype='object')
    v_ac=np.array(v_ac,dtype='object')
    
    return v_dc,v_ac


v_dc1,v_ac1=intermediate_symbols(v1)

code_dc1,root_dc1=dcbitstream(v_dc1)
code_ac1,root_ac1=acbitstream(v_ac1)

v_dc2,v_ac2=intermediate_symbols(v2)

code_dc2,root_dc2=dcbitstream(v_dc2)
code_ac2,root_ac2=acbitstream(v_ac2)

v_dc3,v_ac3=intermediate_symbols(v3)

code_dc3,root_dc3=dcbitstream(v_dc3)
code_ac3,root_ac3=acbitstream(v_ac3)


def binary_encoding(v):
    v_dc,v_ac=intermediate_symbols(v)

    code_dc,root_dc=dcbitstream(v_dc)
    code_ac,root_ac=acbitstream(v_ac)
    
    n=v_dc.shape[0]
    m=v_ac.shape[0]
    
    s=''
    array=[]
    
    i=0
    j=0
    
    flag=1
    print(n,m)
    while i<n and j<m:
        if flag==1:
            
            t=code_dc[get_category(v_dc[i])]+vlicode(v_dc[i])
            s+=t
            array.append(t)
            flag=0
            i+=1
        else:
            
            t=code_ac[(v_ac[j][0],v_ac[j][1])]
            if(t!=code_ac[(0,0)]):
                t+=vlicode(v_ac[j][2])
                s+=t
                array.append(t)
                j+=1
            else:
                s+=t
                array.append(t)
                j+=1
                flag=1
    
    while j<m:
        t=code_ac[(v_ac[j][0],v_ac[j][1])]
        if(t!=code_ac[(0,0)]):
            t+=vlicode(v_ac[j][2])
            s+=t
            array.append(t)
            j+=1
        else:
            s+=t
            array.append(t)
            j+=1
    
    
    array=np.array(array,dtype='object')
    return s,array

s1,array1=binary_encoding(v1)
s2,array2=binary_encoding(v2)
s3,array3=binary_encoding(v3)

        
            

text_file = open("encodedY.txt", "w")
 
#write string to file
text_file.write(s1)
 
#close file
text_file.close()

text_file = open("encodedcr.txt", "w")
 
#write string to file
text_file.write(s2)
 
#close file
text_file.close()

text_file = open("encodedcb.txt", "w")
 
#write string to file
text_file.write(s3)
 
#close file
text_file.close()


compression_ratio=(len(s1)+len(s2)+len(s3))/(3*height*width*8)
print(compression_ratio)


    


    



