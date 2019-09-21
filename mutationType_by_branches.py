#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 15:15:28 2019

@author: alexander lucaci

Takes in a folder where the .fitter.json files are located

Outputs a csv formatted file containing:
        Filename
        Site position
        Mutation Type
        Branch affected.
        
        
@Usage: python3 mutationType_by_branches.py <FITTER_FOLDER> > OUTPUT_FILE.csv

python mutationType_by_branches.py /Users/alex/Documents/TRIPLE_HITS/FITTERS/SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON > SELECTOME_MUTATIONS_BRANCH_SITE.csv
"""

# =============================================================================
# Imports
# =============================================================================
import sys, os
import json

# =============================================================================
# Declares
# =============================================================================

path = sys.argv[1] #Fitters directory
#path =  "/Users/alex/Documents/TRIPLE_HITS/FITTERS/SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"

filenames = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(".json")]

delimiter = "\t"
# =============================================================================
# Helper functions
# =============================================================================
def diff_counter(from_codon, to_codon):
    count = 0
    
    if from_codon[0] != to_codon[0]: 
        count += 1
    if from_codon[1] != to_codon[1]: 
        count += 1
    if from_codon[2] != to_codon[2]: 
        count += 1
    
    #assign mutation type
    if count == 1: 
        #change_types["SH"] += counter
        return "SH"
    
    if count == 3: 
        #change_types["TH"] += counter
        return "TH"
    if count == 2:
        #change_types["TH"] += counter
        return "DH"



def read_json(filename):
    
    this_row = []
    
    with open(filename, "r") as fh:
        json_data = json.load(fh)
        this_row.append(json_data["Site substitutions"])
    fh.close()

    
    short_filename = filename.split("/")[-1]
    
    for k in this_row[0]: #This is the Site Number
        
        for keys in this_row[0][k]: #Changes at this site
            
            from_codon = keys
            
            for to_codon in this_row[0][k][keys]:  
                
              mutation_type = diff_counter(from_codon, to_codon)
        
              #str(this_row[0][k][keys][to_codon])]) are, effectively, the branches
              print(delimiter.join([short_filename, k, mutation_type, str(this_row[0][k][keys][to_codon])]))
                    
    


# =============================================================================
# Main subroutine
# =============================================================================
#header
print(delimiter.join(["Filename", "Site Position", "Mutation Type", "Branch"])) 
            
for file in filenames:
    read_json(file)
