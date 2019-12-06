#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 11:22:14 2019

@author: alexander lucaci

data munging, Nexus datatype correction Protein to DNA.

"""
import os

subdir = "/selectome_trip_ammended"

def write_correction(filename, lines):
    with open(filename, "w") as f:
        for line in lines:
            if line == "\t\tDATATYPE = PROTEIN\n":
                line = "\t\tDATATYPE = DNA\n"
            f.write(line)
    f.close()

def read_and_check(filename):
    #read
    with open(filename, "r") as f:
        lines = f.readlines()
    f.close()

    #check
    for line in lines:
        #if "DATATYPE = PROTEIN" in line:
        if line == "\t\tDATATYPE = PROTEIN\n":
            print(filename, [line])
            write_correction(filename, lines)

path = os.getcwd()
files = [path+subdir+"/"+f.name for f in os.scandir(path+subdir) if f.is_file()]

for file in files:
    read_and_check(file)
    #print(file)

# =============================================================================
# END OF FILE
# =============================================================================
    