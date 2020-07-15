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


aBSREL_DIR = "/Users/user/Documents/TH_REVISIONS/analysis/UNMASKED_SELECTOME/UNMASKED_SELECTOME/ABSREL"
aBSREL_MH_DIR = "/Users/user/Documents/TH_REVISIONS/analysis/UNMASKED_SELECTOME/UNMASKED_SELECTOME/ABSREL-MH"

OUTPUT_CSV = "processed_aBSREL_vs_aBSREL-MH.csv"

# =============================================================================
# Helper functions
# =============================================================================

def read_json_aBSREL(filename_aBSREL):
    print("\t# Reading:", filename_aBSREL)
    
    if os.stat(filename_aBSREL).st_size == 0: return 9999991 
    with open(filename_aBSREL, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    cAIC = json_data["fits"]["Full adaptive model"]["AIC-c"]
    
    print("\t\tBaseline model (aBSREL) cAIC =", cAIC)
    return cAIC
#end method

def read_json_aBSREL_MH(filename_aBSREL_MH):
    print("\t# Reading:", filename_aBSREL_MH)
    
    if os.stat(filename_aBSREL_MH).st_size == 0: return 9999990
    
    
    with open(filename_aBSREL_MH, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    cAIC = json_data["fits"]["Full adaptive model"]["AIC-c"]
    
    print("\t\tNovel model (aBSREL-MH) cAIC =", cAIC)
    
    return cAIC
#end method

def process(filename_aBSREL_MH, filename_aBSREL):
    global OUTPUT_CSV
    cAIC_aBSREL = read_json_aBSREL(filename_aBSREL)
    cAIC_aBSREL_MH = read_json_aBSREL_MH(filename_aBSREL_MH)

    #Calculate aBSREL-MH minus aBSREL
    delta_cAIC = float(cAIC_aBSREL_MH) - float(cAIC_aBSREL)
    print("\t### RESULT", delta_cAIC)
    
    #Check for errors
    if cAIC_aBSREL_MH == 9999990 or cAIC_aBSREL == 9999991: return 1
    
    
    #Output to csv
    with open(OUTPUT_CSV, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([filename_aBSREL_MH.split("/")[-1].replace(".ABSREL-MH.json", ""), str(delta_cAIC)])
    csvfile.close()
#end with

#end method

#def calculate_delta():
#    cAIC_aBSREL = read_json_aBSREL(filename_aBSREL_MH, filename_aBSREL)


# =============================================================================
# Main subroutine
# =============================================================================

print("# Init ")

print("# Saving output to:", OUTPUT_CSV)
#Empty out the output CSV
with open(OUTPUT_CSV, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["Filename", "delta_cAIC"])
csvfile.close()
#end with
    
print("# Processing ", aBSREL_DIR)
print("# Processing ", aBSREL_MH_DIR)
aBSREL_DIR_FILES = [os.path.join(aBSREL_DIR, file.name) for file in os.scandir(aBSREL_DIR) if file.name.endswith(".json")]
aBSREL_MH_DIR_FILES = [os.path.join(aBSREL_MH_DIR, file.name) for file in os.scandir(aBSREL_MH_DIR) if file.name.endswith(".json")]


print("# Number of aBSREL results:", len(aBSREL_DIR_FILES))
print("# Number of aBSREL-MH results:", len(aBSREL_MH_DIR_FILES))

# Loop over files in aBSREL-MH_DIR
matches_count = 0
for n, file in enumerate(aBSREL_MH_DIR_FILES):
    print("# Searching for match for:", file.split("/")[-1])
    NEXUS_FILENAME = file.split("/")[-1].replace(".ABSREL-MH.json", "")
    #print(n, "# Checking for BUSTED output for:", NEXUS_FILENAME)
    
    ABSREL_VERSION = os.path.join(aBSREL_DIR, NEXUS_FILENAME) + ".ABSREL.json"
    print("\t", n, "Checking for aBSREL output for:", ABSREL_VERSION.split("/")[-1])
    # Does it match with a file in aBSREL_DIR?, if soo..
    if ABSREL_VERSION in aBSREL_DIR_FILES:
        # process
        matches_count += 1
        process(file, ABSREL_VERSION)
        
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
