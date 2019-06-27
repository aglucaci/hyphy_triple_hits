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
import json, csv, sys, os
import pandas as pd
import numpy as np

# =============================================================================
# Declares
# =============================================================================
codon_change = {}
pvalue_threshold = 0.005
file_passed_threshold = 0
num_ER_thresholded_sites = 0

#path = "/Users/user/Documents/Pond Lab/Triple hits/Analysis/selectome_trip_ammended_analysis"
path = r"E:\SELECTOME_TRIP_AMMENDED_SRV\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"
#path = r"E:\BUSTED_SIM_SRV_FITTER_JSON\BUSTED_SIM_SRV_FITTER_JSON"

files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(".json")]
#files = ["/Users/user/Documents/Pond Lab/Triple hits/Analysis/selectome_trip_ammended_analysis/ENSGT00670000097768.Euteleostomi.003.nex.FITTER.json"]

# =============================================================================
# Helper funcs.
# =============================================================================
def diff_count(from_codon, to_codon):
    count = 0
    #print(from_codon, to_codon)
    if from_codon[0] != to_codon[0]: count += 1
    if from_codon[1] != to_codon[1]: count += 1
    if from_codon[2] != to_codon[2]: count += 1
    #print(type(from_codon), type(to_codon))
    #print(from_codon.difference(to_codon))
    return count

def subprocessing_thisrow(this_row):
    global codon_change
    for k in this_row[0]:
        for keys in this_row[0][k]:
            for to_codon in this_row[0][k][keys]:
                from_codon = keys
                if diff_count(from_codon, to_codon) == 3:
                    #print("->", filename, from_codon, to_codon)
                    change = {to_codon : len(this_row[0][k][from_codon][to_codon])} #counts   
                    if from_codon not in codon_change:
                        codon_change[from_codon] = change
                    else:
                        if to_codon not in codon_change[from_codon]:
                            codon_change[from_codon][to_codon] = len(this_row[0][k][from_codon][to_codon])
                        else:
                            codon_change[from_codon][to_codon] += len(this_row[0][k][from_codon][to_codon])

def read_json_fullfilter(filename): #Pvalue and ER Thresholdings for sensitive sites
    global codon_change, file_passed_threshold, num_ER_thresholded_sites
    this_row = []
    with open(filename, "r") as fh:
        json_data = json.load(fh)
        THvsDH_LRT_pvalue = json_data["test results"]["Triple-hit vs double-hit"]["p-value"]
        EvidenceRatio_TH = json_data["Evidence Ratios"]["Three-hit"][0]
        Site_subs = json_data["Site substitutions"]
        #Filtering
        if float(THvsDH_LRT_pvalue) >= pvalue_threshold: return #P VALUE THRESHOLDs
        Threshold_TH = 3 * np.mean(EvidenceRatio_TH)
        Filtered_Threshold_TH = list(filter(lambda x: x > Threshold_TH, EvidenceRatio_TH))
        #this_row.append(json_data["Site substitutions"])
        if Filtered_Threshold_TH == []: return #NO SITES ABOVE THRESHOLD 
        num_ER_thresholded_sites += len(Filtered_Threshold_TH) 
        for i, item in enumerate(EvidenceRatio_TH):
            if item in Filtered_Threshold_TH:
                try:
                    #print(i, "{'" + str(i) + "': " + str(Site_subs[str(i)]) + "}")
                    this_row.append({i: Site_subs[str(i)]})
                    #can do analysis here.
                except:
                    #SITE SUB NOT FOUND
                    #print("ERROR:", i, "{'" + str(i) + "': " + str(Site_subs[str(i)]) + "}")
                    #print("ERROR:", i, "SITE SUB NOT FOUND")
                    pass
        file_passed_threshold += 1
    fh.close()
    
    if len(this_row) == 0: return
    subprocessing_thisrow(this_row)
  
