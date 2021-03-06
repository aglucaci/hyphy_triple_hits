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

# =============================================================================
# Declares
# =============================================================================
codon_change = {}
change_types = {}
change_types["SH"] = 0
change_types["DHT1"] = 0
change_types["DHT1A"] = 0
change_types["DHT1B"] = 0
change_types["DHT2"] = 0
change_types["TH"] = 0

#DHT1 is a tandem mutations, 2 nucleotide changes in a row
#DHT2 is a skip the middle type, nontandem 2 nucleotide change
total_TH = []



# =============================================================================
# Helper funcs.
# =============================================================================
"""
def diff_count(from_codon, to_codon):
    count = 0

    if from_codon[0] != to_codon[0]: count += 1
    if from_codon[1] != to_codon[1]: count += 1
    if from_codon[2] != to_codon[2]: count += 1
    return count

"""

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
        
    
    #DHT1 is a tandem mutations, 2 nucleotide changes in a row
    #DHT2 is a skip the middle type, nontandem 2 nucleotide change
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

        
        
    #return count
    

def read_json(filename):
    global codon_change, total_TH
    
    this_row = []
    
    with open(filename, "r") as fh:
        json_data = json.load(fh)
        this_row.append(json_data["Site substitutions"])
    fh.close()
    
    num_change = 0
    
    for k in this_row[0]: #This is the Site  Number
        
        #print("THIS_ROW:", this_row)
        #print(k)
        
        for keys in this_row[0][k]: #Changes at this site
            #print(keys, this_row[0][k][keys])
            #E.g.
            #GGT {'AAT': {'0': 'Apochrysa_matsumurae', '1': 'Ditaxis_biseriata'}, 'GGA': {'0': 'Node1', '1': 'Chrysoperla_nipponensis'}}
            from_codon = keys
            
            for to_codon in this_row[0][k][keys]:
                
                #print(filename.split("/")[-1], k, from_codon, to_codon) #all the changes, site substitutions
                
                diff_counter(from_codon, to_codon, len(this_row[0][k][from_codon][to_codon]))
                
                if diff_count(from_codon, to_codon) == 1:
                    
                    #print(filename.split("/")[-1].replace(".FITTER.json", ""), k, from_codon, to_codon, this_row[0][k][from_codon][to_codon], len(this_row[0][k][from_codon][to_codon]) )
                    #num_change += len(this_row[0][k][from_codon][to_codon])
                    #print(filename.split("/")[-1].replace(".FITTER.json", ""), k, from_codon, to_codon, this_row[0][k][from_codon][to_codon], len(this_row[0][k][from_codon][to_codon]) )
                    pass
                
                if diff_count(from_codon, to_codon) == 2:
                    #print(filename.split("/")[-1].replace(".FITTER.json", ""), k, from_codon, to_codon, this_row[0][k][from_codon][to_codon], len(this_row[0][k][from_codon][to_codon]) )
                    pass
                    #num_change += 1 
                    
                if diff_count(from_codon, to_codon) == 3:
                    #num_change += 1
                    #print(len(this_row[0][k][from_codon][to_codon]))
                    if len(this_row[0][k][from_codon][to_codon]) > 1: 
                        
                        #print(filename.split("/")[-1].replace(".FITTER.json", ""), k, from_codon, to_codon, this_row[0][k][from_codon][to_codon], len(this_row[0][k][from_codon][to_codon]) )
                        
                        #print(filename.split("/")[-1], k, from_codon, to_codon)
                        pass
                    change = {to_codon : len(this_row[0][k][from_codon][to_codon])} #counts       \
                    #print(change)
                    
                    if from_codon not in codon_change:
                        codon_change[from_codon] = change
                        #print(change)
                        
                    else:
                        if to_codon not in codon_change[from_codon]:
                            codon_change[from_codon][to_codon] = len(this_row[0][k][from_codon][to_codon])  
                        else:
                            
                            codon_change[from_codon][to_codon] += len(this_row[0][k][from_codon][to_codon])
                            
    #print("num TH change:", num_change)
    total_TH.append(num_change)
    
    
def pass_pvalue_threshold(filename):
    global pvalue_threshold
    #pvalue_threshold = 10000
    
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    file_pvalue = json_data["test results"]["Triple-hit vs double-hit"]["p-value"]
    
    
    #print(filename, file_pvalue)
    if float(file_pvalue) < pvalue_threshold:
        passed = True
    else:
        passed = False
        
    return passed
# =============================================================================
# Main subroutine
# =============================================================================

#path = "/Users/user/Documents/Pond Lab/Triple hits/Analysis/selectome_trip_ammended_analysis"
#path = r"E:\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"
#path = r"E:\BUSTED_SIM_SRV_FITTER_JSON\BUSTED_SIM_SRV_FITTER_JSON"
#path = "/Users/alex/Documents/TRIPLE_HITS/mtDNA/updatedAnalysis_mtDNA_combined(FASTA_AND_FITTERS)"

#path = "/Users/alex/Documents/TRIPLE_HITS/mtDNA/Vertebrate_mtDNA_FITTERS"
#path = "/Users/alex/Documents/TRIPLE_HITS/mtDNA/Invertebrate_mtDNA_FITTERS"   
#output_filename = "sample_circos_data_TripleHit_Invertebrate_mtDNA.txt"                

path = sys.argv[1]
output_filename = sys.argv[2]
#pvalue_threshold = 10000   
pvalue_threshold = float(sys.argv[3])   
files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(".json")]
#files = ["/Users/user/Documents/Pond Lab/Triple hits/Analysis/selectome_trip_ammended_analysis/ENSGT00670000097768.Euteleostomi.003.nex.FITTER.json"]

for file in files:
    #print(file)
    if pass_pvalue_threshold(file) == True:
        read_json(file)

#print(len(codon_change), len(codon_change["AGG"]))




