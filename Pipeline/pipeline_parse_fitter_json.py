#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:49:59 2019

@author: alexander lucaci

@used: to edit the *.FITTER.json from FitMultiModel.bf

6/2019: Modified to handle the output from the FitMultiModel with SRV added.

"""

"""
    MAKE THIS A PIPELINE
    
    INPUT: FITTERS DIRECTORY
    
    Circos: circos_grab_site_substitution_data.py <FITTERS DIRECTORY> <OUTPUTTXT>
    
    parse_fitter_json.py <FITTERS DIRECTORY> <OUTPUTCSV>
    
    plot_csv.py
    
    plot_pvalue_vs_seqlength.py
    
    plot_2LogEvidenceRatio.py
    
    physiochemical_triple_changes.py
    
    Serine_to_Serine.py
"""

# =============================================================================
# Imports
# =============================================================================
import json, csv, os
import sys

# =============================================================================
# Declares
# =============================================================================
#path = "/Users/alex/Documents/TRIPLE_HITS/mtDNA/Invertebrate_mtDNA_FITTERS"
path = sys.argv[1]

#Look for this ending.
file_ending = "FITTER.json"

#Output CSF Filename
#file_output = "Invertebrate_mtDNA.csv"
file_output = sys.argv[2]

# =============================================================================
# Helper functions
# =============================================================================
def read_json(filename):
    this_row = []
    with open(filename, "r") as fh:
        json_data = json.load(fh)

        this_row.append(json_data["input"]["file name"].split("/")[-1])
        this_row.append(json_data["input"]["number of sequences"])
        this_row.append(json_data["input"]["number of sites"])

        this_row.append(json_data["test results"]["Double-hit vs single-hit"]["LRT"])
        this_row.append(json_data["test results"]["Double-hit vs single-hit"]["p-value"])
        this_row.append(json_data["test results"]["Triple-hit vs double-hit"]["LRT"])
        this_row.append(json_data["test results"]["Triple-hit vs double-hit"]["p-value"])
        this_row.append(json_data["test results"]["Triple-hit vs single-hit"]["LRT"])
        this_row.append(json_data["test results"]["Triple-hit vs single-hit"]["p-value"])

        #"MG94 with double and triple instantaneous substitutions"
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["AIC-c"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Log Likelihood"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide A to nucleotide C"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide A to nucleotide G"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide A to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide C to nucleotide G"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide C to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide G to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["non-synonymous/synonymous rate ratio"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["rate at which 2 nucleotides are changed instantly within a single codon"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["rate at which 3 nucleotides are changed instantly within a single codon"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["GDD rate category 1"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["GDD rate category 2"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["GDD rate category 3"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["Mixture auxiliary weight for GDD category 1"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["Mixture auxiliary weight for GDD category 2"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["distribution"])

        #"MG94 with double instantaneous substitutions"
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["AIC-c"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Log Likelihood"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide A to nucleotide C"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide A to nucleotide G"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide A to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide C to nucleotide G"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide C to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide G to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["non-synonymous/synonymous rate ratio"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["rate at which 2 nucleotides are changed instantly within a single codon"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["GDD rate category 1"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["GDD rate category 2"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["GDD rate category 3"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["Mixture auxiliary weight for GDD category 1"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["Mixture auxiliary weight for GDD category 2"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["distribution"])

        #"Standard MG94"
        this_row.append(json_data["fits"]["Standard MG94"]["AIC-c"])
        this_row.append(json_data["fits"]["Standard MG94"]["Log Likelihood"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide A to nucleotide C"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide A to nucleotide G"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide A to nucleotide T"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide C to nucleotide G"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide C to nucleotide T"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide G to nucleotide T"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["parameters"]["non-synonymous/synonymous rate ratio"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["parameters"]["GDD rate category 1"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["parameters"]["GDD rate category 2"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["parameters"]["GDD rate category 3"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["parameters"]["Mixture auxiliary weight for GDD category 1"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["parameters"]["Mixture auxiliary weight for GDD category 2"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["distribution"])

        #GENES WITH TRIPLE HIT RATES ABOVE 1
    fh.close()
    writeto_csv(filename, this_row, "a+")

# --- CSV --- #
def writeto_csv(filename, this_row, mode):
    global columns, wrote_columns, file_output
    #csv.writer(open(file_output, "a+"), delimiter=",") #MAC
    csv_writer = csv.writer(open(file_output, mode), delimiter=",", lineterminator='\n') #WINDOWS
    if wrote_columns == False:
        csv_writer.writerow(columns)
        wrote_columns = True
    #print([this_row])
    csv_writer.writerow(this_row)
    
def create_nullfile(filename):
    with open(filename, "w") as f:
        f.write("")
    f.close()
    
    

# =============================================================================
# Main subroutine
# =============================================================================
columns = ["File name", "number of sequences", "number of sites", "Double-hit vs single-hit - LRT", "Double-hit vs single-hit - p-value", "Triple-hit vs double-hit - LRT", "Triple-hit vs double-hit - p-value", "Triple-hit vs single-hit - LRT",  "Triple-hit vs single-hit - p-value"]
columns += ["MG94 with double and triple instantaneous substitutions - AIC-c", "MG94 with double and triple instantaneous substitutions - Log Likelihood"]
columns += ["Substitution rate from nucleotide A to nucleotide C", "Substitution rate from nucleotide A to nucleotide G", "Substitution rate from nucleotide A to nucleotide T","Substitution rate from nucleotide C to nucleotide G","Substitution rate from nucleotide C to nucleotide T","Substitution rate from nucleotide G to nucleotide T"]
columns += ["non-synonymous/synonymous rate ratio", "rate at which 2 nucleotides are changed instantly within a single codon","rate at which 3 nucleotides are changed instantly within a single codon"]

columns += ["GDD rate category 1.triple", "GDD rate category 2.triple", "GDD rate category 3.triple","Mixture auxiliary weight for GDD category 1.triple", "Mixture auxiliary weight for GDD category 2.triple"]
columns += ["distribution.triple"]

columns += ["MG94 with double instantaneous substitutions - AIC-c", "MG94 with double instantaneous substitutions - Log Likelihood"]
columns += ["Substitution rate from nucleotide A to nucleotide C", "Substitution rate from nucleotide A to nucleotide G", "Substitution rate from nucleotide A to nucleotide T","Substitution rate from nucleotide C to nucleotide G","Substitution rate from nucleotide C to nucleotide T","Substitution rate from nucleotide G to nucleotide T"]
columns += ["non-synonymous/synonymous rate ratio", "rate at which 2 nucleotides are changed instantly within a single codon"]

columns += ["GDD rate category 1.double", "GDD rate category 2.double", "GDD rate category 3.double","Mixture auxiliary weight for GDD category 1.double", "Mixture auxiliary weight for GDD category 2.double"]
columns += ["distribution.double"]

columns += ["Standard MG94 - AIC-c", "Standard MG94 - Log Likelihood"]
columns += ["Substitution rate from nucleotide A to nucleotide C", "Substitution rate from nucleotide A to nucleotide G", "Substitution rate from nucleotide A to nucleotide T","Substitution rate from nucleotide C to nucleotide G","Substitution rate from nucleotide C to nucleotide T","Substitution rate from nucleotide G to nucleotide T"]
columns += ["non-synonymous/synonymous rate ratio"]

columns += ["GDD rate category 1.single", "GDD rate category 2.single", "GDD rate category 3.single","Mixture auxiliary weight for GDD category 1.single", "Mixture auxiliary weight for GDD category 2.single"]
columns += ["distribution.single"]

#path = os.getcwd()
#path="/home/swisotsky/data/selectome_4_11_19/data/"

files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(file_ending)]

create_nullfile(file_output)

wrote_columns = False
count = 0
for file in files:
    #print(count, file)
    read_json(file)
    count += 1
    #if count == 2: break

print("\tDone.")
# =============================================================================
# END OF FILE
# =============================================================================