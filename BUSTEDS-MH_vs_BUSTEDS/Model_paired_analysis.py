#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 19:49:17 2020

@author: Alexander G. Lucaci
"""

# =============================================================================
# Imports
# =============================================================================
import os
import sys
import json
import csv

# =============================================================================
# Declares
# =============================================================================
# Empirical 11-datasets
DIR = "/Users/user/Documents/TH_REVISIONS/analysis/13-datasets"
MH_DIR = DIR
OUTPUT_CSV = "PROCESSED_paired_analysis_BUSTEDS-MH_vs_BUSTEDS_13datasets.csv"

# Empirical 11-datasets
#DIR = "/Users/user/Documents/EmpiricalDatasets/11-datasets"
#MH_DIR = "/Users/user/Documents/EmpiricalDatasets/11-datasets"
#OUTPUT_CSV = "processed_paired_analysis_BUSTEDS-MH_vs_BUSTEDS.csv"

# Unmasked Selectome
#DIR = "/Users/user/Documents/TH_REVISIONS/analysis/BUSTEDS-Selectome/selectome_4_11_19/BUSTED_12_runs"
#MH_DIR = "/Users/user/Documents/TH_REVISIONS/analysis/BUSTED_on_UNMASKED_SELECTOME_07272020"
#OUTPUT_CSV = "processed_paired_analysis_Unmasked_Selectome_BUSTEDS-MH_vs_BUSTEDS.csv"


# =============================================================================
# Helper functions
# =============================================================================

def read_json(filename):
    print("\t # Reading:", filename)
    
    if os.stat(filename).st_size == 0: return 9999991 
    
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    p_value = json_data["test results"]["p-value"]
    BASE_Unconstrained_cAIC = json_data["fits"]["Unconstrained model"]["AIC-c"]
    BASE_Unconstrained_log_L = json_data["fits"]["Unconstrained model"]["Log Likelihood"]
    
    print("\t\tBaseline model (BUSTEDS) p-value =", p_value)
    print("\t\tBaseline model (BUSTEDS) Unconstrained cAIC =", BASE_Unconstrained_cAIC)
    print("\t\tBaseline model (BUSTEDS) Unconstrained logL =", BASE_Unconstrained_log_L)
    return p_value, BASE_Unconstrained_cAIC, BASE_Unconstrained_log_L
#end method


def read_json_MH(filename_MH):
    print("\t # Reading:", filename_MH)
    
    if os.stat(filename_MH).st_size == 0: return 9999990
    
    
    with open(filename_MH, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    # Part 1 - MG94 with double and triple instantaneous substitutions"
    p_value = json_data["test results"]["p-value"]
    MH_cAIC = json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["AIC-c"]
    MH_log_L = json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Log Likelihood"]
    MH_dNdS = json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["non-synonymous/synonymous rate ratio for *test*"]
    MH_DH_rate = json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["rate at which 2 nucleotides are changed instantly within a single codon"]
    MH_TH_rate = json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["rate at which 3 nucleotides are changed instantly within a single codon"]
    MH_TH_SI_rate = json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["rate at which 3 nucleotides are changed instantly within a single codon between synonymous codon islands"]
    
    # Part 2 - "Unconstrained model"
    MH_Unconstrained_cAIC = json_data["fits"]["Unconstrained model"]["AIC-c"]
    MH_Unconstrained_log_L = json_data["fits"]["Unconstrained model"]["Log Likelihood"]
    #UN_SRV_0 = json_data["fits"]["Unconstrained model"]["Rate Distributions"]["Synonymous site-to-site rates"]
    #UN_SRV_1 = json_data["fits"]["Unconstrained model"]["Rate Distributions"]["Synonymous site-to-site rates"]
    #UN_SRV_2 = json_data["fits"]["Unconstrained model"]["Rate Distributions"]["Synonymous site-to-site rates"]
    MH_Unconstrained_DH_rate = json_data["fits"]["Unconstrained model"]["rate at which 2 nucleotides are changed instantly within a single codon"]
    MH_Unconstrained_TH_rate = json_data["fits"]["Unconstrained model"]["rate at which 3 nucleotides are changed instantly within a single codon"]
    MH_Unconstrained_TH_SI_rate = json_data["fits"]["Unconstrained model"]["rate at which 3 nucleotides are changed instantly within a single codon between synonymous codon islands"]
    
    #Report on what we found.
    print("\t\tNovel model (BUSTEDS-MH) p-value =", p_value)
    print("\t\tNovel model (BUSTEDS-MH) cAIC =", MH_Unconstrained_cAIC)
    print("\t\tNovel model (BUSTEDS-MH) logL =", MH_Unconstrained_log_L)
    
    return p_value, MH_cAIC, MH_log_L, MH_dNdS, MH_DH_rate, MH_TH_rate, MH_TH_SI_rate, MH_Unconstrained_cAIC, MH_Unconstrained_log_L, MH_Unconstrained_DH_rate, \
                MH_Unconstrained_TH_rate, \
                MH_Unconstrained_TH_SI_rate
#end method

def process(filename_MH, filename):
    global OUTPUT_CSV
    p_value_BUSTEDS, BASE_Unconstrained_cAIC, BASE_Unconstrained_log_L = read_json(filename)
    p_value_BUSTEDS_MH, MH_MG94_cAIC, MH_MG94_log_L, MH_MG94_dNdS, MH_MG94_DH_rate, MH_MG94_TH_rate, MH_MG94_TH_SI_rate, MH_Unconstrained_cAIC, MH_Unconstrained_log_L, MH_Unconstrained_DH_rate, \
                MH_Unconstrained_TH_rate, \
                MH_Unconstrained_TH_SI_rate  = read_json_MH(filename_MH)

    #Calculate aBSREL-MH minus aBSREL
    #delta_cAIC = float(cAIC_aBSREL_MH) - float(cAIC_aBSREL)
    #print("\t### RESULT", delta_cAIC)
    delta_p_value = float(p_value_BUSTEDS_MH) - float(p_value_BUSTEDS)
    
    #Check for errors
    if p_value_BUSTEDS == 9999990 or p_value_BUSTEDS_MH == 9999991: return 1
    
    #Output to csv
    with open(OUTPUT_CSV, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        spamwriter.writerow([filename_MH.split("/")[-1].replace(".BUSTEDS.json", ""), str(p_value_BUSTEDS_MH), str(p_value_BUSTEDS), str(delta_p_value),
                             BASE_Unconstrained_cAIC, BASE_Unconstrained_log_L, \
                             MH_MG94_cAIC, MH_MG94_log_L, \
                                 MH_MG94_dNdS, MH_MG94_DH_rate, MH_MG94_TH_rate, MH_MG94_TH_SI_rate, \
                                 MH_Unconstrained_cAIC, MH_Unconstrained_log_L, \
                                     MH_Unconstrained_DH_rate, \
                                     MH_Unconstrained_TH_rate, \
                                     MH_Unconstrained_TH_SI_rate
                             ])
    csvfile.close()
    #end with

#end method

# =============================================================================
# Main subroutine
# =============================================================================

#SMH_tag = ".BUSTEDS-MH.json"
#S_tag = ".BUSTEDS.json"

print("# Init ")
print("# Program is in:", os.getcwd())

print("# Saving output to:", OUTPUT_CSV)

#Empty out the output CSV
with open(OUTPUT_CSV, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["Filename", "pvalue_BUSTEDSMH", "pvalue_BUSTEDS", "delta p-values", \
                         "BASE_Unconstrained_cAIC", "BASE_Unconstrained_log_L",
                         "MH_MG94x(2+3)_cAIC", "MH_MG94x(2+3)_log_L", "MH_MG94x(2+3)_dNdS", "MH_MG94x(2+3)_DH_rate", "MH_MG94x(2+3)_TH_rate", "MH_MG94x(2+3)_TH_SI_rate", \
                         "MH_Unconstrained_cAIC", "MH_Unconstrained_log_L", \
                         "MH_Unconstrained_DH_rate", "MH_Unconstrained_TH_rate", "MH_Unconstrained_TH_SI_rate"])
csvfile.close()
#end with
    
print("# Processing ", DIR)
print("# Processing ", MH_DIR)
#BUSTEDS_DIR_FILES = [os.path.join(DIR, file.name) for file in os.scandir(DIR) if file.name.endswith(".BUSTEDS.json")]
#BUSTEDS_MH_DIR_FILES = [os.path.join(MH_DIR, file.name) for file in os.scandir(MH_DIR) if file.name.endswith(".BUSTEDS-MH.json")]

BASE_tag = ""
MH_tag = ""

BUSTEDS_DIR_FILES = [os.path.join(DIR, file.name) for file in os.scandir(DIR) if file.name.endswith(".BUSTEDS.json")]
BUSTEDS_MH_DIR_FILES = [os.path.join(MH_DIR, file.name) for file in os.scandir(MH_DIR) if file.name.endswith(".BUSTEDS-MH.json")]

print("# Number of BUSTEDS results:", len(BUSTEDS_DIR_FILES))
print("# Number of BUSTEDS-MH results:", len(BUSTEDS_MH_DIR_FILES))

# Loop over files in aBSREL-MH_DIR
matches_count = 0
for n, file in enumerate(BUSTEDS_MH_DIR_FILES):
    print("# Searching for match for:", file.split("/")[-1])
    NEXUS_FILENAME = file.split("/")[-1].replace(".BUSTEDS-MH.json", "")
    
    BUSTEDS_VERSION = os.path.join(DIR, NEXUS_FILENAME) + ".BUSTEDS.json"
    print("\t", n, "Checking for BUSTEDS output for:", BUSTEDS_VERSION.split("/")[-1])
    # Does it match with a file in aBSREL_DIR?, if soo..
    if BUSTEDS_VERSION in BUSTEDS_DIR_FILES:
        # process
        matches_count += 1
        process(file, BUSTEDS_VERSION)
    else:
        # dont process, but record this.
        pass
    # end if
    print()
#end for

print("# Number of matches:", matches_count)
             




# =============================================================================
# End of file
# =============================================================================
"""
Notes:\
    
    Models:
    
    ### Fitting MG94 with double and triple instantaneous substitutions (MH)
    ### Performing the full (dN/dS > 1 allowed) branch-site model fit (BUSTED-SMH model)
    ### Performing the constrained (dN/dS > 1 not allowed) model fit (Negative or Neutral evolution)
    

    Question: 2H and 3H rates are accounted for by suitable rate variation?
    
    Interpretation: My understanding is that you want lower AIC.
                    and a higher logL
    
"""