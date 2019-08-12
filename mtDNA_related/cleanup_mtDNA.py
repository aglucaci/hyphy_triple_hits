# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 16:57:15 2019

@author: admin
"""

import glob


mtDNA_dir = r"E:\TRIPLE HITS\mtDNA\STDIN*"

files = glob.glob(mtDNA_dir)

error1 = "The input alignment must have the number of sites that is divisible by 3"
error2 = "The number of tree tips in "

def read_errorfile(filename):
    data = []
    
    with open(filename, "r") as f:
        for n, line in enumerate(f):
            #print(filename, n, [line.strip()])
            
            #if n == 23 and error2 in line:
            #    print(filename, n, [line.strip()])
            
            if n == 20 and error1 not in line: 
                print(filename, n, [line.strip()])
                
                #if error1 in line:
                #    print("$#$#$#$")

count = 0
print("Number of error files:", len(files))

for n, f in enumerate(files):
    #print("##################### ################# Reading:", n, f)
    
    read_errorfile(f)
    
    count += 1
    #if count == 3: break