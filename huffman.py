# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 12:51:14 2022

@author: HP
"""

# A Huffman Tree Node
import heapq
from img_to_rle import *

class node:
	def __init__(self, freq, symbol, left=None, right=None):
		# frequency of symbol
		self.freq = freq

		# symbol name (character)
		self.symbol = symbol

		# node left of current node
		self.left = left

		# node right of current node
		self.right = right

		# tree direction (0/1)
		self.huff = ''
		
	def __lt__(self, nxt):
		return self.freq < nxt.freq
		

def printNodes(node, val=''):
	
	# huffman code for current node
	newVal = val + str(node.huff)

	# if node is not an edge node
	# then traverse inside it
	if(node.left):
		printNodes(node.left, newVal)
	if(node.right):
		printNodes(node.right, newVal)

		# if node is edge node then
		# display its huffman code
	if(not node.left and not node.right):
		print(f"{node.symbol} -> {newVal}")


def getcodetemp(node,bincodes,val=''):
    newVal = val + str(node.huff)
    
    
    if(node.left):
        getcodetemp(node.left, bincodes, newVal)
        
    if(node.right):
        getcodetemp(node.right, bincodes, newVal)
    
    if(not node.left and not node.right):
        bincodes[node.symbol]=newVal


def getcode(node):
    bincodes=dict()
    getcodetemp(node,bincodes,val='')
    
    return bincodes
    
    


def generate_huffman(v):
    sym=dict()
    for i in range(1,v.shape[0]):
        key=(v[i][0],v[i][1])
        if(sym.get(key)==None):
            sym[key]=1
        else:
            sym[key]+=1
            
    
    # list containing unused nodes
    nodes = []
    
    # converting characters and frequencies
    # into huffman tree nodes
    for key in sym:
    	heapq.heappush(nodes, node(sym[key], key))
    
    while len(nodes) > 1:
    	
    	
    	left = heapq.heappop(nodes)
    	right = heapq.heappop(nodes)
    
    	# assign directional value to these nodes
    	left.huff = 0
    	right.huff = 1
    
    	# combine the 2 smallest nodes to create
    	# new node as their parent
    	newNode = node(left.freq+right.freq, left.symbol+right.symbol, left, right)
    
    	heapq.heappush(nodes, newNode)
    
    return nodes[0]



def generate_huffman_dc(v):
    sym=dict()
    prev=0
    for i in range(v.shape[0]):
        key=get_category(v[i]-prev)
        if(sym.get(key)==None):
            sym[key]=1
        else:
            sym[key]+=1
        prev=v[i]
            
    
    # list containing unused nodes
    nodes = []
    
    # converting characters and frequencies
    # into huffman tree nodes
    for key in sym:
    	heapq.heappush(nodes, node(sym[key], key))
    
    while len(nodes) > 1:
    	
    	
    	left = heapq.heappop(nodes)
    	right = heapq.heappop(nodes)
    
    	# assign directional value to these nodes
    	left.huff = 0
    	right.huff = 1
    
    	# combine the 2 smallest nodes to create
    	# new node as their parent
    	newNode = node(left.freq+right.freq, left.symbol+right.symbol, left, right)
    
    	heapq.heappush(nodes, newNode)
    
    return nodes[0]
# Huffman Tree is ready!

#temp=generate_huffman(v)
#printNodes(generate_huffman(v))

def get_symbols(root,s,code,i=0):
    n=len(s)
    if(code.get(s)==True):
        return code[s],n
    
    if(not root.left and not root.right):
        code[s[0:i]]=root.symbol
        return root.symbol,i
        
    
    if(i==n):
        code[s]=root.symbol
        return code[s],n
    
    if(s[i]=='0'):
        return get_symbols(root.left, s, code,i+1)
    if(s[i]=='1'):
        return get_symbols(root.right, s, code,i+1)


'''
code=dict()
code=getcode(temp)
#print(code)

'''

    
    
    
    
    
    

    