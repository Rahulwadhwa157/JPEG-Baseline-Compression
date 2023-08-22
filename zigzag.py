# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 18:27:39 2022

@author: HP
"""

import numpy as np

rw=[0,1,1,-1]
col=[1,-1,0,1]

def issafe(i,j,n,m):
    return i>=0 and i<n and j>=0 and j<m




def rec(i,j,n,m,d,x,cnt,a,flag,arr):
    if(cnt==n*m):
        return
    
    
    arr.append(a[i][j])
    #print(i,j,d,x,cnt)
    
    
    d1=d
    x1=x
    cnt1=cnt+1
    flag1=flag
    
    
    
    if((d==0 or d==2) and x==1):
        
        x1=0
        
        if flag==0:
            d1=(d+1)%4
        else:
            d1=(d+3)%4
        
    
    
    i1=i+rw[d1]
    j1=j+col[d1]
    
    if(issafe(i1,j1,n,m)==0):
        d1=(d1+1)%4
    
    i1=i+rw[d1]
    j1=j+col[d1]
    
    if(issafe(i1,j1,n,m)==0):
        d1=(d1+2)%4
        flag1=1
    
    i1=i+rw[d1]
    j1=j+col[d1]
    
    if(issafe(i1,j1,n,m)==0):
        return
    
    
    if(d1==0 or d1==2):
        x1=x1+1
    rec(i1,j1,n,m,d1,x1,cnt1,a,flag1,arr)
    

def rec2(i,j,n,m,d,x,cnt,a,flag,arr):
    if(cnt==n*m):
        return
    
    
    #arr.append(a[i][j])
    a[i][j]=arr[cnt]
    #print(i,j,d,x,cnt)
    
    
    d1=d
    x1=x
    cnt1=cnt+1
    flag1=flag
    
    
    
    if((d==0 or d==2) and x==1):
        
        x1=0
        
        if flag==0:
            d1=(d+1)%4
        else:
            d1=(d+3)%4
        
    
    
    i1=i+rw[d1]
    j1=j+col[d1]
    
    if(issafe(i1,j1,n,m)==0):
        d1=(d1+1)%4
    
    i1=i+rw[d1]
    j1=j+col[d1]
    
    if(issafe(i1,j1,n,m)==0):
        d1=(d1+2)%4
        flag1=1
    
    i1=i+rw[d1]
    j1=j+col[d1]
    
    if(issafe(i1,j1,n,m)==0):
        return
    
    
    if(d1==0 or d1==2):
        x1=x1+1
    rec2(i1,j1,n,m,d1,x1,cnt1,a,flag1,arr)
    
    
'''
a=[[0 for j in range(8)] for i in range(8)]

for i in range(8):
    for j in range(8):
        a[i][j]=8*i+j+1


a=np.array(a)
#rec(0,0,8,8,0,0,0,a,0)
'''

def zigzagscan(a):
    n=a.shape[0]
    m=a.shape[1]
    
    arr=[]
    rec(0,0,8,8,0,0,0,a,0,arr)
    
    arr=np.array(arr)
    return arr


def inv_zigzag(arr):
    a=np.zeros((8,8))
    rec2(0,0,8,8,0,0,0,a,0,arr)
    return a
'''
arr=zigzagscan(a)
#print(arr)

 ''' 
    
    
    
    







    
    
    
    

        
        
        
    