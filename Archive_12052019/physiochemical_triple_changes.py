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
import json, csv, sys, os, time
import pandas as pd
import numpy as np
from prettytable import PrettyTable
start_time = time.time()

# =============================================================================
# Declares
# =============================================================================
codon_change = {}
pvalue_threshold = 0.005
file_passed_threshold = 0
num_ER_thresholded_sites = 0
THRESHOLD_TH_VALUE = 3
#path = "/Users/user/Documents/Pond Lab/Triple hits/Analysis/selectome_trip_ammended_analysis"
path = r"E:\SELECTOME_TRIP_AMMENDED_SRV\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"
#path = r"E:\BUSTED_SIM_SRV_FITTER_JSON\BUSTED_SIM_SRV_FITTER_JSON"

files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(".json")]
#files = ["/Users/user/Documents/Pond Lab/Triple hits/Analysis/selectome_trip_ammended_analysis/ENSGT00670000097768.Euteleostomi.003.nex.FITTER.json"]

# =============================================================================
# Codons
# =============================================================================
#https://www.khanacademy.org/science/biology/gene-expression-central-dogma/central-dogma-transcription/a/the-genetic-code-discovery-and-properties
#http://www.geneinfinity.org/sp/sp_aaprops.html
#http://www.inf.fu-berlin.de/lehre/WS14/ProteomicsWS14/LUS/lu1d/201/objects/il_1600_mob_1043762/aa_properties.png

GLYCINE_CODONS = ["GGT", "GGC", "GGA", "GGG"] #Nonpolar, aliphatic R Groups
ALANINE_CODONS = ["GCT", "GCC", "GCA", "GCG"]
VALINE_CODONS = ["GTT", "GTC", "GTA", "GTG"]
LEUCINE_CODONS = ["CTT", "CTC", "CTA", "CTG", "TTA", "TTG"]
METHIONINE_CODONS = ["ATG"]
ISOLEUCINE_CODONS = ["ATT", "ATC", "ATA"]

PHENYLALANINE_CODONS = ["TTT", "TTC"] #Polar, uncharged R Groups
TYROSINE_CODONS = ["TAT", "TAC"]
TRYPTOPHAN_CODONS = ["TGG"]

SERINE_CODONS = ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"] #Aromatic R Groups
THREONINE_CODONS = ["ACT", "ACC", "ACA", "ACG"]
CYSTEINE_CODONS = ["TGT", "TGC"]
PROLINE_CODONS = ["CCT", "CCC", "CCA", "CCG"]
ASPARAGINE_CODONS = ["AAT", "AAC"] #Asn
GLUTAMINE_CODONS = ["CAA", "CAG"] #Gln

LYSINE_CODONS = ["AAA", "AAG"] #Positively charged R Groups
ARGININE_CODONS = ["CGT", "CGC", "CGA", "CGG"] #Arg
HISTIDINE_CODONS = ["CAT", "CAC"]

ASPARTATE_CODONS = ["GAT", "GAC"] #Negattively charged R Groups, #Asp
GLUTAMATE_CODONS = ["GAA", "GAG"] #Glu

STOP_CODONS = ["TAA", "TAG", "TGA"]
# =============================================================================
# Codons dict
# =============================================================================
Universal_codon_table = {"Glycine": ["GGT", "GGC", "GGA", "GGG"], 
                         "Alanine": ["GCT", "GCC", "GCA", "GCG"],
                         "Valine": ["GTT", "GTC", "GTA", "GTG"],
                         "Leucine": ["CTT", "CTC", "CTA", "CTG", "TTA", "TTG"],
                         "Methionine": ["ATG"],
                         "Isoleucine":  ["ATT", "ATC", "ATA"],
                         "Phenylalanine": ["TTT", "TTC"] ,
                         "Tyrosine": ["TAT", "TAC"],
                         "Tryptophan": ["TGG"],
                         "Serine": ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"],
                         "Threonine": ["ACT", "ACC", "ACA", "ACG"],
                         "Cysteine": ["TGT", "TGC"],
                         "Proline": ["CCT", "CCC", "CCA", "CCG"],
                         "Asparagine": ["AAT", "AAC"],
                         "Glutamine":  ["CAA", "CAG"], 
                         "Lysine": ["AAA", "AAG"],
                         "Arginine": ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"], 
                         "Histidine": ["CAT", "CAC"],
                         "Aspartate": ["GAT", "GAC"], 
                         "Glutamate": ["GAA", "GAG"],
                         "Stop":  ["TAA", "TAG", "TGA"]}