def read_json_p_filter(filename): #Pvalue and ER Thresholdings for sensitive sites
    global codon_change, file_passed_threshold, num_ER_thresholded_sites
    this_row = []
    with open(filename, "r") as fh:
        json_data = json.load(fh)
        THvsDH_LRT_pvalue = json_data["test results"]["Triple-hit vs double-hit"]["p-value"]
        #EvidenceRatio_TH = json_data["Evidence Ratios"]["Three-hit"][0]
        Site_subs = json_data["Site substitutions"]
        #Filtering
        if float(THvsDH_LRT_pvalue) >= pvalue_threshold: return #P VALUE THRESHOLDs
        this_row.append(Site_subs)
        file_passed_threshold += 1
    fh.close()
    
    if len(this_row) == 0: return
    subprocessing_thisrow(this_row)
    
def read_json_nofilter(filename):
    global codon_change, file_passed_threshold, num_ER_thresholded_sites
    this_row = []
    with open(filename, "r") as fh:
        json_data = json.load(fh)
        Site_subs = json_data["Site substitutions"]
        file_passed_threshold += 1
    fh.close()
    this_row.append(Site_subs)
    if len(this_row) == 0: return
    subprocessing_thisrow(this_row)


# =============================================================================
# Main subroutine
# =============================================================================
def main_sub(output_filename, mode):
    file_count = 0
    for file in files:
        #print(file_count, "Processing:", file)
        if mode == "NOFILTER": read_json_nofilter(file)
        if mode == "P_FILTER": read_json_p_filter(file)
        if mode == "FULLFILTER": read_json_fullfilter(file)
        
        file_count += 1
        
    #Sum this.
    triple_changes = 0
    SERINE_to_SERINE = 0
    SERINE_CODONS = ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"]
    
    """ This is on triple instant. changes"""
    for key in codon_change:
        #print(key, codon_change[key])
        for second_key in codon_change[key]:
            #if diff_count(key, second_key) == 3:
            triple_changes += codon_change[key][second_key]
            if key in SERINE_CODONS and second_key in SERINE_CODONS: SERINE_to_SERINE += codon_change[key][second_key]
        
    print("Number of files:", file_passed_threshold)
    if mode == "FULLFILTER": print("Number of ER Thresholded Sites:", num_ER_thresholded_sites)
    print("Total number of triple changes observed:", triple_changes)
    print("TH: Serine to Serine changesT:", SERINE_to_SERINE)
    
    #df1 = pd.DataFrame.from_dict(codon_change)
    #df1.fillna("-", inplace=True)
    #df1.to_csv("TEST_ORIGINAL_sample_circos_data_TripleHit_SELECTOME_SRV.txt", sep="\t")


# =============================================================================
# Main main
# =============================================================================
print("() No filter analysis") 
main_sub("", "NOFILTER")

codon_change, file_passed_threshold, num_ER_thresholded_sites = {}, 0 , 0
print("() p < 0.005") 
main_sub("", "P_FILTER")

codon_change, file_passed_threshold, num_ER_thresholded_sites = {}, 0 , 0
print("() p < 0.005, TH Threshold (3x)") 
main_sub("", "FULLFILTER")

codon_change, file_passed_threshold, num_ER_thresholded_sites = {}, 0 , 0
print("() p < 0.005, TH Threshold (10x)") #REMEMBER TO CHANGE THE THRESHOLD IN THE FUNCTION
main_sub("", "FULLFILTER")


#need to run this three times.
#different output files
#differnt modes
# =============================================================================
# End of file
# =============================================================================
"""
    for k in this_row[0]:
        for keys in this_row[0][k]:
            for to_codon in this_row[0][k][keys]:
                from_codon = keys
                if diff_count(from_codon, to_codon) == 3:
                    print("->", filename, from_codon, to_codon)
                    change = {to_codon : len(this_row[0][k][from_codon][to_codon])} #counts   
                    
                    if from_codon not in codon_change:
                        codon_change[from_codon] = change
                    else:
                        if to_codon not in codon_change[from_codon]:
                            pass
                            codon_change[from_codon][to_codon] = len(this_row[0][k][from_codon][to_codon])
                        
                        else:
                            codon_change[from_codon][to_codon] += len(this_row[0][k][from_codon][to_codon])
"""