# SAVE AS TAB DELIMTED FILE
#data = {'AGG': {'GGC': 68, 'TCT': 32, 'CAC': 76, 'GAC': 38, 'CAT': 48, 'TGT': 22, 'GAG': 264, 'TGG': 124, 'ACG': 170, 'AGT': 261, 'TTA': 12, 'AGC': 376, 'GGA': 73, 'GGG': 390, 'GTG': 131, 'ACA': 98, 'GAT': 24, 'CGT': 252, 'CAA': 88, 'GGT': 22, 'CTT': 9, 'CTC': 8, 'ACT': 52, 'AAG': 1811, 'AAC': 158, 'AGA': 3034, 'CAG': 478, 'TGC': 34, 'CCA': 16, 'CCC': 12, 'CCT': 5, 'TCG': 30, 'ATT': 30, 'GCC': 75, 'ACC': 57, 'CTG': 60, 'GCG': 132, 'TTC': 12, 'CTA': 4, 'TAT': 16, 'GTA': 16, 'CGA': 405, 'AAT': 167, 'TCA': 48, 'ATC': 21, 'CCG': 21, 'TCC': 33, 'GCT': 37, 'ATG': 273, 'GTT': 22, 'ATA': 13, 'TTG': 37, 'GAA': 73, 'GTC': 22, 'CGG': 2316, 'TAC': 21, 'GCA': 63, 'CGC': 797, 'TTT': 13, 'AAA': 346}, 'CGT': {'AGG': 216, 'GGC': 31, 'TCT': 103, 'CCT': 80, 'TGC': 72, 'CAT': 949, 'TGT': 383, 'GGT': 77, 'GAG': 17, 'TGG': 28, 'TCA': 9, 'ACG': 9, 'AGT': 197, 'AGC': 52, 'GGA': 13, 'TTG': 3, 'GTG': 7, 'ACA': 5, 'GAT': 42, 'GTT': 26, 'CAA': 154, 'CAC': 212, 'CTT': 122, 'CTC': 47, 'ACT': 32, 'AAG': 63, 'AAC': 54, 'AGA': 217, 'CAG': 232, 'GAC': 13, 'TTC': 13, 'CCC': 10, 'TCG': 7, 'ATT': 23, 'GCC': 20, 'ACC': 14, 'GCG': 7, 'CTA': 5, 'GCA': 6, 'GTA': 4, 'TCC': 41, 'AAT': 164, 'CCA': 7, 'ATC': 10, 'TAT': 135, 'CGA': 784, 'GCT': 48, 'ATG': 8, 'ATA': 3, 'GGG': 8, 'CCG': 3, 'GAA': 28, 'GTC': 24, 'CGG': 1051, 'CTG': 26, 'TAC': 37, 'CGC': 2172, 'TTT': 44, 'AAA': 82}, 'TCG': {'AGG': 31, 'GGC': 21, 'TCT': 2274, 'CCT': 25, 'GAC': 13, 'CAT': 10, 'TGT': 25, 'GGT': 9, 'GAG': 146, 'TGG': 128, 'ACG': 473, 'AGT': 234, 'TTA': 48, 'AGC': 408, 'GGA': 23, 'ATG': 158, 'TTG': 738, 'ACA': 151, 'GAT': 6, 'CGT': 9, 'CAA': 36, 'GCC': 170, 'CTT': 9, 'CTC': 16, 'ACT': 58, 'AAG': 99, 'AAC': 21, 'CGA': 6, 'AGA': 16, 'CAG': 211, 'TGC': 28, 'TCA': 5132, 'CCC': 36, 'CAC': 21, 'GTG': 194, 'ATT': 8, 'TTC': 18, 'ACC': 87, 'GCG': 557, 'CTA': 10, 'TAT': 9, 'GTA': 16, 'CCG': 180, 'AAT': 23, 'CCA': 64, 'ATC': 7, 'TAC': 15, 'TCC': 2847, 'GCT': 63, 'GTT': 15, 'ATA': 15, 'GGG': 68, 'GAA': 39, 'GTC': 17, 'CGG': 44, 'CTG': 226, 'GCA': 180, 'CGC': 4, 'TTT': 18, 'AAA': 38}, 'GGC': {'AGG': 74, 'CAA': 75, 'TCG': 27, 'TCT': 113, 'TTA': 14, 'CAC': 306, 'TGC': 222, 'CAT': 61, 'TGT': 47, 'GAG': 184, 'TGG': 12, 'ACG': 40, 'AGT': 370, 'AAT': 350, 'AGC': 2568, 'GGA': 3502, 'GGG': 3504, 'TTG': 15, 'TTC': 53, 'GAT': 193, 'CGT': 32, 'ACA': 54, 'GGT': 5370, 'CTT': 19, 'CTC': 54, 'ACT': 102, 'AAG': 161, 'AAC': 1627, 'AGA': 66, 'CAG': 125, 'GAC': 939, 'CCA': 16, 'CCC': 91, 'CCT': 27, 'GTG': 47, 'ATT': 20, 'GCC': 969, 'ACC': 354, 'GCG': 77, 'CTA': 3, 'GTA': 15, 'CGA': 14, 'GTT': 45, 'AAA': 152, 'TCA': 70, 'ATC': 99, 'TAT': 8, 'TCC': 292, 'GCT': 222, 'CCG': 17, 'ATG': 33, 'GAA': 136, 'GTC': 210, 'CGG': 25, 'CTG': 22, 'TAC': 61, 'CGC': 222, 'TTT': 21, 'ATA': 9, 'GCA': 106}, 'TCT': {'AGG': 32, 'GGC': 124, 'TAC': 86, 'CCT': 992, 'TGC': 235, 'CAT': 236, 'TGT': 1053, 'GAG': 96, 'TGG': 52, 'ACG': 229, 'AGT': 3383, 'TTA': 88, 'AGC': 2088, 'GGA': 68, 'GGG': 62, 'GTG': 126, 'TTC': 163, 'GAT': 209, 'CGT': 109, 'CAA': 103, 'GGT': 213, 'CTT': 213, 'CTC': 78, 'ACT': 1999, 'AAG': 89, 'AAC': 215, 'CGA': 15, 'AGA': 44, 'CAG': 200, 'GAC': 82, 'TCA': 8425, 'CCC': 235, 'CAC': 125, 'TCG': 6214, 'ATT': 152, 'GCC': 728, 'ACC': 503, 'GCG': 259, 'CTA': 29, 'GTA': 34, 'TCC': 17336, 'AAT': 567, 'ACA': 444, 'CCA': 175, 'ATC': 50, 'TAT': 355, 'CCG': 71, 'GCT': 2580, 'ATG': 134, 'GTT': 240, 'ATA': 32, 'TTG': 262, 'GAA': 71, 'GTC': 88, 'CGG': 33, 'CTG': 159, 'GCA': 378, 'CGC': 41, 'TTT': 748, 'AAA': 95}, 'CAC': {'AGG': 54, 'GGC': 189, 'TCT': 111, 'CCT': 49, 'AAA': 207, 'GAC': 302, 'CAT': 6316, 'TGT': 152, 'GAG': 186, 'TGG': 59, 'ACG': 26, 'AGT': 126, 'TTA': 16, 'AGC': 596, 'GGA': 25, 'GGG': 35, 'TCG': 23, 'TTC': 341, 'GAT': 75, 'CGT': 225, 'ACA': 46, 'GGT': 34, 'CTT': 87, 'CTC': 419, 'ACT': 59, 'AAG': 200, 'TCC': 368, 'AGA': 61, 'CAG': 1494, 'TGC': 676, 'AAC': 792, 'CCA': 24, 'CCC': 265, 'GTG': 28, 'ATT': 25, 'GCC': 164, 'ACC': 186, 'GCG': 19, 'CTA': 21, 'GTA': 12, 'CCG': 27, 'AAT': 187, 'CAA': 665, 'TCA': 60, 'ATC': 83, 'TAT': 262, 'CGA': 109, 'GCT': 45, 'ATG': 60, 'GTT': 29, 'ATA': 10, 'TTG': 26, 'GAA': 142, 'GTC': 102, 'CGG': 139, 'CTG': 100, 'TAC': 1049, 'CGC': 1328, 'TTT': 127, 'GCA': 42}, 'GAC': {'AGG': 63, 'GGC': 747, 'TCT': 91, 'CAC': 446, 'TGC': 91, 'CAT': 78, 'TGT': 20, 'GAG': 1834, 'TGG': 15, 'ACG': 55, 'AGT': 307, 'TTA': 23, 'AGC': 1401, 'GGA': 85, 'GGG': 97, 'TCG': 23, 'TTC': 58, 'GAT': 7317, 'GTT': 41, 'ACA': 103, 'GCA': 71, 'GGT': 96, 'CTT': 18, 'CTC': 76, 'ACT': 96, 'AAG': 293, 'AAC': 1827, 'CGA': 14, 'AGA': 68, 'CAG': 480, 'TTG': 14, 'TCA': 78, 'CCC': 101, 'CCT': 42, 'GTG': 35, 'ATT': 22, 'GCC': 649, 'ACC': 394, 'GCG': 67, 'CTA': 7, 'CGT': 18, 'GTA': 14, 'CCG': 20, 'AAT': 350, 'CAA': 203, 'CCA': 28, 'ATC': 74, 'TAT': 36, 'TCC': 239, 'GCT': 115, 'ATA': 12, 'ATG': 38, 'GAA': 1219, 'GTC': 152, 'CGG': 30, 'CTG': 29, 'TAC': 113, 'CGC': 114, 'TTT': 20, 'AAA': 313}, 'CAT': {'AGG': 27, 'GGC': 51, 'TCT': 230, 'CAC': 6454, 'TGC': 113, 'TGT': 593, 'GAG': 94, 'TGG': 44, 'ACG': 20, 'AGT': 369, 'TTA': 15, 'AGC': 137, 'GGA': 14, 'TTG': 28, 'TCG': 21, 'TTC': 63, 'GAT': 226, 'CGT': 948, 'CAA': 495, 'GGG': 20, 'GGT': 101, 'CTT': 275, 'CTC': 55, 'ACT': 93, 'AAG': 106, 'AAC': 141, 'AGA': 37, 'CAG': 1019, 'GAC': 57, 'CCA': 22, 'CCC': 43, 'CCT': 158, 'GTG': 21, 'ATT': 61, 'GCC': 36, 'ACC': 39, 'GCG': 13, 'CTA': 17, 'GCA': 32, 'GTA': 10, 'CGA': 74, 'AAT': 580, 'ACA': 23, 'TCA': 41, 'ATC': 21, 'TAT': 719, 'TCC': 76, 'GCT': 98, 'GTT': 58, 'ATA': 7, 'ATG': 32, 'CCG': 18, 'GAA': 95, 'GTC': 25, 'CGG': 117, 'CTG': 81, 'TAC': 192, 'CGC': 165, 'TTT': 245, 'AAA': 112}, 'TGT': {'AGG': 29, 'GGC': 70, 'TCT': 531, 'CAC': 144, 'TGC': 5327, 'CAT': 465, 'GGT': 179, 'GAG': 18, 'TGG': 86, 'ACG': 17, 'AGT': 484, 'TTA': 38, 'AGC': 124, 'GGA': 23, 'ATG': 37, 'GTG': 65, 'TTC': 43, 'GAT': 57, 'CGT': 309, 'CAA': 41, 'CCT': 46, 'CTT': 114, 'CTC': 45, 'ACT': 152, 'AAG': 22, 'AAC': 61, 'AGA': 27, 'CAG': 86, 'GAC': 24, 'TTG': 61, 'TCA': 48, 'CCC': 11, 'TCG': 37, 'ATT': 67, 'GCC': 73, 'ACC': 59, 'GCG': 26, 'CTA': 8, 'GCA': 27, 'GTA': 15, 'CGA': 18, 'AAT': 176, 'ACA': 46, 'CCA': 10, 'ATC': 41, 'TAT': 411, 'TCC': 99, 'GCT': 176, 'GTT': 115, 'ATA': 10, 'GGG': 22, 'CCG': 5, 'GAA': 15, 'GTC': 48, 'CGG': 41, 'CTG': 72, 'TAC': 90, 'CGC': 70, 'TTT': 183, 'AAA': 24}, 'GAG': {'AGG': 488, 'CGT': 45, 'GGC': 182, 'TCT': 176, 'CAC': 349, 'GAC': 2297, 'CAT': 197, 'TGT': 36, 'GGT': 85, 'TGG': 115, 'TCA': 258, 'ACG': 383, 'AGT': 325, 'TTA': 54, 'AGC': 526, 'GGA': 178, 'GGG': 803, 'GTG': 639, 'ACA': 338, 'GAT': 1580, 'AAT': 541, 'CAA': 389, 'CCT': 73, 'CTT': 33, 'CTC': 47, 'ACT': 135, 'AAG': 1893, 'AAC': 651, 'CGA': 68, 'AGA': 151, 'CAG': 2769, 'TGC': 35, 'TTG': 214, 'TTC': 25, 'CCC': 110, 'TCG': 229, 'ATT': 62, 'GCC': 365, 'ACC': 216, 'GCG': 789, 'CTA': 36, 'TAT': 93, 'GTA': 67, 'TCC': 169, 'GTT': 76, 'CCA': 128, 'ATC': 53, 'TAC': 81, 'CCG': 187, 'GCT': 213, 'ATA': 68, 'ATG': 458, 'GAA': 13287, 'GTC': 101, 'CGG': 270, 'CTG': 304, 'AAA': 458, 'CGC': 91, 'TTT': 36, 'GCA': 460}, 'TGG': {'AGG': 137, 'GGC': 25, 'TCT': 30, 'CAC': 58, 'GAC': 9, 'CAT': 52, 'TGT': 148, 'GAG': 75, 'ACG': 29, 'AGT': 25, 'TTA': 38, 'AGC': 26, 'GGA': 28, 'ATG': 93, 'GTG': 80, 'TTC': 176, 'GAT': 7, 'CGT': 25, 'ACA': 19, 'GGG': 187, 'GGT': 8, 'CTT': 17, 'CTC': 18, 'ACT': 6, 'AAG': 115, 'AAC': 20, 'CGA': 33, 'AGA': 29, 'CAG': 584, 'TGC': 172, 'CCA': 12, 'CCC': 6, 'CCT': 3, 'TCG': 116, 'ATT': 12, 'GCC': 20, 'ACC': 10, 'GCG': 28, 'CTA': 7, 'GCA': 18, 'GTA': 8, 'CCG': 22, 'AAT': 20, 'CAA': 44, 'TCA': 81, 'ATC': 12, 'TAT': 271, 'TCC': 42, 'GCT': 8, 'GTT': 8, 'ATA': 10, 'TTG': 220, 'GAA': 19, 'GTC': 14, 'CGG': 333, 'CTG': 120, 'TAC': 281, 'CGC': 31, 'TTT': 263, 'AAA': 39}, 'ACG': {'AGG': 218, 'GGC': 40, 'TCT': 116, 'CAC': 24, 'TGC': 25, 'CAT': 13, 'TGT': 26, 'GAG': 284, 'TGG': 22, 'AGT': 69, 'TTA': 30, 'AGC': 148, 'GGA': 34, 'GGG': 98, 'TAT': 5, 'GTG': 1303, 'ACA': 5609, 'GAT': 16, 'AAT': 51, 'CAA': 40, 'GGT': 15, 'CTT': 25, 'CTC': 43, 'ACT': 1842, 'AAG': 473, 'AAC': 63, 'CGA': 9, 'AGA': 60, 'CAG': 246, 'GAC': 26, 'CCA': 55, 'CCC': 23, 'CCT': 24, 'TCG': 502, 'ATT': 64, 'GCC': 200, 'ACC': 2733, 'GCG': 861, 'TTC': 16, 'CTA': 24, 'CGT': 6, 'GTA': 131, 'CCG': 109, 'GTT': 98, 'TCA': 165, 'ATC': 71, 'TAC': 11, 'TCC': 119, 'GCT': 137, 'ATG': 2191, 'ATA': 112, 'TTG': 212, 'GAA': 71, 'GTC': 116, 'CGG': 58, 'CTG': 385, 'GCA': 319, 'CGC': 24, 'TTT': 23, 'AAA': 98}, 'AGT': {'AGG': 565, 'GGC': 774, 'TCT': 3274, 'CAC': 221, 'TGC': 180, 'CAT': 694, 'TGT': 886, 'GAG': 244, 'TGG': 25, 'TAC': 36, 'ACG': 191, 'TTA': 14, 'AGC': 25264, 'GGA': 339, 'GGG': 398, 'TTG': 39, 'ACA': 318, 'GAT': 905, 'CGT': 558, 'CAA': 140, 'GTG': 86, 'GGT': 2432, 'CTT': 102, 'CTC': 37, 'ACT': 2423, 'AAG': 446, 'AAC': 1092, 'AGA': 513, 'CAG': 252, 'GAC': 318, 'TCA': 878, 'CCC': 61, 'CCT': 173, 'TCG': 369, 'ATT': 379, 'GCC': 360, 'ACC': 502, 'GCG': 92, 'TTC': 25, 'CTA': 1, 'GTA': 22, 'TCC': 1214, 'AAT': 5166, 'CCA': 37, 'ATC': 80, 'TAT': 158, 'CGA': 64, 'GCT': 1005, 'GTT': 230, 'ATA': 38, 'ATG': 172, 'CCG': 9, 'GAA': 201, 'GTC': 68, 'CGG': 81, 'CTG': 42, 'AAA': 456, 'CGC': 143, 'TTT': 92, 'GCA': 168}, 'TTA': {'AGG': 8, 'TCG': 37, 'GGC': 7, 'TCT': 43, 'CAC': 11, 'TGC': 30, 'CAT': 10, 'TGT': 32, 'GGT': 6, 'GAG': 10, 'TGG': 16, 'ACG': 17, 'AGT': 9, 'AAT': 6, 'AGC': 9, 'GGA': 24, 'GGG': 10, 'TTG': 2411, 'TTC': 165, 'GAT': 5, 'CGT': 2, 'CAA': 38, 'GCC': 27, 'CTT': 339, 'AGA': 25, 'CTC': 615, 'ACT': 13, 'AAG': 23, 'AAC': 8, 'CCG': 9, 'CAG': 36, 'GAC': 2, 'TCA': 343, 'CCC': 7, 'CCT': 1, 'GTG': 85, 'ATT': 50, 'ACA': 103, 'ACC': 29, 'GCG': 19, 'CTA': 1404, 'GTA': 180, 'TCC': 60, 'GTT': 30, 'AAA': 59, 'CCA': 24, 'ATC': 46, 'TAT': 59, 'CGA': 14, 'GCT': 31, 'ATA': 205, 'ATG': 115, 'GAA': 38, 'GTC': 40, 'CGG': 10, 'CTG': 1744, 'TAC': 51, 'CGC': 2, 'TTT': 133, 'GCA': 134}, 'AGC': {'AGG': 831, 'GGC': 5249, 'TCT': 2333, 'CAC': 1042, 'CCA': 51, 'TGC': 1221, 'CAT': 257, 'TGT': 261, 'GAG': 436, 'TGG': 62, 'ACG': 312, 'AGT': 24495, 'TTA': 18, 'GGA': 516, 'ATG': 211, 'TAT': 62, 'GTG': 123, 'ACA': 451, 'GAT': 377, 'GTT': 131, 'CAA': 213, 'GGT': 628, 'CTT': 54, 'CTC': 206, 'ACT': 819, 'AAG': 806, 'AAC': 7593, 'CGA': 87, 'AGA': 836, 'CAG': 504, 'GAC': 1449, 'TTG': 34, 'TTC': 125, 'CCC': 255, 'CCT': 74, 'TCG': 695, 'ATT': 137, 'GCC': 1735, 'ACC': 3560, 'GCG': 159, 'CTA': 20, 'CGT': 165, 'GTA': 37, 'CCG': 35, 'AAT': 1443, 'TCA': 1275, 'ATC': 551, 'TAC': 187, 'TCC': 5595, 'GCT': 483, 'ATA': 46, 'GGG': 515, 'GAA': 308, 'GTC': 406, 'CGG': 137, 'CTG': 75, 'AAA': 791, 'CGC': 964, 'TTT': 43, 'GCA': 251}, 'GGA': {'AGG': 86, 'CGT': 10, 'GGC': 3193, 'TCT': 86, 'CCT': 13, 'GAC': 100, 'CAT': 21, 'TGT': 20, 'GAG': 178, 'TGG': 18, 'TAC': 4, 'ACG': 46, 'AGT': 154, 'TTA': 54, 'AGC': 219, 'ATG': 54, 'GTG': 56, 'ACA': 281, 'GAT': 92, 'GTT': 16, 'CAA': 207, 'GGT': 1882, 'CTT': 5, 'CTC': 7, 'ACT': 53, 'AAG': 187, 'AAC': 233, 'AGA': 463, 'CAG': 152, 'TGC': 18, 'TTG': 21, 'TCA': 343, 'CCC': 18, 'CAC': 35, 'TCG': 53, 'ATT': 11, 'GCC': 114, 'ACC': 51, 'GCG': 125, 'TTC': 6, 'CTA': 14, 'TAT': 21, 'GTA': 78, 'CGA': 77, 'AAT': 218, 'CCA': 68, 'ATC': 16, 'CCG': 13, 'TCC': 78, 'GCT': 94, 'ATA': 62, 'GGG': 5580, 'GAA': 583, 'GTC': 14, 'CGG': 25, 'CTG': 33, 'AAA': 508, 'CGC': 17, 'TTT': 8, 'GCA': 622}, 'GGG': {'AGG': 594, 'CGT': 14, 'GGC': 2777, 'TCT': 61, 'CAC': 40, 'GAC': 102, 'CAT': 29, 'TGT': 14, 'GAG': 683, 'TGG': 111, 'TAC': 3, 'ACG': 127, 'AGT': 159, 'TTA': 13, 'AGC': 253, 'GGA': 4919, 'ATG': 134, 'GTG': 223, 'ACA': 117, 'GAT': 71, 'GTT': 14, 'CAA': 59, 'GGT': 1350, 'CTT': 5, 'CTC': 7, 'ACT': 41, 'AAG': 483, 'AAC': 178, 'AGA': 101, 'CAG': 375, 'TGC': 12, 'CCA': 18, 'CCC': 12, 'CCT': 14, 'TCG': 95, 'ATT': 11, 'GCC': 106, 'ACC': 50, 'GCG': 390, 'TTC': 7, 'CTA': 5, 'TAT': 8, 'GTA': 20, 'TCC': 73, 'AAT': 112, 'TCA': 106, 'ATC': 10, 'CCG': 34, 'CGA': 21, 'GCT': 81, 'ATA': 17, 'TTG': 42, 'GAA': 121, 'GTC': 20, 'CGG': 151, 'CTG': 63, 'GCA': 216, 'CGC': 19, 'TTT': 8, 'AAA': 136}, 'TTG': {'AGG': 32, 'CGT': 1, 'GGC': 5, 'TCT': 82, 'CAC': 16, 'TGC': 46, 'CAT': 12, 'TGT': 57, 'GAG': 60, 'TGG': 181, 'ACG': 106, 'AGT': 13, 'TTA': 2096, 'AGC': 21, 'GGA': 8, 'ATG': 592, 'GTG': 474, 'TTC': 215, 'GAT': 7, 'AAT': 20, 'ACA': 101, 'GGT': 2, 'CTT': 340, 'CTC': 482, 'ACT': 31, 'AAG': 96, 'AAC': 18, 'CGA': 6, 'AGA': 8, 'CAG': 136, 'GAC': 12, 'TCA': 278, 'CCC': 7, 'CCT': 12, 'TCG': 352, 'ATT': 78, 'GCC': 55, 'ACC': 32, 'GCG': 129, 'CTA': 357, 'GCA': 102, 'GTA': 45, 'TCC': 126, 'GTT': 33, 'CAA': 27, 'CCA': 26, 'ATC': 70, 'TAT': 103, 'CCG': 34, 'GCT': 37, 'ATA': 90, 'GGG': 47, 'GAA': 25, 'GTC': 49, 'CGG': 34, 'CTG': 4400, 'TAC': 84, 'CGC': 7, 'TTT': 263, 'AAA': 43}, 'TTC': {'AGG': 16, 'GGC': 45, 'TCT': 62, 'CAC': 227, 'TGC': 136, 'CAT': 50, 'TGT': 46, 'GGT': 17, 'GAG': 11, 'TGG': 121, 'ACG': 16, 'AGT': 11, 'TTA': 138, 'AGC': 46, 'GGA': 8, 'GGG': 9, 'TCG': 20, 'ACA': 23, 'GAT': 6, 'CGT': 9, 'CAA': 26, 'CCT': 11, 'CTT': 65, 'CTC': 431, 'ACT': 21, 'AAG': 21, 'AAC': 67, 'AGA': 15, 'CAG': 37, 'GAC': 13, 'CCA': 7, 'CCC': 71, 'GTG': 81, 'ATT': 41, 'GCC': 232, 'ACC': 110, 'GCG': 23, 'CTA': 29, 'GCA': 19, 'GTA': 21, 'TCC': 343, 'AAT': 22, 'TCA': 37, 'ATC': 179, 'TAT': 125, 'CGA': 8, 'GCT': 35, 'ATG': 166, 'GTT': 28, 'ATA': 22, 'TTG': 226, 'CCG': 4, 'GAA': 15, 'GTC': 227, 'CGG': 13, 'CTG': 181, 'TAC': 535, 'CGC': 34, 'TTT': 3092, 'AAA': 28}, 'GAT': {'AGG': 46, 'TCG': 12, 'GGC': 148, 'TCT': 208, 'CAC': 73, 'GAC': 8495, 'CAT': 325, 'TGT': 64, 'GAG': 1241, 'TGG': 10, 'TAC': 20, 'ACG': 46, 'AGT': 975, 'TTA': 8, 'AGC': 359, 'GGA': 68, 'GGG': 79, 'TTG': 19, 'ACA': 67, 'GTT': 129, 'CAA': 150, 'GGT': 446, 'CTT': 39, 'CTC': 11, 'ACT': 296, 'AAG': 202, 'AAC': 370, 'AGA': 53, 'CAG': 272, 'TGC': 16, 'CCA': 21, 'CCC': 38, 'CCT': 80, 'GTG': 27, 'ATT': 82, 'GCC': 120, 'ACC': 94, 'GCG': 48, 'TTC': 13, 'CTA': 3, 'CGT': 81, 'GTA': 8, 'TCC': 71, 'AAT': 1403, 'TCA': 48, 'ATC': 26, 'TAT': 120, 'CGA': 13, 'GCT': 450, 'ATA': 15, 'ATG': 45, 'CCG': 11, 'GAA': 956, 'GTC': 24, 'CGG': 23, 'CTG': 16, 'GCA': 63, 'CGC': 26, 'TTT': 40, 'AAA': 230}, 'GTT': {'AGG': 18, 'GGC': 39, 'TCT': 183, 'GCC': 215, 'CAC': 25, 'GAC': 17, 'CAT': 55, 'TGT': 101, 'GAG': 49, 'TGG': 10, 'TAC': 12, 'ACG': 94, 'AGT': 142, 'TTA': 34, 'AGC': 77, 'GGA': 13, 'ATG': 191, 'TCG': 12, 'TTC': 32, 'GAT': 109, 'CGT': 20, 'CAA': 26, 'GGG': 23, 'GGT': 93, 'CTT': 383, 'CTC': 117, 'ACT': 951, 'AAG': 31, 'AAC': 45, 'AGA': 13, 'CAG': 38, 'TGC': 31, 'TCA': 34, 'CCC': 21, 'CCT': 93, 'GTG': 3224, 'ATT': 1645, 'ACA': 162, 'ACC': 257, 'GCG': 64, 'CTA': 14, 'GTA': 860, 'CGA': 4, 'AAT': 104, 'CCA': 14, 'ATC': 343, 'TAT': 55, 'TCC': 63, 'GCT': 977, 'ATA': 123, 'TTG': 48, 'CCG': 7, 'GAA': 38, 'GTC': 3498, 'CGG': 4, 'CTG': 95, 'GCA': 106, 'CGC': 9, 'TTT': 198, 'AAA': 31}, 'ACA': {'AGG': 166, 'CGT': 17, 'GGC': 64, 'TCT': 297, 'CCT': 57, 'GAC': 71, 'CAT': 40, 'TGT': 49, 'GAG': 279, 'TGG': 23, 'ACG': 10812, 'AGT': 205, 'TTA': 244, 'AGC': 279, 'GGA': 193, 'GGG': 118, 'TCG': 307, 'TTC': 33, 'GAT': 61, 'GTT': 204, 'CAA': 257, 'GGT': 35, 'CTT': 62, 'CTC': 75, 'ACT': 4562, 'AAG': 313, 'TCC': 288, 'AGA': 428, 'CAG': 240, 'TGC': 48, 'AAC': 143, 'TTG': 267, 'TCA': 1523, 'CCC': 58, 'CAC': 44, 'GTG': 1510, 'ATT': 198, 'GCC': 421, 'ACC': 5801, 'GCG': 533, 'CTA': 179, 'TAT': 22, 'GTA': 1089, 'CCG': 77, 'AAT': 155, 'CCA': 311, 'ATC': 232, 'TAC': 20, 'CGA': 37, 'GCT': 323, 'ATA': 1342, 'ATG': 1925, 'GAA': 441, 'GTC': 220, 'CGG': 34, 'CTG': 385, 'GCA': 2566, 'CGC': 13, 'TTT': 31, 'AAA': 807}, 'GGT': {'AGG': 34, 'TCG': 13, 'GGC': 4198, 'TCT': 152, 'CCT': 49, 'GAC': 119, 'CAT': 155, 'TGT': 158, 'GAG': 95, 'TGG': 10, 'ACG': 20, 'AGT': 1137, 'TTA': 6, 'AGC': 270, 'GGA': 1861, 'ATG': 22, 'TTG': 8, 'ACA': 40, 'GAT': 457, 'CGT': 103, 'CAA': 43, 'CAC': 41, 'CTT': 23, 'CTC': 11, 'ACT': 178, 'AAG': 62, 'AAC': 218, 'AGA': 45, 'CAG': 54, 'TGC': 23, 'CCA': 16, 'CCC': 15, 'GTG': 28, 'ATT': 39, 'GCC': 105, 'ACC': 53, 'GCG': 24, 'TTC': 11, 'CTA': 2, 'GCA': 53, 'GTA': 6, 'TCC': 55, 'AAT': 710, 'TCA': 34, 'ATC': 11, 'TAT': 27, 'CGA': 7, 'GCT': 543, 'GTT': 131, 'ATA': 3, 'GGG': 1919, 'CCG': 1, 'GAA': 73, 'GTC': 24, 'CGG': 19, 'CTG': 12, 'TAC': 12, 'CGC': 21, 'TTT': 37, 'AAA': 85}, 'CTT': {'AGG': 7, 'GGT': 18, 'TCT': 150, 'CCT': 131, 'TGC': 34, 'CAT': 190, 'TGT': 150, 'GAG': 20, 'TGG': 12, 'ACG': 22, 'AGT': 50, 'TTA': 261, 'AGC': 22, 'GGA': 7, 'GGG': 6, 'GGC': 13, 'TCG': 8, 'TTC': 89, 'GAT': 15, 'CGT': 118, 'CAA': 35, 'CAC': 33, 'CTC': 2484, 'ACT': 117, 'AAG': 21, 'AAC': 27, 'CGA': 9, 'AGA': 5, 'CAG': 68, 'GAC': 6, 'TCA': 15, 'CCC': 28, 'GTG': 64, 'ATT': 358, 'GCC': 66, 'ACC': 46, 'GCG': 6, 'CTA': 465, 'GCA': 25, 'GTA': 25, 'TCC': 36, 'AAT': 75, 'ACA': 23, 'CCA': 13, 'ATC': 69, 'TAT': 132, 'CCG': 11, 'GCT': 179, 'ATG': 106, 'GTT': 304, 'ATA': 27, 'TTG': 396, 'GAA': 10, 'GTC': 77, 'CGG': 23, 'CTG': 1931, 'TAC': 39, 'CGC': 24, 'TTT': 386, 'AAA': 23}, 'AGA': {'AGG': 3466, 'GGC': 61, 'TCT': 39, 'CAC': 80, 'TGC': 40, 'CAT': 48, 'TGT': 24, 'GAG': 104, 'TGG': 20, 'TAC': 18, 'ACG': 49, 'AGT': 279, 'TTA': 32, 'AGC': 385, 'GGA': 292, 'GGG': 81, 'TCG': 23, 'ACA': 341, 'GAT': 36, 'CGT': 373, 'CAA': 285, 'GGT': 21, 'CTT': 11, 'CTC': 16, 'ACT': 47, 'AAG': 461, 'AAC': 190, 'CCG': 4, 'CAG': 193, 'GAC': 45, 'TTG': 12, 'TCA': 113, 'CCC': 10, 'CCT': 9, 'GTG': 45, 'ATT': 17, 'GCC': 65, 'ACC': 58, 'GCG': 43, 'TTC': 10, 'CTA': 17, 'GTA': 56, 'CGA': 1679, 'AAT': 167, 'CCA': 26, 'ATC': 23, 'TAT': 34, 'TCC': 37, 'GCT': 47, 'GTT': 17, 'ATA': 88, 'ATG': 57, 'GAA': 223, 'GTC': 13, 'CGG': 827, 'CTG': 30, 'GCA': 175, 'CGC': 625, 'TTT': 16, 'AAA': 1594}, 'CTC': {'AGG': 15, 'CGT': 25, 'GGC': 52, 'TCT': 61, 'CAC': 276, 'TGC': 155, 'CAT': 46, 'TGT': 41, 'GGT': 8, 'GAG': 21, 'TGG': 16, 'ACG': 36, 'AGT': 19, 'TTA': 423, 'AGC': 85, 'GGA': 10, 'TTG': 643, 'GTG': 99, 'TTC': 664, 'GAT': 7, 'GTT': 75, 'CAA': 61, 'GGG': 16, 'CCT': 38, 'CTT': 2844, 'ACT': 62, 'AAG': 33, 'AAC': 82, 'AGA': 8, 'CAG': 137, 'GAC': 32, 'CCA': 25, 'CCC': 162, 'TCG': 17, 'ATT': 115, 'GCC': 306, 'ACC': 224, 'GCG': 42, 'CTA': 681, 'GCA': 33, 'GTA': 31, 'CGA': 16, 'AAT': 22, 'ACA': 38, 'TCA': 25, 'ATC': 520, 'TAT': 52, 'TCC': 201, 'GCT': 78, 'ATA': 40, 'ATG': 128, 'CCG': 7, 'GAA': 27, 'GTC': 506, 'CGG': 21, 'CTG': 3382, 'TAC': 178, 'CGC': 168, 'TTT': 103, 'AAA': 35}, 'ACT': {'AGG': 56, 'GGC': 116, 'TCT': 1501, 'GCC': 546, 'CAC': 68, 'GAC': 106, 'CAT': 141, 'TGT': 195, 'GAG': 109, 'TGG': 6, 'TAC': 26, 'ACG': 3447, 'AGT': 1404, 'TTA': 31, 'AGC': 487, 'GGA': 46, 'GGG': 45, 'TCG': 111, 'TTC': 39, 'GAT': 239, 'CGT': 56, 'CAA': 57, 'GGT': 174, 'CTT': 235, 'CTC': 89, 'AAG': 137, 'AAC': 216, 'CGA': 10, 'AGA': 58, 'CAG': 102, 'TGC': 85, 'CCA': 39, 'CCC': 60, 'CCT': 278, 'GTG': 470, 'ATT': 1114, 'ACA': 4612, 'ACC': 7983, 'GCG': 162, 'CTA': 19, 'GTA': 120, 'CCG': 27, 'AAT': 852, 'TCA': 177, 'ATC': 255, 'TAT': 78, 'TCC': 327, 'GCT': 2210, 'ATG': 553, 'GTT': 1175, 'ATA': 113, 'TTG': 88, 'GAA': 97, 'GTC': 339, 'CGG': 13, 'CTG': 129, 'AAA': 144, 'CGC': 31, 'TTT': 164, 'GCA': 280}, 'AAG': {'AGG': 2926, 'GGC': 213, 'TCT': 144, 'CAC': 375, 'GAC': 317, 'CAT': 256, 'TGT': 67, 'GGT': 71, 'GAG': 1706, 'TGG': 164, 'ACG': 701, 'AGT': 622, 'TTA': 57, 'AGC': 843, 'GGA': 134, 'ATG': 669, 'TCG': 250, 'ACA': 447, 'GAT': 220, 'CGT': 153, 'CAA': 333, 'CCT': 52, 'CTT': 44, 'CTC': 70, 'ACT': 184, 'AAC': 863, 'CGA': 158, 'AGA': 614, 'CAG': 2529, 'TGC': 71, 'TTG': 201, 'TCA': 221, 'CCC': 84, 'GTG': 386, 'ATT': 81, 'GCC': 323, 'ACC': 257, 'GCG': 419, 'TTC': 29, 'CTA': 28, 'TAT': 73, 'GTA': 61, 'TCC': 155, 'AAT': 747, 'CCA': 104, 'ATC': 75, 'TAC': 76, 'CCG': 137, 'GCT': 169, 'GTT': 74, 'ATA': 62, 'GGG': 482, 'GAA': 292, 'GTC': 83, 'CGG': 849, 'CTG': 317, 'AAA': 11212, 'CGC': 472, 'TTT': 37, 'GCA': 355}, 'AAC': {'AGG': 274, 'GGC': 1656, 'TCT': 214, 'CAC': 1443, 'AAA': 904, 'TGC': 260, 'CAT': 269, 'TGT': 81, 'GAG': 583, 'TGG': 26, 'ACG': 140, 'AGT': 814, 'TTA': 20, 'AGC': 5065, 'GGA': 234, 'GGG': 285, 'GTG': 90, 'TTC': 104, 'GAT': 385, 'CGT': 53, 'ACA': 216, 'GGT': 316, 'CTT': 50, 'CTC': 159, 'ACT': 273, 'AAG': 1014, 'AGA': 288, 'CAG': 749, 'GAC': 2038, 'TTG': 34, 'CCA': 39, 'CCC': 177, 'CCT': 56, 'TCG': 61, 'ATT': 63, 'GCC': 824, 'ACC': 1333, 'GCG': 94, 'CTA': 14, 'GTA': 20, 'CGA': 40, 'AAT': 12188, 'CAA': 401, 'TCA': 117, 'ATC': 223, 'TAT': 58, 'TCC': 547, 'GCT': 230, 'GTT': 63, 'ATA': 29, 'ATG': 189, 'CCG': 22, 'GAA': 381, 'GTC': 226, 'CGG': 88, 'CTG': 75, 'TAC': 239, 'CGC': 385, 'TTT': 43, 'GCA': 124}, 'CCG': {'AGG': 19, 'GGC': 11, 'TCT': 37, 'CCT': 716, 'TGC': 6, 'CAT': 10, 'TGT': 3, 'GGT': 5, 'GAG': 112, 'TGG': 34, 'TAC': 4, 'ACG': 69, 'AGT': 12, 'TTA': 7, 'AGC': 17, 'GGA': 10, 'TTG': 46, 'TCG': 163, 'TTC': 7, 'GAT': 7, 'CGT': 4, 'CAA': 33, 'GCC': 46, 'CTT': 10, 'CTC': 12, 'ACT': 21, 'AAG': 80, 'AAC': 10, 'AGA': 9, 'CAG': 332, 'GAC': 17, 'CCA': 1721, 'CCC': 948, 'CAC': 13, 'GTG': 132, 'ATT': 7, 'ACA': 28, 'ACC': 18, 'GCG': 148, 'CTA': 17, 'GTA': 15, 'CGA': 5, 'AAT': 10, 'TCA': 84, 'ATC': 6, 'TAT': 5, 'TCC': 61, 'GCT': 27, 'ATG': 82, 'GTT': 15, 'ATA': 7, 'GGG': 37, 'GAA': 36, 'GTC': 19, 'CGG': 70, 'CTG': 323, 'GCA': 61, 'CGC': 9, 'TTT': 8, 'AAA': 36}, 'CAG': {'AGG': 468, 'GGC': 163, 'TCT': 253, 'CAC': 1756, 'TGC': 191, 'CAT': 1257, 'TGT': 184, 'GGT': 63, 'GAG': 2324, 'TGG': 945, 'ACG': 335, 'AGT': 257, 'TTA': 75, 'AGC': 402, 'GGA': 122, 'ATG': 678, 'GTG': 432, 'ACA': 293, 'GAT': 284, 'CGT': 277, 'CAA': 12691, 'CCT': 143, 'CTT': 132, 'CTC': 201, 'ACT': 127, 'AAG': 1902, 'AAC': 655, 'AGA': 187, 'GAC': 406, 'TTG': 195, 'CCA': 353, 'CCC': 176, 'TCG': 386, 'ATT': 59, 'GCC': 245, 'ACC': 203, 'GCG': 335, 'TTC': 66, 'CTA': 105, 'TAT': 346, 'GTA': 55, 'TCC': 326, 'AAT': 519, 'AAA': 522, 'TCA': 461, 'ATC': 70, 'CCG': 544, 'CGA': 396, 'GCT': 186, 'GTT': 64, 'ATA': 52, 'GGG': 494, 'GAA': 510, 'GTC': 82, 'CGG': 2552, 'CTG': 1343, 'TAC': 430, 'CGC': 585, 'TTT': 73, 'GCA': 317}, 'TGC': {'AGG': 23, 'GGC': 276, 'TCT': 108, 'CAC': 440, 'GAC': 31, 'CAT': 90, 'TGT': 4489, 'GAG': 23, 'TGG': 93, 'ACG': 20, 'AGT': 76, 'TTA': 61, 'AGC': 611, 'GGA': 21, 'ATG': 28, 'TTG': 69, 'TTC': 207, 'GAT': 9, 'CGT': 54, 'ACA': 35, 'GTG': 70, 'GGT': 24, 'CTT': 38, 'CTC': 205, 'ACT': 43, 'AAG': 28, 'AAC': 181, 'AGA': 39, 'CAG': 104, 'CCA': 4, 'CCC': 37, 'CCT': 10, 'TCG': 22, 'ATT': 32, 'GCC': 289, 'ACC': 160, 'GCG': 22, 'CTA': 17, 'GCA': 43, 'GTA': 7, 'TCC': 420, 'AAT': 43, 'CAA': 38, 'TCA': 46, 'ATC': 120, 'TAT': 58, 'CGA': 23, 'GCT': 67, 'GTT': 45, 'ATA': 16, 'GGG': 17, 'CCG': 3, 'GAA': 10, 'GTC': 163, 'CGG': 32, 'CTG': 71, 'TAC': 363, 'CGC': 406, 'TTT': 49, 'AAA': 35}, 'TCA': {'AGG': 38, 'GGC': 57, 'TCT': 5930, 'CCT': 82, 'GAC': 28, 'CAT': 46, 'TGT': 69, 'GGT': 36, 'GAG': 153, 'TGG': 89, 'ACG': 272, 'AGT': 688, 'TTA': 662, 'AGC': 815, 'GGA': 190, 'GGG': 81, 'GTG': 225, 'ACA': 1545, 'GAT': 37, 'AAT': 99, 'CAA': 254, 'CAC': 36, 'CTT': 33, 'CTC': 36, 'ACT': 154, 'AAG': 126, 'AAC': 101, 'CGA': 24, 'AGA': 100, 'CAG': 268, 'TGC': 59, 'TTG': 620, 'TTC': 59, 'CCC': 109, 'TCG': 11359, 'ATT': 22, 'GCC': 318, 'ACC': 192, 'GCG': 339, 'CTA': 74, 'CGT': 7, 'GTA': 156, 'TCC': 7741, 'GTT': 33, 'AAA': 303, 'CCA': 655, 'ATC': 29, 'TAT': 25, 'CCG': 139, 'GCT': 206, 'ATA': 105, 'ATG': 239, 'GAA': 268, 'GTC': 38, 'CGG': 30, 'CTG': 223, 'TAC': 28, 'CGC': 13, 'TTT': 56, 'GCA': 1660}, 'CCC': {'AGG': 7, 'CGT': 26, 'GGC': 111, 'TCT': 172, 'CAC': 207, 'GAC': 115, 'CAT': 44, 'TGT': 29, 'GAG': 78, 'TGG': 8, 'ACG': 25, 'AGT': 52, 'TTA': 13, 'AGC': 235, 'GGA': 18, 'TTG': 15, 'GTG': 68, 'TTC': 114, 'GAT': 39, 'GTT': 48, 'ACA': 46, 'GGT': 19, 'CTT': 61, 'CTC': 287, 'ACT': 60, 'AAG': 51, 'AAC': 140, 'CGA': 10, 'AGA': 11, 'CAG': 124, 'TGC': 76, 'TCA': 82, 'CCT': 3999, 'TCG': 50, 'ATT': 30, 'GCC': 636, 'ACC': 282, 'GCG': 45, 'CTA': 20, 'GCA': 50, 'GTA': 19, 'CCG': 1601, 'AAT': 42, 'CAA': 51, 'CCA': 2226, 'ATC': 99, 'TAT': 27, 'TCC': 856, 'GCT': 114, 'ATG': 36, 'ATA': 11, 'GGG': 19, 'GAA': 60, 'GTC': 190, 'CGG': 18, 'CTG': 91, 'TAC': 56, 'CGC': 116, 'TTT': 30, 'AAA': 55}, 'CCT': {'AGG': 12, 'GGC': 34, 'TCT': 902, 'CAC': 52, 'GAC': 32, 'CAT': 195, 'TGT': 88, 'GAG': 54, 'TGG': 5, 'ACG': 30, 'AGT': 150, 'TTA': 15, 'AGC': 71, 'GGA': 18, 'TTG': 28, 'TCG': 53, 'TTC': 28, 'GAT': 109, 'CGT': 103, 'ACA': 56, 'GGG': 15, 'GGT': 57, 'CTT': 252, 'CTC': 80, 'ACT': 282, 'AAG': 46, 'AAC': 70, 'CGA': 13, 'AGA': 15, 'CAG': 111, 'TGC': 29, 'CCA': 2372, 'CCC': 4565, 'GTG': 65, 'ATT': 137, 'GCC': 142, 'ACC': 75, 'GCG': 38, 'CTA': 26, 'GCA': 96, 'GTA': 23, 'TCC': 194, 'AAT': 142, 'CAA': 57, 'TCA': 87, 'ATC': 31, 'TAT': 51, 'CCG': 1475, 'GCT': 540, 'GTT': 166, 'ATA': 12, 'ATG': 48, 'GAA': 48, 'GTC': 47, 'CGG': 17, 'CTG': 102, 'TAC': 25, 'CGC': 28, 'TTT': 159, 'AAA': 65}, 'GTG': {'AGG': 212, 'GGC': 49, 'TCT': 88, 'CAC': 31, 'GAC': 34, 'CAT': 28, 'TGT': 85, 'GGT': 32, 'GAG': 664, 'TGG': 113, 'ACG': 1564, 'AGT': 77, 'TTA': 138, 'AGC': 87, 'GGA': 76, 'GGG': 342, 'TTC': 60, 'GAT': 28, 'CGT': 16, 'CAA': 63, 'AAT': 51, 'GCC': 453, 'CTT': 92, 'CTC': 116, 'ACT': 333, 'AAG': 355, 'AAC': 65, 'AGA': 61, 'CAG': 377, 'TGC': 67, 'CCA': 133, 'CCC': 55, 'CCT': 51, 'TCG': 249, 'ATT': 526, 'ACA': 1125, 'ACC': 506, 'GCG': 1546, 'CTA': 110, 'GTA': 5845, 'TCC': 112, 'GTT': 3535, 'AAA': 132, 'TCA': 193, 'ATC': 608, 'TAT': 33, 'CGA': 20, 'GCT': 302, 'ATG': 2845, 'ATA': 1034, 'TTG': 722, 'CCG': 102, 'GAA': 132, 'GTC': 3881, 'CGG': 80, 'CTG': 1416, 'TAC': 33, 'CGC': 24, 'TTT': 55, 'GCA': 1038}, 'ATT': {'AGG': 19, 'GGC': 26, 'TCT': 106, 'CCT': 66, 'AAA': 9, 'TGC': 14, 'CAT': 57, 'TGT': 59, 'GGT': 48, 'GAG': 30, 'TGG': 13, 'ACG': 77, 'AGT': 185, 'TTA': 39, 'AGC': 59, 'GGA': 7, 'ATG': 430, 'GTG': 565, 'TTC': 34, 'GAT': 47, 'CGT': 23, 'ACA': 92, 'AAT': 158, 'GGG': 11, 'CAC': 16, 'CTT': 417, 'CTC': 123, 'ACT': 691, 'AAG': 45, 'AAC': 30, 'CGA': 4, 'AGA': 14, 'CAG': 32, 'GAC': 16, 'TCA': 32, 'CCC': 13, 'TCG': 9, 'GCC': 139, 'ACC': 147, 'GCG': 52, 'CTA': 29, 'GTA': 89, 'CCG': 9, 'GTT': 1499, 'CAA': 16, 'CCA': 13, 'ATC': 3958, 'TAT': 50, 'TCC': 31, 'GCT': 492, 'ATA': 970, 'TTG': 125, 'GAA': 21, 'GTC': 355, 'CGG': 5, 'CTG': 198, 'TAC': 22, 'CGC': 10, 'TTT': 201, 'GCA': 55}, 'GCC': {'AGG': 69, 'GGC': 1096, 'TCT': 513, 'CAC': 178, 'GAC': 677, 'CAT': 38, 'TGT': 95, 'GAG': 276, 'TGG': 30, 'TAC': 101, 'ACG': 227, 'AGT': 287, 'TTA': 58, 'AGC': 1626, 'GGA': 118, 'ATG': 373, 'TCG': 170, 'TTC': 266, 'GAT': 136, 'GTT': 315, 'CAA': 70, 'GGT': 153, 'CTT': 110, 'AGA': 59, 'CTC': 460, 'ACT': 577, 'AAG': 155, 'AAC': 856, 'CCG': 48, 'CAG': 212, 'TGC': 362, 'TTG': 111, 'CCA': 77, 'CCC': 508, 'CCT': 120, 'GTG': 582, 'ATT': 209, 'ACA': 356, 'ACC': 3497, 'GCG': 3912, 'CTA': 31, 'CGT': 28, 'GTA': 123, 'TCC': 2419, 'AAT': 215, 'TCA': 270, 'ATC': 1084, 'TAT': 35, 'CGA': 16, 'GCT': 11177, 'ATA': 86, 'GGG': 133, 'GAA': 197, 'GTC': 1960, 'CGG': 24, 'CTG': 237, 'AAA': 138, 'CGC': 96, 'TTT': 69, 'GCA': 5353}, 'ACC': {'AGG': 74, 'GGC': 439, 'TCT': 436, 'GCC': 3222, 'CAC': 268, 'GAC': 362, 'CAT': 60, 'TGT': 88, 'GAG': 174, 'TGG': 18, 'TAC': 101, 'ACG': 4251, 'AGT': 304, 'TTA': 45, 'AGC': 2680, 'GGA': 70, 'TTG': 106, 'TCG': 150, 'TTC': 211, 'GAT': 100, 'AAT': 192, 'CAA': 92, 'GGG': 65, 'GGT': 74, 'CTT': 82, 'CTC': 362, 'ACT': 8833, 'AAG': 182, 'AAC': 1205, 'CGA': 13, 'AGA': 72, 'CAG': 197, 'TGC': 256, 'TCA': 226, 'CCC': 358, 'CCT': 86, 'GTG': 595, 'ATT': 290, 'ACA': 5499, 'GCG': 220, 'CTA': 30, 'CGT': 40, 'GTA': 151, 'TCC': 1927, 'GTT': 372, 'CCA': 49, 'ATC': 1507, 'TAT': 37, 'CCG': 31, 'GCT': 527, 'ATA': 149, 'ATG': 531, 'GAA': 110, 'GTC': 1927, 'CGG': 27, 'CTG': 205, 'GCA': 274, 'CGC': 117, 'TTT': 71, 'AAA': 197}, 'GCG': {'AGG': 95, 'GGC': 52, 'TCT': 100, 'CCT': 21, 'CCA': 54, 'GAC': 35, 'CAT': 8, 'TGT': 27, 'GGT': 20, 'GAG': 571, 'TGG': 33, 'ACG': 726, 'AGT': 48, 'TTA': 24, 'AGC': 83, 'GGA': 49, 'ATG': 725, 'TAT': 5, 'GTG': 1494, 'ACA': 275, 'GAT': 22, 'AAT': 29, 'CAA': 32, 'GGG': 279, 'CAC': 8, 'CTT': 24, 'CTC': 41, 'ACT': 105, 'AAG': 214, 'AAC': 54, 'CGA': 5, 'AGA': 23, 'CAG': 228, 'TGC': 22, 'TTC': 21, 'CCC': 22, 'TCG': 446, 'ATT': 36, 'GCC': 2378, 'ACC': 133, 'CTA': 25, 'CGT': 7, 'GTA': 68, 'CCG': 138, 'GTT': 54, 'TCA': 135, 'ATC': 27, 'TAC': 2, 'TCC': 96, 'GCT': 1659, 'ATA': 62, 'TTG': 186, 'GAA': 85, 'GTC': 44, 'CGG': 44, 'CTG': 298, 'GCA': 3756, 'CGC': 11, 'TTT': 14, 'AAA': 73}, 'CTA': {'AGG': 6, 'GGC': 4, 'TCT': 13, 'CCT': 13, 'TGC': 10, 'CAT': 15, 'TGT': 8, 'GGT': 1, 'GAG': 16, 'GCT': 12, 'ACG': 13, 'AGT': 1, 'TTA': 1001, 'AGC': 6, 'GGA': 16, 'TTG': 264, 'GTG': 44, 'TTC': 22, 'GAT': 3, 'AAT': 4, 'CAA': 160, 'GGG': 6, 'GCC': 19, 'CTT': 503, 'CTC': 756, 'ACT': 17, 'AAG': 11, 'AAC': 7, 'AGA': 16, 'CAG': 47, 'CCA': 100, 'CCC': 14, 'CAC': 9, 'TCG': 9, 'ATT': 30, 'ACA': 95, 'ACC': 16, 'TGG': 3, 'GCG': 15, 'CGT': 4, 'GTA': 135, 'CGA': 32, 'GTT': 18, 'AAA': 44, 'TCA': 42, 'ATC': 28, 'TAT': 14, 'TCC': 13, 'CCG': 10, 'ATA': 181, 'ATG': 54, 'GAA': 30, 'GTC': 22, 'CGG': 12, 'CTG': 1745, 'TAC': 16, 'CGC': 4, 'TTT': 19, 'GCA': 72}, 'GCA': {'AGG': 72, 'GGC': 97, 'TCT': 237, 'GCC': 5621, 'CCT': 69, 'GAC': 70, 'CAT': 24, 'TGT': 49, 'GGT': 63, 'GAG': 460, 'TGG': 16, 'ACG': 446, 'AGT': 148, 'TTA': 262, 'AGC': 205, 'GGA': 554, 'ATG': 829, 'GTG': 1361, 'TTC': 34, 'GAT': 69, 'GTT': 155, 'CAA': 216, 'GGG': 205, 'CAC': 26, 'CTT': 44, 'CTC': 51, 'ACT': 222, 'AAG': 244, 'AAC': 100, 'CGA': 44, 'AGA': 184, 'CAG': 225, 'TGC': 42, 'TCA': 1338, 'CCC': 59, 'TCG': 246, 'ATT': 106, 'ACA': 2360, 'ACC': 271, 'GCG': 7746, 'CTA': 146, 'CGT': 8, 'GTA': 930, 'TCC': 253, 'AAT': 109, 'CCA': 361, 'ATC': 115, 'TAT': 15, 'CCG': 66, 'GCT': 4279, 'ATA': 533, 'TTG': 196, 'GAA': 803, 'GTC': 168, 'CGG': 43, 'CTG': 248, 'TAC': 13, 'CGC': 16, 'TTT': 35, 'AAA': 486}, 'GTA': {'AGG': 18, 'CGT': 1, 'TCG': 18, 'GGT': 6, 'TCT': 26, 'CCT': 13, 'GAC': 6, 'CAT': 6, 'TGT': 13, 'GAG': 42, 'TGG': 8, 'TAC': 5, 'ACG': 101, 'AGT': 18, 'TTA': 215, 'AGC': 23, 'GGA': 87, 'ATG': 200, 'GGC': 11, 'TTG': 66, 'ACA': 753, 'GAT': 9, 'AAT': 15, 'CAA': 53, 'CAC': 8, 'CTT': 35, 'CTC': 36, 'ACT': 90, 'AAG': 37, 'AAC': 15, 'AGA': 58, 'CAG': 43, 'TGC': 15, 'CCA': 50, 'CCC': 15, 'GTG': 3578, 'ATT': 106, 'GCC': 98, 'ACC': 89, 'GCG': 78, 'TTC': 17, 'CTA': 165, 'TAT': 8, 'CGA': 5, 'GTT': 1034, 'TCA': 106, 'ATC': 117, 'CCG': 10, 'TCC': 33, 'GCT': 62, 'ATA': 1140, 'GGG': 17, 'GAA': 186, 'GTC': 1343, 'CGG': 2, 'CTG': 97, 'GCA': 665, 'TTT': 19, 'AAA': 96}, 'CGA': {'AGG': 290, 'GGC': 5, 'TCT': 25, 'CAC': 103, 'TGC': 31, 'CAT': 86, 'TGT': 29, 'GGT': 5, 'GAG': 33, 'TGG': 38, 'ACG': 6, 'AGT': 18, 'TTA': 14, 'AGC': 17, 'GGA': 73, 'ATG': 11, 'TCG': 12, 'TTC': 6, 'GAT': 4, 'CGT': 729, 'CAA': 668, 'GGG': 14, 'GCC': 11, 'CTT': 14, 'CTC': 25, 'ACT': 5, 'AAG': 79, 'AAC': 23, 'AGA': 1199, 'CAG': 277, 'GAC': 5, 'CCA': 52, 'CCC': 12, 'CCT': 8, 'GTG': 16, 'ATT': 1, 'ACA': 27, 'ACC': 6, 'GCG': 9, 'CTA': 38, 'GTA': 12, 'TCC': 23, 'AAT': 20, 'AAA': 224, 'TCA': 46, 'ATC': 1, 'TAT': 24, 'CCG': 9, 'GCT': 8, 'GTT': 9, 'ATA': 7, 'TTG': 14, 'GAA': 77, 'GTC': 4, 'CGG': 1793, 'CTG': 43, 'TAC': 27, 'CGC': 1202, 'TTT': 8, 'GCA': 37}, 'AAT': {'AGG': 225, 'GGC': 456, 'TCT': 373, 'CAC': 312, 'GAC': 442, 'CAT': 1079, 'TGT': 229, 'GGT': 845, 'GAG': 393, 'TGG': 23, 'ACG': 97, 'AGT': 3533, 'TTA': 22, 'AGC': 1068, 'GGA': 179, 'GGG': 214, 'TCG': 33, 'TTC': 27, 'GAT': 1562, 'CGT': 245, 'CAA': 271, 'CCT': 118, 'CTT': 99, 'CTC': 42, 'ACT': 990, 'AAG': 766, 'AAC': 13638, 'AGA': 199, 'CAG': 516, 'TGC': 66, 'TTG': 32, 'CCA': 30, 'CCC': 54, 'GTG': 62, 'ATT': 222, 'GCC': 229, 'ACC': 263, 'GCG': 63, 'CTA': 10, 'GCA': 102, 'GTA': 23, 'CGA': 37, 'GTT': 149, 'ACA': 163, 'TCA': 88, 'ATC': 61, 'TAT': 245, 'TCC': 118, 'GCT': 524, 'ATA': 16, 'ATG': 167, 'CCG': 14, 'GAA': 367, 'GTC': 51, 'CGG': 54, 'CTG': 54, 'TAC': 57, 'CGC': 111, 'TTT': 102, 'AAA': 753}, 'CAA': {'AGG': 68, 'GGC': 47, 'TCT': 108, 'CAC': 687, 'GAC': 137, 'CAT': 560, 'TGT': 53, 'GAG': 220, 'TGG': 71, 'ACG': 37, 'AGT': 95, 'TTA': 65, 'AGC': 108, 'GGA': 175, 'ATG': 78, 'TTG': 40, 'ACA': 214, 'GAT': 114, 'CGT': 117, 'GTG': 59, 'GGT': 25, 'CTT': 60, 'AGA': 192, 'CTC': 78, 'ACT': 36, 'AAG': 181, 'AAC': 223, 'CCG': 50, 'CAG': 8135, 'TGC': 63, 'CCA': 354, 'CCC': 52, 'CCT': 58, 'TCG': 50, 'ATT': 22, 'GCC': 69, 'ACC': 64, 'GCG': 35, 'TTC': 26, 'CTA': 201, 'GTA': 55, 'CGA': 634, 'AAT': 218, 'AAA': 827, 'TCA': 311, 'ATC': 24, 'TAT': 145, 'TCC': 112, 'GCT': 64, 'GTT': 20, 'ATA': 61, 'GGG': 54, 'GAA': 772, 'GTC': 23, 'CGG': 214, 'CTG': 118, 'TAC': 154, 'CGC': 148, 'TTT': 39, 'GCA': 235}, 'CCA': {'AGG': 22, 'GGC': 23, 'TCT': 148, 'CCT': 2359, 'GAC': 38, 'CAT': 31, 'TGT': 18, 'GGT': 15, 'GAG': 163, 'TGG': 23, 'TAC': 9, 'ACG': 49, 'AGT': 38, 'TTA': 76, 'AGC': 30, 'GGA': 80, 'GGG': 40, 'TCG': 121, 'TCC': 152, 'ACA': 349, 'GAT': 32, 'GTT': 35, 'CAA': 400, 'CAC': 39, 'CTT': 37, 'CTC': 44, 'ACT': 64, 'AAG': 119, 'AAC': 30, 'AGA': 41, 'CAG': 267, 'TGC': 7, 'TTC': 12, 'CCC': 2516, 'GTG': 211, 'ATT': 30, 'GCC': 115, 'ACC': 43, 'GCG': 103, 'CTA': 190, 'CGT': 15, 'GTA': 119, 'CCG': 4216, 'AAT': 39, 'TCA': 732, 'ATC': 21, 'TAT': 14, 'CGA': 64, 'GCT': 117, 'ATG': 105, 'ATA': 110, 'TTG': 97, 'GAA': 278, 'GTC': 39, 'CGG': 50, 'CTG': 380, 'AAA': 235, 'CGC': 15, 'TTT': 20, 'GCA': 553}, 'ATC': {'AGG': 31, 'CGT': 6, 'GGC': 99, 'TCT': 45, 'CAC': 71, 'CCA': 10, 'GAC': 48, 'CAT': 23, 'TGT': 22, 'GGT': 13, 'GAG': 44, 'TGG': 16, 'ACG': 83, 'AGT': 34, 'TTA': 50, 'AGC': 297, 'GGA': 15, 'ATG': 507, 'TCG': 20, 'ACA': 89, 'GAT': 16, 'GTT': 356, 'CAA': 20, 'GGG': 10, 'CCT': 19, 'CTT': 116, 'CTC': 696, 'ACT': 142, 'AAG': 45, 'AAC': 146, 'CGA': 4, 'AGA': 18, 'CAG': 49, 'TGC': 81, 'TTC': 205, 'CCC': 73, 'GTG': 684, 'ATT': 3577, 'GCC': 728, 'ACC': 759, 'GCG': 61, 'CTA': 35, 'TAT': 24, 'GTA': 99, 'CCG': 12, 'AAT': 32, 'TCA': 28, 'TAC': 73, 'TCC': 133, 'GCT': 148, 'ATA': 1237, 'TTG': 128, 'GAA': 26, 'GTC': 2003, 'CGG': 8, 'CTG': 261, 'AAA': 29, 'CGC': 32, 'TTT': 51, 'GCA': 64}, 'TAT': {'AGG': 17, 'GGC': 18, 'TCT': 285, 'CCT': 46, 'GAC': 31, 'CAT': 727, 'TGT': 432, 'GAG': 52, 'TGG': 179, 'ACG': 11, 'AGT': 127, 'TTA': 82, 'AGC': 47, 'GGA': 5, 'ATG': 49, 'TCG': 15, 'TTC': 202, 'GAT': 88, 'CGT': 145, 'CAA': 129, 'GGG': 10, 'GGT': 34, 'CTT': 117, 'CTC': 82, 'ACT': 56, 'AAG': 40, 'AAC': 44, 'AGA': 33, 'CAG': 220, 'TGC': 78, 'TCA': 36, 'CCC': 22, 'CAC': 261, 'GTG': 30, 'ATT': 71, 'GCC': 32, 'ACC': 30, 'GCG': 2, 'CTA': 23, 'GCA': 26, 'GTA': 16, 'TCC': 70, 'AAT': 181, 'ACA': 15, 'CCA': 9, 'ATC': 30, 'CCG': 5, 'CGA': 18, 'GCT': 67, 'GTT': 55, 'ATA': 34, 'TTG': 115, 'GAA': 45, 'GTC': 20, 'CGG': 32, 'CTG': 93, 'TAC': 6218, 'CGC': 46, 'TTT': 775, 'AAA': 60}, 'TCC': {'AGG': 50, 'CGT': 30, 'GGC': 441, 'TCT': 18653, 'CAC': 302, 'TGC': 1075, 'CAT': 86, 'TGT': 237, 'GGT': 93, 'GAG': 123, 'TGG': 66, 'ACG': 240, 'AGT': 1628, 'TTA': 104, 'AGC': 5957, 'GGA': 100, 'TTG': 276, 'GTG': 179, 'ACA': 424, 'GAT': 64, 'GTT': 85, 'CAA': 125, 'GGG': 93, 'CCT': 247, 'CTT': 75, 'CTC': 338, 'ACT': 524, 'AAG': 133, 'AAC': 780, 'AGA': 39, 'CAG': 263, 'GAC': 252, 'TCA': 9124, 'CCC': 1182, 'TCG': 6862, 'ATT': 62, 'GCC': 4046, 'ACC': 2767, 'GCG': 269, 'TTC': 883, 'CTA': 20, 'GCA': 370, 'GTA': 34, 'CCG': 118, 'AAT': 210, 'CCA': 143, 'ATC': 193, 'TAT': 97, 'CGA': 17, 'GCT': 580, 'ATA': 30, 'ATG': 143, 'GAA': 99, 'GTC': 376, 'CGG': 39, 'CTG': 198, 'TAC': 386, 'CGC': 146, 'TTT': 179, 'AAA': 117}, 'GCT': {'AGG': 38, 'GGC': 187, 'TCT': 1793, 'CAC': 58, 'CCA': 78, 'TGC': 96, 'CAT': 101, 'TGT': 267, 'GGT': 482, 'GAG': 215, 'TGG': 10, 'TAC': 31, 'ACG': 222, 'AGT': 851, 'TTA': 49, 'AGC': 382, 'GGA': 100, 'GGG': 97, 'GTG': 565, 'ACA': 306, 'GAT': 458, 'GTT': 1476, 'CAA': 72, 'CCT': 434, 'CTT': 299, 'CTC': 116, 'ACT': 2168, 'AAG': 116, 'AAC': 223, 'AGA': 41, 'CAG': 136, 'GAC': 123, 'TTC': 54, 'CCC': 78, 'TCG': 150, 'ATT': 694, 'GCC': 11580, 'ACC': 523, 'GCG': 3311, 'CTA': 23, 'CGT': 65, 'GTA': 104, 'CGA': 7, 'AAT': 567, 'TCA': 230, 'ATC': 233, 'TAT': 81, 'TCC': 385, 'CCG': 50, 'ATG': 334, 'ATA': 91, 'TTG': 95, 'GAA': 146, 'GTC': 331, 'CGG': 18, 'CTG': 136, 'AAA': 140, 'CGC': 39, 'TTT': 219, 'GCA': 5282}, 'ATA': {'AGG': 24, 'GGC': 15, 'TAC': 9, 'CAC': 8, 'TGC': 7, 'CAT': 11, 'TGT': 14, 'GGT': 2, 'GAG': 38, 'TGG': 9, 'ACG': 125, 'AGT': 15, 'TTA': 225, 'AGC': 21, 'TCT': 18, 'GGA': 44, 'TTG': 118, 'TCG': 13, 'TTC': 20, 'GAT': 11, 'AAT': 22, 'CAA': 38, 'GGG': 13, 'CCT': 9, 'CTT': 51, 'CTC': 61, 'ACT': 55, 'AAG': 53, 'AAC': 14, 'AGA': 84, 'CAG': 47, 'GAC': 5, 'CCA': 51, 'CCC': 3, 'GTG': 769, 'ATT': 1082, 'GCC': 86, 'ACC': 59, 'GCG': 69, 'CTA': 229, 'CGT': 2, 'GTA': 986, 'TCC': 23, 'GTT': 111, 'ACA': 632, 'TCA': 86, 'ATC': 1513, 'TAT': 19, 'CGA': 12, 'GCT': 66, 'CCG': 10, 'ATG': 689, 'GAA': 75, 'GTC': 193, 'CGG': 11, 'CTG': 280, 'GCA': 360, 'CGC': 6, 'TTT': 36, 'AAA': 120}, 'ATG': {'AGG': 331, 'GGC': 38, 'TCT': 98, 'CAC': 45, 'CCA': 60, 'TGC': 71, 'CAT': 64, 'TGT': 57, 'GAG': 270, 'TGG': 94, 'ACG': 1441, 'AGT': 131, 'TTA': 179, 'AGC': 158, 'GGA': 52, 'GGG': 182, 'TCG': 224, 'TCC': 116, 'ACA': 1248, 'GAT': 36, 'AAT': 162, 'CAA': 104, 'GGT': 20, 'CTT': 114, 'CTC': 197, 'ACT': 225, 'AAG': 441, 'AAC': 118, 'AGA': 89, 'CAG': 491, 'GAC': 38, 'TTC': 140, 'CCC': 31, 'CCT': 24, 'GTG': 2343, 'ATT': 400, 'GCC': 313, 'ACC': 322, 'GCG': 785, 'CTA': 175, 'CGT': 13, 'GTA': 263, 'CGA': 16, 'GTT': 164, 'AAA': 119, 'TCA': 198, 'ATC': 394, 'TAT': 61, 'CCG': 90, 'GCT': 212, 'ATA': 831, 'TTG': 824, 'GAA': 60, 'GTC': 178, 'CGG': 47, 'CTG': 1631, 'TAC': 53, 'CGC': 19, 'TTT': 185, 'GCA': 634}, 'GAA': {'AGG': 107, 'GGC': 125, 'TCT': 114, 'CAC': 190, 'GAC': 1541, 'CAT': 145, 'TGT': 21, 'GGT': 72, 'GAG': 11442, 'TGG': 27, 'TAC': 54, 'ACG': 97, 'AGT': 246, 'TTA': 119, 'AGC': 329, 'GGA': 591, 'GGG': 147, 'TCG': 52, 'TCC': 118, 'ACA': 477, 'GAT': 1264, 'CGT': 34, 'CAA': 970, 'CCT': 64, 'CTT': 30, 'CTC': 31, 'ACT': 128, 'AAG': 315, 'AAC': 479, 'AGA': 383, 'CAG': 559, 'TGC': 24, 'CCA': 193, 'CCC': 69, 'GTG': 148, 'ATT': 44, 'GCC': 257, 'ACC': 129, 'GCG': 120, 'TTC': 18, 'CTA': 58, 'GTA': 204, 'CCG': 42, 'AAT': 451, 'TCA': 360, 'ATC': 42, 'TAT': 68, 'CGA': 106, 'GCT': 167, 'ATG': 121, 'GTT': 59, 'ATA': 135, 'TTG': 78, 'GTC': 66, 'CGG': 52, 'CTG': 89, 'GCA': 824, 'CGC': 52, 'TTT': 33, 'AAA': 1237}, 'GTC': {'AGG': 22, 'TCG': 29, 'GGC': 174, 'TCT': 78, 'CAC': 54, 'GAC': 130, 'CAT': 18, 'TGT': 46, 'GGT': 18, 'GAG': 61, 'TGG': 8, 'ACG': 124, 'AGT': 49, 'TTA': 23, 'AGC': 274, 'GGA': 21, 'GGG': 22, 'TTG': 49, 'TTC': 192, 'GAT': 17, 'CGT': 16, 'ACA': 157, 'AAT': 42, 'CCT': 40, 'CTT': 86, 'CTC': 569, 'ACT': 244, 'AAG': 54, 'AAC': 168, 'AGA': 14, 'CAG': 52, 'TGC': 147, 'TCA': 45, 'CCC': 102, 'GTG': 3946, 'ATT': 403, 'GCC': 1291, 'ACC': 1297, 'GCG': 85, 'CTA': 27, 'TAT': 23, 'GTA': 1054, 'CGA': 6, 'GTT': 3689, 'CAA': 24, 'CCA': 24, 'ATC': 2364, 'TAC': 62, 'TCC': 225, 'GCT': 210, 'ATA': 147, 'ATG': 203, 'CCG': 6, 'GAA': 45, 'CGG': 10, 'CTG': 133, 'AAA': 52, 'CGC': 53, 'TTT': 56, 'GCA': 118}, 'CGG': {'AGG': 1722, 'GGT': 11, 'TCT': 36, 'GCC': 27, 'CAC': 165, 'TGC': 55, 'CAT': 129, 'TGT': 37, 'GAG': 136, 'TGG': 340, 'ACG': 13, 'AGT': 36, 'TTA': 11, 'AGC': 55, 'GGA': 21, 'GGG': 129, 'GGC': 23, 'TCG': 56, 'TTC': 14, 'GAT': 10, 'CGT': 938, 'CAA': 202, 'CCT': 20, 'CTT': 25, 'CTC': 26, 'ACT': 15, 'AAG': 400, 'AAC': 62, 'AGA': 545, 'CAG': 1775, 'GAC': 14, 'TCA': 51, 'CCC': 15, 'GTG': 64, 'ATT': 9, 'ACA': 17, 'ACC': 7, 'GCG': 53, 'CTA': 10, 'GCA': 29, 'GTA': 7, 'CGA': 1950, 'AAT': 33, 'GCT': 9, 'CCA': 38, 'ATC': 4, 'TAT': 40, 'TCC': 42, 'CCG': 54, 'ATG': 26, 'GTT': 3, 'ATA': 3, 'TTG': 32, 'GAA': 36, 'GTC': 7, 'CTG': 198, 'TAC': 45, 'CGC': 1949, 'TTT': 9, 'AAA': 129}, 'CTG': {'AGG': 63, 'GGC': 25, 'TCT': 91, 'CAC': 68, 'TGC': 79, 'CAT': 60, 'TGT': 74, 'GGT': 15, 'GAG': 219, 'TGG': 139, 'ACG': 320, 'AGT': 28, 'TTA': 1497, 'AGC': 39, 'GGA': 29, 'GGG': 128, 'TCG': 131, 'TTC': 142, 'GAT': 17, 'CGT': 27, 'ACA': 261, 'TAT': 72, 'CTT': 2674, 'CTC': 3816, 'ACT': 125, 'AAG': 247, 'AAC': 42, 'AGA': 25, 'CAG': 1131, 'GAC': 21, 'TCA': 104, 'CCC': 76, 'CCT': 42, 'GTG': 1077, 'ATT': 161, 'GCC': 152, 'ACC': 138, 'GCG': 404, 'CTA': 3706, 'GCA': 249, 'GTA': 115, 'TCC': 113, 'AAT': 45, 'CAA': 153, 'CCA': 179, 'ATC': 175, 'CCG': 241, 'CGA': 44, 'GCT': 130, 'ATG': 1437, 'GTT': 100, 'ATA': 207, 'TTG': 5881, 'GAA': 71, 'GTC': 108, 'CGG': 268, 'TAC': 88, 'CGC': 53, 'TTT': 154, 'AAA': 89}, 'TAC': {'AGG': 31, 'GGC': 62, 'TCT': 87, 'CAC': 1043, 'GAC': 104, 'CAT': 187, 'TGT': 109, 'GGT': 12, 'GAG': 62, 'TGG': 271, 'ACG': 7, 'AGT': 37, 'TTA': 120, 'AGC': 179, 'GGA': 4, 'GGG': 13, 'TCG': 24, 'TTC': 947, 'GAT': 21, 'CGT': 34, 'CAA': 150, 'AAT': 52, 'GCC': 121, 'CTT': 45, 'CTC': 230, 'ACT': 27, 'AAG': 78, 'AAC': 224, 'AGA': 28, 'CAG': 307, 'TGC': 402, 'TTG': 152, 'CCA': 11, 'CCC': 64, 'CCT': 9, 'GTG': 51, 'ATT': 28, 'ACA': 26, 'ACC': 98, 'GCG': 18, 'CTA': 35, 'GTA': 12, 'CGA': 18, 'GTT': 15, 'TCA': 24, 'ATC': 108, 'TAT': 5376, 'TCC': 351, 'GCT': 35, 'ATA': 26, 'ATG': 94, 'CCG': 7, 'GAA': 53, 'GTC': 84, 'CGG': 22, 'CTG': 149, 'AAA': 76, 'CGC': 201, 'TTT': 245, 'GCA': 17}, 'CGC': {'AGG': 404, 'TCG': 16, 'GGC': 219, 'TCT': 64, 'CAC': 1502, 'TGC': 605, 'CAT': 232, 'TGT': 93, 'GAG': 59, 'TGG': 29, 'ACG': 9, 'AGT': 63, 'TTA': 12, 'AGC': 456, 'GGA': 10, 'ATG': 17, 'TTG': 11, 'TTC': 69, 'GAT': 20, 'CGT': 2943, 'CAA': 222, 'GGT': 28, 'CTT': 34, 'CTC': 243, 'ACT': 28, 'AAG': 165, 'AAC': 280, 'AGA': 447, 'CAG': 380, 'GAC': 73, 'CCA': 18, 'CCC': 93, 'CCT': 16, 'GTG': 20, 'ATT': 17, 'GCC': 123, 'ACC': 106, 'GCG': 20, 'CTA': 16, 'TAT': 54, 'GTA': 5, 'CGA': 1245, 'AAT': 67, 'ACA': 11, 'GCA': 18, 'TCA': 23, 'ATC': 51, 'CCG': 19, 'TCC': 178, 'GCT': 40, 'GTT': 12, 'ATA': 3, 'GGG': 23, 'GAA': 34, 'GTC': 62, 'CGG': 1485, 'CTG': 48, 'TAC': 258, 'TTT': 12, 'AAA': 160}, 'TTT': {'AGG': 4, 'GGT': 21, 'TCT': 315, 'CAC': 89, 'CCA': 11, 'TGC': 51, 'CAT': 150, 'TGT': 142, 'GAG': 14, 'TGG': 119, 'ACG': 16, 'AGT': 51, 'TTA': 130, 'AGC': 30, 'GGA': 6, 'ATG': 175, 'GGC': 8, 'TCG': 22, 'ACA': 22, 'GAT': 17, 'CGT': 29, 'CAA': 28, 'GGG': 13, 'CCT': 62, 'CTT': 342, 'CTC': 98, 'ACT': 96, 'AAG': 27, 'AAC': 16, 'CGA': 2, 'AGA': 10, 'CAG': 45, 'GAC': 8, 'TTC': 3557, 'CCC': 16, 'GTG': 64, 'ATT': 141, 'GCC': 55, 'ACC': 32, 'GCG': 15, 'CTA': 24, 'GTA': 17, 'CCG': 4, 'AAT': 47, 'AAA': 15, 'TCA': 35, 'ATC': 46, 'TAT': 504, 'TCC': 75, 'GCT': 142, 'GTT': 185, 'ATA': 29, 'TTG': 235, 'GAA': 13, 'GTC': 51, 'CGG': 5, 'CTG': 158, 'TAC': 163, 'CGC': 13, 'GCA': 24}, 'AAA': {'AGG': 663, 'GGC': 144, 'TCT': 158, 'CAC': 313, 'GAC': 288, 'CAT': 260, 'TGT': 57, 'GGT': 103, 'GAG': 418, 'TGG': 42, 'ACG': 174, 'AGT': 556, 'TTA': 117, 'AGC': 795, 'GGA': 429, 'TTG': 86, 'TCG': 82, 'ACA': 994, 'GAT': 258, 'CGT': 143, 'CAA': 1336, 'GGG': 151, 'CCT': 50, 'CTT': 43, 'CTC': 45, 'ACT': 173, 'AAG': 12654, 'AAC': 908, 'AGA': 2609, 'CAG': 816, 'TGC': 67, 'CCA': 254, 'CCC': 72, 'GTG': 185, 'ATT': 76, 'GCC': 239, 'ACC': 234, 'GCG': 163, 'TTC': 30, 'CTA': 87, 'GTA': 167, 'CGA': 395, 'AAT': 815, 'TCA': 427, 'ATC': 82, 'TAT': 84, 'TCC': 146, 'GCT': 167, 'GTT': 69, 'ATA': 236, 'ATG': 160, 'CCG': 72, 'GAA': 1369, 'GTC': 76, 'CGG': 317, 'CTG': 116, 'TAC': 83, 'CGC': 277, 'TTT': 47, 'GCA': 611}}



