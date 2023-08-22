# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 00:03:19 2022

@author: HP
"""


from huffman import *


def vlicode(x):
    n=get_category(x)
    s=""
    y=abs(x)
    for i in range(n-1,-1,-1):
        if((y>>i)&1):
            if y==x:
                s+='1'
            else:
                s+='0'
        else:
            if y==x:
                s+='0'
            else:
                s+='1'
    
    return s

def vlicode_int(s):
    sign=1
    n=len(s)
    if n==0:
        return 0
    if s[0]=='0':
        sign=-1
    
    x=0
    
    for i in range(n):
        t=int(s[i])
        if sign==-1:
            t=1-t
        
        x=2*x+t
    return sign*x

#print(vlicode(-9))

def dcbitstream(v):
    root=generate_huffman_dc(v)
    code_dc=getcode(root)
    return code_dc,root

def acbitstream(v):
    root=generate_huffman(v)
    code_ac=getcode(root)
    return code_ac,root


def encoding(v,code_dc,code_ac):
    temp=[]
    n=v.shape[0]
    s=code_dc[get_category(v[0])]+vlicode(v[0])
    temp.append(s)
    bitstream=s
    
    for i in range(1,n-1):
        s=code_ac[(v[i][0],v[i][1])]+vlicode(v[i][2])
        temp.append(s)
        bitstream+=s
    s=code_ac[(v[n-1][0],v[n-1][1])]
    temp.append(s)
    bitstream+=s
    
    temp=np.array(temp,dtype='object')
    return temp,bitstream





    