#(1) Nonpolar, aliphatic R (nonpolar and hydrophobic)
#(2) Polar, Uncharged R
#(3) aromatic R
#(4) Positively charged R 
#(5) Negatively charged R


"""
1-1 - Glycine, Alanine, Valine, Leucine, Methionine, Isoleucine
1-2
1-3
1-4
1-5

2-1 Serine, Threonine, Cysteine, Proline, Asparagine, Glutamine
2-2
2-3
2-4
2-5

3-1 Phenylalanine, Tyrosine, Tryptophan
3-2
3-3
3-4
3-5

4-1 Lysine, Arginine, Histidine
4-2
4-3
4-4
4-5

5-1 Aspartate, Glutamate
5-2
5-3
5-4
5-5


"""
physiochemical_change = {"Nonpolar": Universal_codon_table["Glycine"] + Universal_codon_table["Alanine"] + Universal_codon_table["Valine"] +Universal_codon_table["Leucine"] + Universal_codon_table["Methionine"] + Universal_codon_table["Isoleucine"],
                         "Polar": Universal_codon_table["Serine"] + Universal_codon_table["Threonine"] + Universal_codon_table["Cysteine"] + Universal_codon_table["Proline"] +  Universal_codon_table["Asparagine"] + Universal_codon_table["Glutamine"],
                         "Aromatic": Universal_codon_table["Phenylalanine"] + Universal_codon_table["Tyrosine"] + Universal_codon_table["Tryptophan"],
                         "Positive":  Universal_codon_table["Lysine"] +  Universal_codon_table["Arginine"] +   Universal_codon_table["Histidine"],
                         "Negative": Universal_codon_table["Aspartate"] + Universal_codon_table["Glutamate"]}


#one dict with the codons
#another to keep count.
#Amino_Acids = ["Glycine", "Alanine", "Valine", "Leucine", "Methionine", "Isoleucine", "Phenylalanine", "Tyrosine", "Tryptophan", "Serine", "Threonine",
#               "Cysteine", "Proline", "Asparagine", "Glutamine", "Lysine", "Arginine", "Histidine", "Aspartate", "Glutamate"]
    
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
    global codon_change, file_passed_threshold, num_ER_thresholded_sites, THRESHOLD_TH_VALUE
    this_row = []
    with open(filename, "r") as fh:
        json_data = json.load(fh)
        THvsDH_LRT_pvalue = json_data["test results"]["Triple-hit vs double-hit"]["p-value"]
        EvidenceRatio_TH = json_data["Evidence Ratios"]["Three-hit"][0]
        Site_subs = json_data["Site substitutions"]
        #Filtering
        if float(THvsDH_LRT_pvalue) >= pvalue_threshold: return #P VALUE THRESHOLDs
        Threshold_TH = THRESHOLD_TH_VALUE * np.mean(EvidenceRatio_TH)
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

def check_triple_changes(codon_from, codon_to):
    global Universal_codon_table
    for k in Universal_codon_table:
        #print(k, Universal_codon_table[k])
        #print(Universal_codon_table[codon_from])
        if codon_from in Universal_codon_table[k] and codon_to in Universal_codon_table[k]:
            #print(1)
            #print(k, Universal_codon_table[k], codon_from, codon_to)
            #triple_change_count[k] += 1
            return k, 1
    return "NA", 0

def check_physiochemical_change():
    pass

