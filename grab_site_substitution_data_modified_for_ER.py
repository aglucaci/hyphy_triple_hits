#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 16:02:46 2019

@author: alexander lucaci

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
import numpy as np

# =============================================================================
# Declares
# =============================================================================
codon_change = {}
pvalue_threshold = 0.005
passed_threshold = 0

# =============================================================================
# Helper funcs.
# =============================================================================
def diff_count(from_codon, to_codon):
    count = 0
    #print(from_codon, to_codon)
    if from_codon[0] != to_codon[0]: count += 1
    if from_codon[1] != to_codon[1]: count += 1
    if from_codon[2] != to_codon[2]: count += 1
    return count

def read_json(filename):
    global codon_change, passed_threshold
    this_row = []
    with open(filename, "r") as fh:
        json_data = json.load(fh)
        THvsDH_LRT_pvalue = json_data["test results"]["Triple-hit vs double-hit"]["p-value"]
        if float(THvsDH_LRT_pvalue) >= pvalue_threshold: return
        passed_threshold += 1
        
        
        
        data_holder = json_data["Site substitutions"]
        #this_row.append(json_data["Site substitutions"]) #all of the site subs
        TH = json_data["Evidence Ratios"]["Three-hit"][0]
        DH = json_data["Evidence Ratios"]["Two-hit"][0]
        SITES = json_data["input"]["number of sites"] #can also calculated from the len of DH or TH
        THvsDH_LRT_pvalue = json_data["test results"]["Triple-hit vs double-hit"]["p-value"]
        Site_subs = json_data["Site substitutions"]
    fh.close()
    
    #if float(THvsDH_LRT_pvalue) >= pvalue_threshold: return
    
    Threshold_TH = 3 * np.mean(TH)
    Threshold_DH = 3 * np.mean(DH)
    
    Filtered_Threshold_TH = list(filter(lambda x: x > Threshold_TH, TH))
    Filtered_Threshold_DH = list(filter(lambda x: x > Threshold_DH, DH))
    
    if Filtered_Threshold_TH > []:
        #post processing
        for i, item in enumerate(TH):
            if item in Filtered_Threshold_TH:
                this_row.append("{'" + int(i) + "': " + str(Site_subs[str(i)]) + "}")
                try:
                    #this_row.append(data_holder) #actuall a subset of it.
                    print("ADDING DATA")
                    this_row.append("{'" + int(i) + "': " + str(Site_subs[str(i)]) + "}")
                    print(this_row)
                    #this_row.append(str(Site_subs[str(i)]))
                except:
                    pass
    
    #if this_row == []: return               
    if len(this_row) == 0: return
    
    print(this_row[0])    
                
    #matrix of triple changes.
    print("() Processing.")
    for k in this_row[0]:
        print("K:", k)
        for keys in this_row[0][k]:      
            for to_codon in this_row[0][k][keys]:
                from_codon = keys
                if diff_count(from_codon, to_codon) == 3:
                    change = {to_codon : len(this_row[0][k][from_codon][to_codon])} #counts           
                    if from_codon not in codon_change:
                        codon_change[from_codon] = change
                    else:
                        if to_codon not in codon_change[from_codon]:
                            pass
                            codon_change[from_codon][to_codon] = len(this_row[0][k][from_codon][to_codon])
                        
                        else:
                            codon_change[from_codon][to_codon] += len(this_row[0][k][from_codon][to_codon])
    

# =============================================================================
# Main subroutine
# =============================================================================

#path = "/Users/user/Documents/Pond Lab/Triple hits/Analysis/selectome_trip_ammended_analysis"
path = r"E:\SELECTOME_TRIP_AMMENDED_SRV\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"
#path = r"E:\BUSTED_SIM_SRV_FITTER_JSON\BUSTED_SIM_SRV_FITTER_JSON"

files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(".json")]
#files = ["/Users/user/Documents/Pond Lab/Triple hits/Analysis/selectome_trip_ammended_analysis/ENSGT00670000097768.Euteleostomi.003.nex.FITTER.json"]
file_count = 0

for file in files:
    print(file_count, "Processing:", file)
    read_json(file)
    file_count += 1

# SAVE AS TAB DELIMTED FILE
data = codon_change
df1 = pd.DataFrame.from_dict(data)
df1.fillna("-", inplace=True)
df1.to_csv("RE_MODOIFIED_sample_circos_data_TripleHit_SELECTOME_SRV.txt", sep="\t")

print()
print("Passed threshold:", passed_threshold)










