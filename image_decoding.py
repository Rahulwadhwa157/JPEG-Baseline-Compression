# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 19:24:45 2022

@author: HP
"""


import cv2
import numpy as np
import math


from image_encoding import *

text_file = open("encodedY.txt", "r")
 
#write string to file
s1=text_file.read()
 
#close file
text_file.close()

text_file = open("encodedcr.txt", "r")
 
#write string to file
s2=text_file.read()
 
#close file
text_file.close()

text_file = open("encodedcb.txt", "r")
 
#write string to file
s3=text_file.read()
 
#close file
text_file.close()

def binary_decoding(s,root_dc,root_ac):
    n=len(s)
    symbol_dc=dict()
    symbol_ac=dict()
    
    v_dc=[]
    v_ac=[]
    
    i=0
    flag=1
   
    
    while i<n:
        if flag==1:
            stemp,j=get_symbols(root_dc, s[i:], symbol_dc)
            j+=i
            #print(i,j,j+stemp)
            x=vlicode_int(s[j:j+stemp])
            v_dc.append(x)
            flag=0
            i=j+stemp
        else:
            stemp,j=get_symbols(root_ac, s[i:], symbol_dc)
            if ((stemp[0],stemp[1])==(0,0)):
                flag=1
                v_ac.append(stemp)
                j+=i
                i=j
            else:
                n1=stemp[1]
                j+=i
                x=vlicode_int(s[j:j+n1])
                v_ac.append((stemp[0],stemp[1],x))
                i=j+n1
    
    v_dc=np.array(v_dc,dtype='object')
    v_ac=np.array(v_ac,dtype='object')
    
    return v_dc,v_ac


dc1,ac1=binary_decoding(s1, root_dc1, root_ac1)
dc2,ac2=binary_decoding(s2, root_dc2, root_ac2)
dc3,ac3=binary_decoding(s3, root_dc3, root_ac3)
    
                
                
def dc_ac_merge(v_dc,v_ac):
    n=v_dc.shape[0]
    m=v_ac.shape[0]
    
    flag=1
    v=[]
    
    vtemp=[]
    i=0
    j=0
    
    while i<n or j<m:
        if flag==1:
            vtemp.append(v_dc[i])
            i+=1
            flag=0
        else:
            vtemp.append(v_ac[j])
            if (v_ac[j][0],v_ac[j][1])==(0,0):
                flag=1
                v.append(np.array(vtemp,dtype='object'))
                vtemp=[]
            j+=1
    
    v=np.array(v,dtype='object')
    return v


v1_merge=dc_ac_merge(dc1,ac1)
v2_merge=dc_ac_merge(dc2,ac2)
v3_merge=dc_ac_merge(dc3,ac3)  

def get_zigzag_temp(v_merge,prev=0):
    n=v_merge.shape[0]
    v1=[]
    
    v1.append(v_merge[0]+prev)
    
    for i in range(1,n-1):
        cnt=v_merge[i][0]
        
        for k in range(cnt):
            v1.append(0)
        v1.append(v_merge[i][2])
    
    m=len(v1)
    for i in range(64-m):
        v1.append(0)
    return v1


def get_zigzag(v):
    n=v.shape[0]
    v1=np.zeros((n,64))
    
    prev=0
    for i in range(n):
        v1[i]=get_zigzag_temp(v[i],prev)
        prev=v1[i][0]
    
    return v1

v1_zig=get_zigzag(v1_merge)
v2_zig=get_zigzag(v2_merge)
v3_zig=get_zigzag(v3_merge)



def inv_zigzag_scan(v_zig,qdct):
    n=H
    m=W
    p=v_zig.shape[0]
    n1=n//block_size
    m1=m//block_size
    
    img=np.zeros((n,m))
    c=0
    
    for i in range(n1):
        row_ind_1 = i*block_size                
        row_ind_2 = row_ind_1+block_size
        
        for j in range(m1):
            col_ind_1 = j*block_size                       
            col_ind_2 = col_ind_1+block_size
            vtemp=v_zig[c]
            c+=1
            block=inv_zigzag(vtemp)
            block=np.multiply(block,qdct)
            block=idct(block)
            img[ row_ind_1 : row_ind_2 , col_ind_1 : col_ind_2 ]=block
           
    
    return img


retrieved_padded1=inv_zigzag_scan(v1_zig, QDCT[0])
retrieved_padded2=inv_zigzag_scan(v2_zig, QDCT[1])
retrieved_padded3=inv_zigzag_scan(v3_zig, QDCT[2])

retrieved_padded=img_join(retrieved_padded1, retrieved_padded2, retrieved_padded3)

retrieved_image=np.zeros((height,width,3))
retrieved_image[0:height,0:width] = retrieved_padded[0:height,0:width]

decoded_image=ycbcrtorgb(retrieved_image)

cv2.imwrite('decoded_image.jpg',decoded_image)

        
        
    
    

            
            
    
    
    
    