#https://www.khanacademy.org/science/biology/gene-expression-central-dogma/central-dogma-transcription/a/the-genetic-code-discovery-and-properties
# =============================================================================
# Main subroutine
# =============================================================================
def main_sub(output_filename, mode):
    global SERINE_CODONS, Universal_codon_table, physiochemical_change
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
    triple_change_count = {}
    
    #physiochemical_change = {}
    #Nonpolar, aliphatic R (nonpolar and hydrophobic) - Glycine
    #Polar, Uncharged R
    #aromatic R
    #Positively charged R 
    #Negatively charged R
    
    #for AA in Universal_codon_table:    
    #    triple_change_count[AA] = 0
    physiochemical_change_count_initial = {}
    physiochemical_change_count_end = {} 
    physiochemical_change_count_transition = {}
    
    physiochemical_change_count_transition["Nonpolar->Nonpolar"] = 0
    physiochemical_change_count_transition["Nonpolar->Polar"] = 0
    physiochemical_change_count_transition["Nonpolar->Aromatic"] = 0
    physiochemical_change_count_transition["Nonpolar->Positive"] = 0
    physiochemical_change_count_transition["Nonpolar->Negative"] = 0
    
    physiochemical_change_count_transition["Polar->Nonpolar"] = 0
    physiochemical_change_count_transition["Polar->Polar"] = 0
    physiochemical_change_count_transition["Polar->Aromatic"] = 0
    physiochemical_change_count_transition["Polar->Positive"] = 0
    physiochemical_change_count_transition["Polar->Negative"] = 0
    
    physiochemical_change_count_transition["Aromatic->Nonpolar"] = 0
    physiochemical_change_count_transition["Aromatic->Polar"] = 0
    physiochemical_change_count_transition["Aromatic->Aromatic"] = 0
    physiochemical_change_count_transition["Aromatic->Positive"] = 0
    physiochemical_change_count_transition["Aromatic->Negative"] = 0
    
    physiochemical_change_count_transition["Positive->Nonpolar"] = 0
    physiochemical_change_count_transition["Positive->Polar"] = 0
    physiochemical_change_count_transition["Positive->Aromatic"] = 0
    physiochemical_change_count_transition["Positive->Positive"] = 0
    physiochemical_change_count_transition["Positive->Negative"] = 0
    
    physiochemical_change_count_transition["Negative->Nonpolar"] = 0
    physiochemical_change_count_transition["Negative->Polar"] = 0
    physiochemical_change_count_transition["Negative->Aromatic"] = 0
    physiochemical_change_count_transition["Negative->Positive"] = 0
    physiochemical_change_count_transition["Negative->Negative"] = 0
    
    #Nonpolar- Glycine, Alanine, Valine, Leucine, Methionine, Isoleucine
    #Polar - Serine, Threonine, Cysteine, Proline, Asparagine, Glutamine
    #Aromatic - Phenylalanine, Tyrosine, Tryptophan
    #Positive - Lysine, Arginine, Histidine
    #Negative
    
    for key in physiochemical_change:    
        physiochemical_change_count_initial[key] = 0
        physiochemical_change_count_end[key] = 0
    
    
    """ This is on triple instant. changes"""
    for key in codon_change:
        #print(key, codon_change[key])
        for second_key in codon_change[key]: #can write out this matrix
            #if diff_count(key, second_key) == 3:
            
            #print(key, second_key)
            triple_changes += codon_change[key][second_key] #This is really a count for Codons.
            if key in SERINE_CODONS and second_key in SERINE_CODONS: SERINE_to_SERINE += codon_change[key][second_key]
            #triple_change_count[key] += triple_changes(key, second_key, triple_change_count) #This looks at Amino acid level changes.
            
            #AA, value = check_triple_changes(key, second_key)
            #if value != 0: triple_change_count[AA] += codon_change[key][second_key]
            
            #Physiochemical
            #Nonpolar, aliphatic R (nonpolar and hydrophobic) - Glycine
            #Polar, Uncharged R
            #aromatic R
            #Positively charged R 
            #Negatively charged R
            
            #^ how many?
            #physiochemical_change_count["Nonpolar"] = 0
            #physiochemical_change_count["Polar"] = 0
            #physiochemical_change_count["Aromatic"] = 0
            #physiochemical_change_count["Positive"] = 0
            #physiochemical_change_count["Negative"] = 0
            #physiochemical_change["Nonpolar"]
            PC_from, PC_to = "", ""
            
            for k in physiochemical_change:
                #PC_from, PC_to = "", ""
                #How many nonpolars do we have?
                if key in physiochemical_change[k]:
                     physiochemical_change_count_initial[k] += codon_change[key][second_key]
                     PC_from = str(k)
                     
                #what do they become?
                if second_key in physiochemical_change[k]:
                     physiochemical_change_count_end[k] += codon_change[key][second_key]
                     PC_to = str(k)
                     
                #Links aka changes
                #Take the 1st codon: key
                #what is its physiochemical group?
                #print(PC_from, PC_to)
                
                
                
            try:
                physiochemical_change_count_transition[PC_from + "->" + PC_to] += codon_change[key][second_key]
            except:
                #k is the key in physiochemical_change
                #key is codon from
                #second_key is codon to
                #PC_from should hold the key in physiochemical_change for codon from (key)
                
                print("(ERROR)", k, key, second_key, PC_from, "->", PC_to, physiochemical_change[k])
                
                
                
                
                #print(k, physiochemical_change_count_initial[k], PC_from, PC_to)
                """
                if PC_from != "" and PC_to != "":
                    try:
                        physiochemical_change_count_transition[PC_from+"->"+PC_to] += codon_change[key][second_key]
                    except: 
                        print("ERROR:", [PC_from], [PC_to], [PC_from+"->"+PC_to])
                """
                #if key in physiochemical_change[k] and second_key in physiochemical_change[k]:
                #    physiochemical_change_count[k] += codon_change[key][second_key]
                
            
            
        
    print("Number of files:", file_passed_threshold)
    if mode == "FULLFILTER": print("Number of ER Thresholded Sites:", num_ER_thresholded_sites)
    print("Total number of triple changes observed:", triple_changes)
    print("TH: Serine to Serine changes:", SERINE_to_SERINE)
    #for k in triple_change_count: print(k, triple_change_count[k])

    
    #Physiochemical
    print("Initial:")
    for k in physiochemical_change_count_initial: print(k, physiochemical_change_count_initial[k])
    
    print("End:")
    for k in physiochemical_change_count_end: print(k, physiochemical_change_count_end[k])

    print()
    print("Transitions:")
    for k in physiochemical_change_count_transition: 
        if physiochemical_change_count_transition[k] == 0: continue
        print(k.split("->")[0]+"_start", "["+str(physiochemical_change_count_transition[k])+"]", k.split("->")[1]+"_finish")
        #print(k, physiochemical_change_count_transition[k])
    
