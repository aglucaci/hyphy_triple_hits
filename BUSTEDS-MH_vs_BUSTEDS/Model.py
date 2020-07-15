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

DIR = "/Users/user/Documents/TH_REVISIONS/analysis/UNMASKED_SELECTOME/UNMASKED_SELECTOME/BUSTEDS"
MH_DIR = "/Users/user/Documents/TH_REVISIONS/analysis/UNMASKED_SELECTOME/UNMASKED_SELECTOME/BUSTEDS-MH"

OUTPUT_CSV = "processed_BUSTEDS-MH_vs_BUSTEDS.csv"

# =============================================================================
# Helper functions
# =============================================================================

def read_json(filename):
    print("\t# Reading:", filename)
    
    if os.stat(filename).st_size == 0: return 9999991 
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    p_value = json_data["test results"]["p-value"]
    
    print("\t\tBaseline model (BUSTEDS) p-value =", p_value)
    return p_value
#end method

def read_json_MH(filename_MH):
    print("\t# Reading:", filename_MH)
    
    if os.stat(filename_MH).st_size == 0: return 9999990
    
    
    with open(filename_MH, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    p_value = json_data["test results"]["p-value"]
    
    print("\t\tNovel model (BUSTEDS-MH) p-value =", p_value)
    
    return p_value
#end method

def process(filename_MH, filename):
    global OUTPUT_CSV
    p_value_BUSTEDS = read_json(filename)
    p_value_BUSTEDS_MH = read_json_MH(filename_MH)

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
        
        spamwriter.writerow([filename_MH.split("/")[-1].replace(".BUSTEDS.json", ""), str(p_value_BUSTEDS_MH), str(p_value_BUSTEDS), str(delta_p_value)])
    csvfile.close()
    #end with

#end method

# =============================================================================
# Main subroutine
# =============================================================================

print("# Init ")

print("# Saving output to:", OUTPUT_CSV)

#Empty out the output CSV
with open(OUTPUT_CSV, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["Filename", "pvalue_BUSTEDSMH", "pvalue_BUSTEDS", "delta"])
csvfile.close()
#end with
    
print("# Processing ", DIR)
print("# Processing ", MH_DIR)
BUSTEDS_DIR_FILES = [os.path.join(DIR, file.name) for file in os.scandir(DIR) if file.name.endswith(".json")]
BUSTEDS_MH_DIR_FILES = [os.path.join(MH_DIR, file.name) for file in os.scandir(MH_DIR) if file.name.endswith(".json")]


print("# Number of BUSTEDS results:", len(BUSTEDS_DIR_FILES))
print("# Number of BUSTEDS-MH results:", len(BUSTEDS_MH_DIR_FILES))

# Loop over files in aBSREL-MH_DIR
matches_count = 0
for n, file in enumerate(BUSTEDS_MH_DIR_FILES):
    print("# Searching for match for:", file.split("/")[-1])
    NEXUS_FILENAME = file.split("/")[-1].replace(".BUSTEDS.json", "")
    
    BUSTEDS_VERSION = os.path.join(DIR, NEXUS_FILENAME) + ".BUSTED.json"
    print("\t", n, "Checking for BUSTED output for:", BUSTEDS_VERSION.split("/")[-1])
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