#data = codon_change
data = {}
#data = [v for v in codon_change.values() if 100 in v.values()]


#THRESHOLDING
for (key, value) in codon_change.items(): #DICT
    data[key] = {}
    
    for (key2, value2) in codon_change[key].items(): #NESTED DICT
        if codon_change[key][key2] >= 0:
            data[key][key2] =  codon_change[key][key2]
        #print(key, value)
        #data[key] = ""
        
    if data[key] == {}: #nothing was added.
        del data[key]
        #pop it
        #data[key] = value
    



#data[key]
num_data = 0 
#Count of total TH change:
for k in data:
    #print(k)
    for j in data[k]:
        #print(codon_change[k][j])
        num_data += data[k][j]
print("\tTotal number of TH codon changes, after applying Codon to Codon threshold filter:", num_data)


#print(data)

#for (key, value) in codon_change.item():
#    if codon_change[key]

#sys.exit(1)

df1 = pd.DataFrame.from_dict(data)
#convert_fill(df1)
#df1.replace("", 0, inplace=True)
df1.fillna("-", inplace=True)
df1.to_csv(output_filename, sep="\t")








num_codon_change = 0 
#Count of total TH change:
for k in codon_change:
    #print(k)
    for j in codon_change[k]:
        #print(codon_change[k][j])
        num_codon_change += codon_change[k][j]
        
print("\tTotal number of TH codon changes:", num_codon_change)

change_sum = 0

for item in change_types:
    change_sum += change_types[item]


for item in change_types:
    print("\t", item, change_types[item], *[round((change_types[item]/change_sum)*100,2), "%"])


#print(sum(total_TH))







