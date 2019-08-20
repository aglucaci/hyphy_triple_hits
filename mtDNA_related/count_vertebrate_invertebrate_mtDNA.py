#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 13:10:46 2019

@author: alexander

counts number of files which belong to Vertebrate or Invertbrate mtDNA

also copies the FITTER.json to a new folder 

Vertebrate_mtDNA_FITTERS
or
Invertebrate_mtDNA_FITTERS

"""

# =============================================================================
# Imports
# =============================================================================
import glob, os

# =============================================================================
# Declares
# =============================================================================
vertebrate_mtdna = "usefulOddsandEnds/vertebratefolders.txt"
invertebrate_mtdna = "usefulOddsandEnds/invertebratefolders.txt"


vertebrate_mtdna_files = [] #loaded from file above
invertebrate_mtdna_files = []

vertebrate_mtdna_files_count = 0
invertebrate_mtdna_files_count = 0

FITTERS = "updatedAnalysis_mtDNA_combined(FASTA_AND_FITTERS)/"

def load_folders(filename, mode):
    global vertebrate_mtdna_files, invertebrate_mtdna_files
    with open(filename, "r") as f:
        for n, line in enumerate(f):
            data = line.split("/")[1].strip().replace(".fas", "")
            #print(n, data)
            if mode == "Vertebrate": vertebrate_mtdna_files.append(data)
            if mode == "Invertebrate": invertebrate_mtdna_files.append(data)
            
        f.close()
        
    if mode == "Vertebrate": print("\tLoaded Vertebrate mtDNA files")
    if mode == "Invertebrate": print("\tLoaded Invertebrate mtDNA files")
    return 0

def search_fitter_folder(directory):
    global vertebrate_mtdna_files, invertebrate_mtdna_files
    vertebrate_mtdna_files_count = 0
    invertebrate_mtdna_files_count = 0
    os.chdir(directory)
    for file in glob.glob("*.FITTER.json"):
        parsed_filename = file.replace(".fa.FITTER.json", "")
        if parsed_filename in vertebrate_mtdna_files:
            #print(vertebrate_mtdna_files_count, file)
            vertebrate_mtdna_files_count += 1
        elif parsed_filename in invertebrate_mtdna_files:
            #print(vertebrate_mtdna_files_count, file)
            invertebrate_mtdna_files_count += 1
    return vertebrate_mtdna_files_count, invertebrate_mtdna_files_count

# =============================================================================
#       Main subrtn      
# =============================================================================
print("(1)")
print("\tStarting..")
load_folders(vertebrate_mtdna, "Vertebrate")
load_folders(invertebrate_mtdna, "Invertebrate")

print("\tSearching directory")
x, y = search_fitter_folder(FITTERS)

print("Total:", x+y)
print("Vertebrate:", x)
print("Invertebrate:", y)


# =============================================================================
# End of file
# =============================================================================
