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

DIR = "/Users/user/Documents/TH_REVISIONS/BUSTEDS-Selectome/selectome_4_11_19/data"
MH_DIR = "/Users/user/Documents/TH_REVISIONS/analysis/UNMASKED_SELECTOME/UNMASKED_SELECTOME_2/BUSTEDS-MH"

OUTPUT_CSV = "processed_BUSTEDS-MH_vs_BUSTEDS_with_dnds.csv"

# =============================================================================
# Helper functions
# =============================================================================

def read_json(filename):
    filesize = os.stat(filename).st_size
    print("\t # Reading:", "(filesize =", filesize, ")", filename)
    if filesize == 0: 
        #print("## Exiting")
        return 9999991, 1
    
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    p_value = json_data["test results"]["p-value"]
    dNdS = json_data["fits"]["MG94xREV with separate rates for branch sets"]["Rate Distributions"]["non-synonymous/synonymous rate ratio for *test*"]
    
    print("\t\tBaseline model (BUSTEDS) p-value =", p_value)
    print("\t\tBaseline model (BUSTEDS) dNdS =", dNdS[0][0])
    
    return p_value, dNdS[0][0]
#end method

def read_json_MH(filename_MH):
    filesize_MH = os.stat(filename_MH).st_size
    print("\t # Reading:", "(filesize =", filesize_MH, ")", filename_MH)
    if filesize_MH == 0: return 9999990, 0
    
    with open(filename_MH, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    p_value = json_data["test results"]["p-value"]
    dNdS = json_data["fits"]["MG94xREV with separate rates for branch sets"]["Rate Distributions"]["non-synonymous/synonymous rate ratio for *test*"]
    
    print("\t\tNovel model (BUSTEDS-MH) p-value =", p_value)
    print("\t\tNovel model (BUSTEDS-MH) dNdS =", dNdS[0][0])
    
    return p_value, dNdS[0][0]
#end method

def process(filename_MH, filename):
    global OUTPUT_CSV
    p_value_BUSTEDS, dnds_BUSTEDS = read_json(filename)
    p_value_BUSTEDS_MH, dnds_BUSTEDSMH = read_json_MH(filename_MH)

    #Calculate aBSREL-MH minus aBSREL
    #delta_cAIC = float(cAIC_aBSREL_MH) - float(cAIC_aBSREL)
    #print("\t### RESULT", delta_cAIC)
    delta_p_value = float(p_value_BUSTEDS_MH) - float(p_value_BUSTEDS)
    
    #Check for errors
    if p_value_BUSTEDS == 9999991 or p_value_BUSTEDS_MH == 9999990: 
        print("### EXITING, FILE ERROR")
        #sys.exit(1)
        return 1
    
    #delta dNdS
    delta_dNdS = float(dnds_BUSTEDSMH) - float(dnds_BUSTEDS)
    
    #Output to csv
    with open(OUTPUT_CSV, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)  
        spamwriter.writerow([filename_MH.split("/")[-1].replace(".BUSTEDS-MH.json", ""), str(p_value_BUSTEDS_MH), str(p_value_BUSTEDS), str(delta_p_value), str(dnds_BUSTEDS), str(dnds_BUSTEDSMH), str(delta_dNdS)])
    csvfile.close()
    #end with

#end method

# =============================================================================
# Main subroutine
# =============================================================================

print("# Inititialize ")

print("# Saving output to:", OUTPUT_CSV)

#Empty out the output CSV
with open(OUTPUT_CSV, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["Filename", "pvalue_BUSTEDSMH", "pvalue_BUSTEDS", "delta_for_p-value", "BUSTEDS-dNdS", "BUSTEDSMH-dNdS", "delta_dNdS"])
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
BUSTEDS_tag = ".BUSTED-SRV.json"
BUSTEDSMH_tag = ".BUSTEDS-MH.json"

for n, file in enumerate(BUSTEDS_MH_DIR_FILES):
    
    print("# Searching for match for:", file.split("/")[-1])
    
    NEXUS_FILENAME = file.split("/")[-1].replace(BUSTEDSMH_tag, "")
    
    BUSTEDS_VERSION = os.path.join(DIR, NEXUS_FILENAME) + BUSTEDS_tag
    
    print("\t", n+1, "Checking for BUSTED output for:", BUSTEDS_VERSION.split("/")[-1])
    
    # Does it match with a file in aBSREL_DIR?, if soo..
    
    if BUSTEDS_VERSION in BUSTEDS_DIR_FILES:
        # process
        print("\t", "Match Found!")
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
     "Test":{
         "0":{
           "omega":0.01007421713990577,
           "proportion":0.8708564955693479
          },
         "1":{
           "omega":0.2739584278783274,
           "proportion":0.1286368019414106
          },
         "2":{
           "omega":1,
           "proportion":0.0005067024892415948
          }


    "Rate Distributions":{
       "non-synonymous/synonymous rate ratio for *test*":        [
[0.04834499742457001, 1] 
        ]

"""