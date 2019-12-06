#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 18:22:31 2019

@author: phylo
"""
# =============================================================================
# imports
# =============================================================================
import os

# =============================================================================
# Declares
# =============================================================================

BIONJ_DIR = "PETROV/bestrecip_prank_alignments/Trees/BioNJ"
NJ_DIR = "PETROV/bestrecip_prank_alignments/Trees/NJ"

count = 0

#make output dir
output_dir = os.path.join(BIONJ_DIR, "ForHyPhy")

    
# =============================================================================
# Helper functions
# =============================================================================
    

def readfile(filename, input_directory):
    with open(filename, "r") as f:
        for n, line in enumerate(f):
            #print(n, [line])
            
            #only one line
            #delete up to first "("
            
            print(line[line.find("("):])
            
            data = line[line.find("("):]
            filename = filename.split("/")[-1] + "_hyphy.nwk"
            output_dir = os.path.join(input_directory, "ForHyPhy")
            
            write_newfile(data, filename, output_dir)
            print(".. Done")
            print()
            
    f.close()
    return 0



def write_newfile(data, filename, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    #filename = filename.split("/")[:-1] + "/
    
    output_file = os.path.join(os.getcwd(), output_dir)
    output_file = os.path.join(output_file, filename)
    
    print("Saving ..", output_file)
    #print("filename:", filename)
    #print("Output_dir:", output_dir)
    #print("Output_file:", output_file)
    print()
    
    #return 1
    
    with open(output_file, "w") as f:
        f.write(data)
    f.close()
    
    return 0

def mainsub(input_directory):
    count = 0
    for root, dirs, files in os.walk(input_directory):
        for n, file in enumerate(files):
            
            if file == ".DS_Store": continue
        
            if not ".nwk" in file:
                print(n, file)
                readfile(os.path.join(input_directory, file), input_directory)
            
            #if count == 0: break
            count += 1
        
# =============================================================================
# main subrtn
# =============================================================================
mainsub(BIONJ_DIR)

mainsub(NJ_DIR)

# =============================================================================
# end of file
# =============================================================================
