#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:49:59 2019

@author: alexander lucaci

@used: to edit the *.FITTER.json from FitMultiModel.bf

6/2019: Modified to handle the output from the FitMultiModel with SRV added.

10/2019: Added support for v0.2 Fitters
"""

# =============================================================================
# Imports
# =============================================================================
import json, csv, os
import sys

# =============================================================================
# Declares
# =============================================================================
path = "/Users/phylo/Documents/Pond Lab/FITTERS/MG94_FITTERS"

#Look for this ending.
file_ending = ".FITTER.json"

#Output CSF Filename
file_output = "MG94_FITTERS.csv"

#Create blank file.
with open(file_output, "w") as f:
    f.write("")
f.close()

# =============================================================================
# Helper functions
# =============================================================================
def sum_branchlengths(branch_attributes, model):
    #pass
    #print(branch_attributes)
    treelength = 0
    for key in branch_attributes.keys():
        #print(key, branch_attributes[key][model])
        treelength += float(branch_attributes[key][model])
    return treelength

def report_branchlengths(branch_attributes, model):
    taxa_bl_dict = {}
    
    for key in branch_attributes.keys():
        taxa_bl_dict[key] = branch_attributes[key][model]
    
    return taxa_bl_dict
        

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
        this_row.append(json_data["test results"]["Triple-hit vs Triple-hit-island"]["LRT"])
        this_row.append(json_data["test results"]["Triple-hit vs Triple-hit-island"]["p-value"])
        this_row.append(json_data["test results"]["Triple-hit-island vs double-hit"]["LRT"])
        this_row.append(json_data["test results"]["Triple-hit-island vs double-hit"]["p-value"])
        
        #"MG94 with double and triple instantaneous substitutions" [ISLANDS]
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["AIC-c"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Log Likelihood"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide A to nucleotide C"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide A to nucleotide G"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide A to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide C to nucleotide G"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide C to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["Substitution rate from nucleotide G to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["non-synonymous/synonymous rate ratio"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["rate at which 2 nucleotides are changed instantly within a single codon"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["rate at which 3 nucleotides are changed instantly within a single codon"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["rate at which 3 nucleotides are changed instantly within a single codon between synonymous codon islands"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["GDD rate category 1"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["GDD rate category 2"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["GDD rate category 3"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["Mixture auxiliary weight for GDD category 1"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["parameters"]["Mixture auxiliary weight for GDD category 2"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions [only synonymous islands]"]["Rate Distributions"]["distribution"])

        

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
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["rate at which 3 nucleotides are changed instantly within a single codon between synonymous codon islands"])
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

        #Tree lengths
        TREE_data = json_data["branch attributes"]["0"]
        #Triple hit Tree length
        TH_TL = sum_branchlengths(TREE_data, "MG94 with double and triple instantaneous substitutions")
        #Double hit tree length
        DH_TL = sum_branchlengths(TREE_data, "MG94 with double instantaneous substitutions")
        #Single hit tree length
        SH_TL = sum_branchlengths(TREE_data, "Standard MG94")
        
        #print(TH_TL, DH_TL, SH_TL)
        this_row.append(TH_TL)
        this_row.append(DH_TL)
        this_row.append(SH_TL)
        
        
        #Branch attributes
        TH_BA = report_branchlengths(TREE_data, "MG94 with double and triple instantaneous substitutions")
        DH_BA = report_branchlengths(TREE_data, "MG94 with double and triple instantaneous substitutions")
        SH_BA = report_branchlengths(TREE_data, "Standard MG94")
        
        #print(TH_BA)
        this_row.append(TH_BA)
        this_row.append(DH_BA)
        this_row.append(SH_BA)
                
    fh.close()
    writeto_csv(filename, this_row)

# --- CSV --- #
def writeto_csv(filename, this_row):
    global columns, wrote_columns, file_output
    #csv.writer(open(file_output, "a+"), delimiter=",") #MAC
    csv_writer = csv.writer(open(file_output, "a+"), delimiter=",", lineterminator='\n') #WINDOWS
    if wrote_columns == False:
        csv_writer.writerow(columns)
        wrote_columns = True
    #print([this_row])
    csv_writer.writerow(this_row)

# =============================================================================
# Main subroutine
# =============================================================================
columns = ["File name", "number of sequences", "number of sites"]

#Test results, model comparisons via LRT
columns += ["Double-hit vs single-hit - LRT", "Double-hit vs single-hit - p-value"] 
columns += ["Triple-hit vs double-hit - LRT", "Triple-hit vs double-hit - p-value"]
columns += ["Triple-hit vs single-hit - LRT",  "Triple-hit vs single-hit - p-value"]
columns += ["Triple-hit vs Triple-hit-island - LRT", "Triple-hit vs Triple-hit-island - p-value"]
columns += ["Triple-hit-island vs double-hit - LRT", "Triple-hit-island vs double-hit - p-value"]


#TH Model Islands
columns += ["MG94 with double and triple instantaneous substitutions [ISLANDS]- AIC-c", "MG94 with double and triple instantaneous substitutions [ISLANDS] - Log Likelihood"]
columns += ["Substitution rate from nucleotide A to nucleotide C", "Substitution rate from nucleotide A to nucleotide G", "Substitution rate from nucleotide A to nucleotide T","Substitution rate from nucleotide C to nucleotide G","Substitution rate from nucleotide C to nucleotide T","Substitution rate from nucleotide G to nucleotide T"]
columns += ["non-synonymous/synonymous rate ratio", "rate at which 2 nucleotides are changed instantly within a single codon", "rate at which 3 nucleotides are changed instantly within a single codon"]
columns += ["rate at which 3 nucleotides are changed instantly within a single codon between synonymous codon islands"]
columns += ["GDD rate category 1.triple", "GDD rate category 2.triple", "GDD rate category 3.triple","Mixture auxiliary weight for GDD category 1.triple", "Mixture auxiliary weight for GDD category 2.triple"]
columns += ["distribution.triple"]

#TH Model
columns += ["MG94 with double and triple instantaneous substitutions - AIC-c", "MG94 with double and triple instantaneous substitutions - Log Likelihood"]
columns += ["Substitution rate from nucleotide A to nucleotide C", "Substitution rate from nucleotide A to nucleotide G", "Substitution rate from nucleotide A to nucleotide T","Substitution rate from nucleotide C to nucleotide G","Substitution rate from nucleotide C to nucleotide T","Substitution rate from nucleotide G to nucleotide T"]
columns += ["non-synonymous/synonymous rate ratio", "rate at which 2 nucleotides are changed instantly within a single codon", "rate at which 3 nucleotides are changed instantly within a single codon"]
columns += ["rate at which 3 nucleotides are changed instantly within a single codon between synonymous codon islands"]
columns += ["GDD rate category 1.triple", "GDD rate category 2.triple", "GDD rate category 3.triple","Mixture auxiliary weight for GDD category 1.triple", "Mixture auxiliary weight for GDD category 2.triple"]
columns += ["distribution.triple"]

#DH Model
columns += ["MG94 with double instantaneous substitutions - AIC-c", "MG94 with double instantaneous substitutions - Log Likelihood"]
columns += ["Substitution rate from nucleotide A to nucleotide C", "Substitution rate from nucleotide A to nucleotide G", "Substitution rate from nucleotide A to nucleotide T","Substitution rate from nucleotide C to nucleotide G","Substitution rate from nucleotide C to nucleotide T","Substitution rate from nucleotide G to nucleotide T"]
columns += ["non-synonymous/synonymous rate ratio", "rate at which 2 nucleotides are changed instantly within a single codon"]
columns += ["GDD rate category 1.double", "GDD rate category 2.double", "GDD rate category 3.double","Mixture auxiliary weight for GDD category 1.double", "Mixture auxiliary weight for GDD category 2.double"]
columns += ["distribution.double"]

#SH Model
columns += ["Standard MG94 - AIC-c", "Standard MG94 - Log Likelihood"]
columns += ["Substitution rate from nucleotide A to nucleotide C", "Substitution rate from nucleotide A to nucleotide G", "Substitution rate from nucleotide A to nucleotide T","Substitution rate from nucleotide C to nucleotide G","Substitution rate from nucleotide C to nucleotide T","Substitution rate from nucleotide G to nucleotide T"]
columns += ["non-synonymous/synonymous rate ratio"]
columns += ["GDD rate category 1.single", "GDD rate category 2.single", "GDD rate category 3.single","Mixture auxiliary weight for GDD category 1.single", "Mixture auxiliary weight for GDD category 2.single"]
columns += ["distribution.single"]

#Branches
columns += ["Tree Length - MG94 with double and triple instantaneous substitutions", "Tree Length - MG94 with double instantaneous substitutions", "Tree Length - Standard MG94"]
columns += ["Branch Attributes - MG94 with double and triple instantaneous substitutions", "Branch Attributes - MG94 with double instantaneous substitutions", "Branch Attributes - Standard MG94"]



files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(file_ending)]

wrote_columns = False

count = 0 #for debugging.

for file in files:
    print(count, file)
    read_json(file)
    count += 1
    #if count == 2: break

# =============================================================================
# END OF FILE
# =============================================================================