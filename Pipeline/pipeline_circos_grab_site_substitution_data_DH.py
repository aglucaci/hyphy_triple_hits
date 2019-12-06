#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 16:02:46 2019

@author: alexander g lucaci

Grab site substitution data to be used to create circos plot.

http://mkweb.bcgsc.ca/tableviewer/
https://plot.ly/create/#/
"""
# =============================================================================
# Imports
# =============================================================================
import json, csv, sys
import os
import pandas as pd

# =============================================================================
# Declares
# =============================================================================
# This dict will hold all of our FROM_CODON to TO_CODON exchanges
codon_change = {}

# Keep a numeric count of the mutation type.
change_types = {}
change_types["SH"] = 0
change_types["DHT1"] = 0
change_types["DHT1A"] = 0
change_types["DHT1B"] = 0
change_types["DHT2"] = 0
change_types["TH"] = 0

# DHT1 is a tandem mutations, 2 nucleotide changes in a row
# DHT2 is a skip the middle type, nontandem 2 nucleotide change
total_DH = []



# =============================================================================
# Helper funcs.
# =============================================================================

def diff_count(from_codon, to_codon):
    count = 0
    if from_codon[0] != to_codon[0]: count += 1
    if from_codon[1] != to_codon[1]: count += 1
    if from_codon[2] != to_codon[2]: count += 1
    return count

def diff_counter(from_codon, to_codon, counter):
    count = 0
    if from_codon[0] != to_codon[0]: 
        count += 1
        
    if from_codon[1] != to_codon[1]: 
        count += 1
        
    if from_codon[2] != to_codon[2]: 
        count += 1
    
    #assign mutation type
    if count == 1: 
        change_types["SH"] += counter
    
    if count == 3: 
        #print("TH:", change_types["TH"], counter )
        change_types["TH"] += counter
        
    
    # DHT1 is a tandem mutations, 2 nucleotide changes in a row
    # DHT2 is a skip the middle type, nontandem 2 nucleotide change
    if count == 2:
        if from_codon[0] != to_codon[0] and from_codon[1] != to_codon[1] or from_codon[1] != to_codon[1] and from_codon[2] != to_codon[2]:
            #DHT1
            change_types["DHT1"] += counter
        else:
            #DHT2
            change_types["DHT2"] += counter
            
        if from_codon[0] != to_codon[0] and from_codon[1] != to_codon[1]:
            change_types["DHT1A"] += counter
        elif from_codon[1] != to_codon[1] and from_codon[2] != to_codon[2]:
            change_types["DHT1B"] += counter

        
    # end method
    

def read_json(filename):
    global codon_change, total_DH
    this_row = []
    with open(filename, "r") as fh:
        json_data = json.load(fh)
        this_row.append(json_data["Site substitutions"])
    fh.close()
    
    num_change = 0
    
    for k in this_row[0]: #This is the Site  Number
        for keys in this_row[0][k]: #Changes at this site
            from_codon = keys
            for to_codon in this_row[0][k][keys]:
                diff_counter(from_codon, to_codon, len(this_row[0][k][from_codon][to_codon]))
                
                if diff_count(from_codon, to_codon) == 1:
                    #save this here if I want to process SH's
                    pass
                
                if diff_count(from_codon, to_codon) == 2:
                    print(from_codon, to_codon)
                    
                    change_amount = {to_codon : len(this_row[0][k][from_codon][to_codon])} #counts
                    
                    if from_codon not in codon_change:
                        codon_change[from_codon] = change_amount
                    else:
                        if to_codon not in codon_change[from_codon]:
                            codon_change[from_codon][to_codon] = len(this_row[0][k][from_codon][to_codon])
                        else:
                            codon_change[from_codon][to_codon] += len(this_row[0][k][from_codon][to_codon])
                    
                if diff_count(from_codon, to_codon) == 3:
                    #DEBUG: THis is a modification to allow for DHs
                    #continue
                    """
                    change = {to_codon : len(this_row[0][k][from_codon][to_codon])} #counts       \
                    
                    if from_codon not in codon_change:
                        codon_change[from_codon] = change
                    else:
                        if to_codon not in codon_change[from_codon]:
                            codon_change[from_codon][to_codon] = len(this_row[0][k][from_codon][to_codon])  
                        else:
                            codon_change[from_codon][to_codon] += len(this_row[0][k][from_codon][to_codon])
                    #end if
                    """
                    pass
            #end for
        #end for
    total_DH.append(num_change)
    #end method
    
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
    #end method
    
# =============================================================================
# Main subroutine
# =============================================================================
# --- Command line arguments
path = sys.argv[1]
output_filename = sys.argv[2]

## ignore pvalue thresholding
#pvalue_threshold = float(sys.argv[3]) # hard-code or pass a pvalue threshold

files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(".json")]

for file in files: #main for loop
    #if pass_pvalue_threshold(file) == True:
    #   read_json(file)
    # ignore pvalue thresholding
    read_json(file)

# --- After the main for loop
#data = {}
data = codon_change
# --- THRESHOLDING
"""
for (key, value) in codon_change.items(): #DICT
    data[key] = {}
    for (key2, value2) in codon_change[key].items(): #NESTED DICT
        if codon_change[key][key2] >= 0:
            data[key][key2] =  codon_change[key][key2]
        
    if data[key] == {}: #nothing was added.
        del data[key]
"""

num_data = 0

# --- Count of total TH change:
for k in data:
    for j in data[k]:
        num_data += data[k][j]
        
print("\tTotal number of TH codon changes, after applying Codon to Codon threshold filter:", num_data)
print("\tSaving to:", output_filename)
df1 = pd.DataFrame.from_dict(data)
df1.fillna("-", inplace=True)
df1.to_csv(output_filename, sep="\t")

num_codon_change = 0

# --- Count of total TH change:
for k in codon_change:
    for j in codon_change[k]:
        num_codon_change += codon_change[k][j]
        
print("\tTotal number of TH codon changes:", num_codon_change)
change_sum = 0

for item in change_types:
    change_sum += change_types[item]

for item in change_types:
    print("\t", item, change_types[item], *[round((change_types[item]/change_sum)*100,2), "%"])





# =============================================================================
# End of file
# =============================================================================