# =============================================================================
# Main main
# =============================================================================
"""
print("(1) No filter analysis") 
main_sub("", "NOFILTER")
print("Elapsed time was %g seconds" % (time.time() - start_time))

codon_change, file_passed_threshold, num_ER_thresholded_sites = {}, 0 , 0
print("\n", "(2) p < 0.005") 
main_sub("", "P_FILTER")
print("Elapsed time was %g seconds" % (time.time() - start_time))
"""


codon_change, file_passed_threshold, num_ER_thresholded_sites = {}, 0 , 0
print("\n", "(3) p < 0.005, TH Threshold (3x)") 
main_sub("", "FULLFILTER")
print("Elapsed time was %g seconds" % (time.time() - start_time))

codon_change, file_passed_threshold, num_ER_thresholded_sites = {}, 0 , 0
THRESHOLD_TH_VALUE = 10
print("\n", "(4) p < 0.005, TH Threshold (10x)") #REMEMBER TO CHANGE THE THRESHOLD IN THE FUNCTION
main_sub("", "FULLFILTER")

print("Elapsed time was %g seconds" % (time.time() - start_time))


"""
Make a Sankey: http://sankeymatic.com/build/

"""

# =============================================================================
# End of file
# =============================================================================


#df1 = pd.DataFrame.from_dict(codon_change)
#df1.fillna("-", inplace=True)
#df1.to_csv("TEST_ORIGINAL_sample_circos_data_TripleHit_SELECTOME_SRV.txt", sep="\t")





