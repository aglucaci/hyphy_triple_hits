#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 16:43:49 2019

@author: alexander g. lucaci

Provides analysis of SELECTOME dataset.

Looks to provide biological context of alignments
with TH rate over 1.0
p-value thresholded
omega over 1.0


"""
# =============================================================================
# Imports
# =============================================================================
import sys, os
import json
from collections import Counter

# =============================================================================
# Declares
# =============================================================================
#Path of SELECTOME FITTERS
path = "/Users/alex/Documents/TRIPLE_HITS/FITTERS/SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"
nexus_path = "/Users/alex/Documents/TRIPLE_HITS/selectome_trip_ammended"


pvalue_threshold = 0.05
omega_threshold = 1.0
TH_rate_threshold = 1.0


# =============================================================================
# Helper functions
# =============================================================================
def pass_pvalue_threshold(filename):
    global pvalue_threshold
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    file_pvalue = json_data["test results"]["Triple-hit vs double-hit"]["p-value"]
    
    if float(file_pvalue) < pvalue_threshold:
        passed = True
    else:
        passed = False
        
    return passed

def pass_TH_rate_threshold():
    return True

def pass_omega_over_1():
    pass

def read_nexus_grab_genename():
    pass

def grab_genename(filename):
    #gets genename list from the fitter.json
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    output = []
    
    x = json_data["tested"]["0"]
    
    for k, v in x.items():
        
        if k[:4] != "NODE":
            #print(k[:k.find("_")])
            output.append(k[:k.find("_")])

    
    return set(output)
    
    
    
# =============================================================================
# Main function
# =============================================================================
def main():
    pass


# =============================================================================
# Main subroutine
# =============================================================================
    
files = [f for f in os.scandir(path) if f.name.endswith(".json")]

#print("Total number of files:", len(files))

files_threshold = []

"""
   "Triple-hit vs double-hit":{
     "LRT":1.353009336880859,
     "p-value":0.2447527087761215
    }

"""

gene_name_count = 0
genes = []

for n, file in enumerate(files):
    #if n == 10: break
    if pass_pvalue_threshold(file) == True:
        
        files_threshold.append(file.name.replace(".FITTER.json", ""))
        
        x = grab_genename(file)
        
        
        
        for item in x: #print the first then leave 
            print(item)
            gene_name_count += len(x)
            
            
            
            break
        
        #print(file.name[:file.name.find(".")])
    else:
        continue
    
    
print("Gene name count:", gene_name_count)
#print()
#print("pvalue threshold:", pvalue_threshold)
        
asapercent = (len(files_threshold)/len(files))*100  



print(len(files_threshold))
print(asapercent)

#print("Number of files which pass threshold:", len(files_threshold), round(asapercent, 2), "%")
#for file in files_threshold.append:
#    print(os.path.join(nexus_path))
    #open the nexus
    #get the first gene name
    #get only the gene name not the species.
    
        




# =============================================================================
# End of file
# =============================================================================
