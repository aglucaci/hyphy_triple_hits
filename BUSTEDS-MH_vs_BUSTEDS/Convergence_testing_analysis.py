#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 08:48:43 2020

@author: Alexander Lucaci
"""
# =============================================================================
# Imports
# =============================================================================
import pandas as pd
import os
import json
from os import listdir
from os.path import isfile, join

# =============================================================================
# Declares
# =============================================================================
# ENSGT00660000095461.Euteleostomi.002.nex

# BUSTEDS-MH with no --starting-points (LL)
# BUSTEDS , --starting-points 10 (LL)

# BUSTEDS-MH with --starting-points 10 (LL) (range)
# BUSTEDS-MH with --starting-points 25 (LL) (range)

# Unmasked Selectome
#DIR = "/Users/user/Documents/TH_REVISIONS/analysis/BUSTEDS-Selectome/selectome_4_11_19/BUSTED_12_runs"
#MH_DIR = "/Users/user/Documents/TH_REVISIONS/analysis/BUSTED_on_UNMASKED_SELECTOME_07272020"
#OUTPUT_CSV = "processed_paired_analysis_Unmasked_Selectome_BUSTEDS-MH_vs_BUSTEDS.csv"

# Input CSV (with BUSTEDS-MH (no sp), and BUSTEDS results)
INPUT_CSV = "/Users/user/Documents/TH_REVISIONS/scripts/BUSTEDS-MH_vs_BUSTEDS/processed_paired_analysis_Unmasked_Selectome_BUSTEDS-MH_vs_BUSTEDS.csv"

#Convergence testing dir 
CONVERGENCE_DIR = "/Users/user/Documents/BUSTEDS-MH_Convergence_testing"

# =============================================================================
# Subroutine
# =============================================================================
#Lets look at: ENSGT00440000038881.Euteleostomi.001.nex
#filename = "ENSGT00440000038881.Euteleostomi.001.nex"
#filename = "ENSGT00660000095461.Euteleostomi.002.nex"
#filename = "ENSGT00390000008221.Euteleostomi.001.nex" # aka the worst
#filename = "ENSGT00390000002684.Euteleostomi.001.nex"

onlyfiles = [f for f in listdir(CONVERGENCE_DIR) if isfile(join(CONVERGENCE_DIR, f))]

print(onlyfiles)

def main(filename):
    global INPUT_CSV
    print("\n# Analyzing:", filename)
    #tag_pair = [["MH_Unconstrained_log_L", "BASE_Unconstrained_log_L"]]
    df = pd.read_csv(INPUT_CSV)
    for index, row in df.iterrows():
        nexus_filename = str(df["Filename"][index]).replace(".BUSTEDS-MH.json", "")
        if nexus_filename == filename:
            BUSTEDS_MH_no_sp_LL = float(df["MH_Unconstrained_log_L"][index])
            BUSTEDS_sp10_LL = df["BASE_Unconstrained_log_L"][index]
            print("# BUSTEDS_MH_no_sp_LL:", df["MH_Unconstrained_log_L"][index])
            print("# BUSTEDS_sp10_LL:",df["BASE_Unconstrained_log_L"][index])
            delta = BUSTEDS_MH_no_sp_LL - BUSTEDS_sp10_LL
            print("# delta ll:", delta)
            
            #Loop through analysis
            #We need the sp_10 (runs 1-10)
            #We need the sp_25 (runs 1-10)
            
            # Grab the following
            # MH_Unconstrained_cAIC = json_data["fits"]["Unconstrained model"]["AIC-c"]
            # MH_Unconstrained_log_L = json_data["fits"]["Unconstrained model"]["Log Likelihood"]
            
            #sp 10, spy25
            tag = ["sp10", "sp25"]
            for t in tag:
                print("##", t)
                MH_Unconstrained_log_L_dict = {}
                
                for n in range(1, 11):
                    pass
                    #ENSGT00390000002684.Euteleostomi.001.nex_1_sp10.BUSTEDS-MH.json    
                    search_for_file = CONVERGENCE_DIR + "/analysis/" + nexus_filename + "_" + str(n) + "_" + t + ".BUSTEDS-MH.json"
                    #print("# Searching for:", search_for_file.split("/")[-1])
                    #if os.path.exists(my_path) and os.path.getsize(my_path) > 0:
                    if os.path.exists(search_for_file) and os.path.getsize(search_for_file) > 0:
                        #print("\t", "File exists and is not empty")
                        # Grab LL data
                        with open(search_for_file, "r") as fh:
                            json_data = json.load(fh)
                        fh.close()
                        
                        MH_Unconstrained_log_L = json_data["fits"]["Unconstrained model"]["Log Likelihood"]
                        print(MH_Unconstrained_log_L)
                        #MH_Unconstrained_log_L_dict
                    #end if
                #end for
                print()
            #end for
                    
            """        
            print()
            #sp 25
            MH_Unconstrained_log_L_dict = {}
            for n in range(1, 11):
                pass
                #ENSGT00390000002684.Euteleostomi.001.nex_1_sp10.BUSTEDS-MH.json    
                search_for_file = CONVERGENCE_DIR + "/analysis/" + nexus_filename + "_" + str(n) + "_sp25.BUSTEDS-MH.json"
                print("# Searching for:", search_for_file.split("/")[-1])
                #if os.path.exists(my_path) and os.path.getsize(my_path) > 0:
                if os.path.exists(search_for_file) and os.path.getsize(search_for_file) > 0:
                    #print("\t", "File exists and is not empty")
                    # Grab LL data
                    with open(search_for_file, "r") as fh:
                        json_data = json.load(fh)
                    fh.close()
                    
                    MH_Unconstrained_log_L = json_data["fits"]["Unconstrained model"]["Log Likelihood"]
                    print(MH_Unconstrained_log_L)
                    #MH_Unconstrained_log_L_dict
                #end inner if
            #end inner if
            """
            
            
        #end outer if
    #end outer for
    
    print("# #####################") 
#end method

# =============================================================================
# Loader
# =============================================================================

onlyfiles = [f for f in listdir(CONVERGENCE_DIR) if isfile(join(CONVERGENCE_DIR, f))]

for file in onlyfiles:
    if ".nex" not in file: continue
    main(file)

# =============================================================================
# End of file 
# =============================================================================
