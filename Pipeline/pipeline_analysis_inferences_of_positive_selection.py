#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 19:04:16 2019

@author: alexander g. lucaci

This script looks for changes in the inference of positive selection across our three models.

Triple hit models
DH models
SH models



"""
# =============================================================================
# Imports
# =============================================================================
import sys
import os
import json
from prettytable import PrettyTable

# =============================================================================
# Declares
# =============================================================================

path = "/Users/alex/Documents/TRIPLE_HITS/SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"

pvalue_threshold = 0.05


# =============================================================================
# Helper functions
# =============================================================================
"""
fits

MG94 with double and triple instantaneous substitutions
parameters
non-synonymous/synonymous rate ratio


MG94 with double instantaneous substitutions
parameters
non-synonymous/synonymous rate ratio


Standard MG94
parameters
non-synonymous/synonymous rate ratio

"""

def read_json(filename):
    global pvalue_threshold
    
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()

    TH_omega, DH_omega, SH_omega = 0, 0 ,0
    pvalue_THvsDH_LRT = 0
    
    TH_omega = json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["non-synonymous/synonymous rate ratio"]
    DH_omega = json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["non-synonymous/synonymous rate ratio"]
    SH_omega = json_data["fits"]["Standard MG94"]["Rate Distributions"]["parameters"]["non-synonymous/synonymous rate ratio"]

    if json_data["test results"]["Triple-hit vs double-hit"]["p-value"] < pvalue_threshold:
        pvalue_THvsDH_LRT = 1

    return pvalue_THvsDH_LRT, TH_omega, DH_omega, SH_omega

# =============================================================================
# Main subroutine
# =============================================================================

files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(".json")]

print("Total number of .jsons:", len(files))

positive_omega = [0, 0, 0] #count of files with omegas over 1.0
files_omega = [[], [], []] #files with omegas over 1.0

pvalue_threshold_THvsDH_LRT = 0
pvalue_threshold_THvsDH_LRT_files = []
#omega_comparison = {}

up_TH_omega_comparison = [0, 0] # vsDH, vsSH
up_DH_omega_comparison = [0, 0] # vsTH, vsSH
up_SH_omega_comparison = [0, 0] # vsTH, vsDH

down_TH_omega_comparison = [0, 0] # vsDH, vsSH
down_DH_omega_comparison = [0, 0] # vsTH, vsSH
down_SH_omega_comparison = [0, 0] # vsTH, vsDH

for file in files:
    
    pvalue_THvsDH_LRT, TH, DH, SH = read_json(file) #returns omegas
    
    #print(type(TH))
    if TH > 1.0:
        positive_omega[0] += 1
        files_omega[0].append(file)
    if DH > 1.0:
        positive_omega[1] += 1
        files_omega[1].append(file)
    if SH > 1.0:
        positive_omega[2] += 1
        files_omega[2].append(file)
        
    pvalue_threshold_THvsDH_LRT += pvalue_THvsDH_LRT # 1 if passes threshold, 0 if it doesn't
    
    if pvalue_THvsDH_LRT == 1:
        pvalue_threshold_THvsDH_LRT_files.append(file)
        
        #omega_comparison[file] = [TH, DH, SH]
        
        #up
        if TH > DH: up_TH_omega_comparison[0] += 1
        if TH > SH: up_TH_omega_comparison[1] += 1
        
        if DH > TH: up_DH_omega_comparison[0] += 1
        if DH > SH: up_DH_omega_comparison[1] += 1
        
        if SH > TH: up_SH_omega_comparison[0] += 1
        if SH > DH: up_SH_omega_comparison[1] += 1
        
        #down
        if TH < DH: down_TH_omega_comparison[0] += 1 #means the TH omega is less than the DH omega
        if TH < SH: down_TH_omega_comparison[1] += 1
        
        if DH < TH: down_DH_omega_comparison[0] += 1
        if DH < SH: down_DH_omega_comparison[1] += 1
        
        if SH < TH: down_SH_omega_comparison[0] += 1
        if SH < DH: down_SH_omega_comparison[1] += 1
        
    
        


print("Positive omegas (TH, DH, SH):", positive_omega)

print("Omega comparison UP ([vsDH, vsSH], [vsTH, vsSH], [vsTH, vsDH])", up_TH_omega_comparison, up_DH_omega_comparison, up_SH_omega_comparison)
print("Omega comparison Down ([vsDH, vsSH], [vsTH, vsSH], [vsTH, vsDH])", down_TH_omega_comparison, down_DH_omega_comparison, down_SH_omega_comparison)


#table
"""
                                    Standard MG94, DH, TH
number of files with omega > 1.0


Are they the same files?


"""

x = PrettyTable()

x.field_names = ["#", "", "MG94 with double and triple instantaneous substitutions", "MG94 with double instantaneous substitutions", "Standard MG94"]

x.add_row(["1", "number of files with omega > 1.0"] + positive_omega)

x.add_row(["2", "Are they the same files? "] + [  "DH("+str(len(set(files_omega[0]) & set(files_omega[1])))+") SH("+str(len(set(files_omega[0]) & set(files_omega[2]))) + ")",
                                              "TH("+str(len(set(files_omega[1]) & set(files_omega[0])))+") SH("+str(len(set(files_omega[1]) & set(files_omega[2]))) + ")", 
                                              "TH("+str(len(set(files_omega[2]) & set(files_omega[0])))+") DH("+str(len(set(files_omega[2]) & set(files_omega[1]))) + ")"])

x.add_row(["3" , "Number of files with p<0.05 for THvsDH LRT"] + [pvalue_threshold_THvsDH_LRT, "NA", "NA"])

x.add_row(["4", "Are these the same files?"] + [  len(set(files_omega[0]) & set(pvalue_threshold_THvsDH_LRT_files)),
                                              len(set(files_omega[1]) & set(pvalue_threshold_THvsDH_LRT_files)), 
                                              len(set(files_omega[2]) & set(pvalue_threshold_THvsDH_LRT_files))])
    
    
x.add_row(["5", "[What happened in these files? From 3.]"] + ["-", "-", "-"])  

#x.add_row([" -> Omega went up"] + "DH(), SH()")

x.add_row(["6", " -> Omega went up"] + ["(vsDH, vsSH) " + " ".join(str(v) for v in up_TH_omega_comparison), 
          "(vsTH, vsSH) " + " ".join(str(v) for v in up_DH_omega_comparison), 
          "(vsTH, vsDH) " + " ".join(str(v) for v in up_SH_omega_comparison)])
    
x.add_row(["7", " -> Omega stayed the same"] + ["NA", "NA", "NA"])      

x.add_row(["8", " -> Omega went down"] + [" ".join(str(v) for v in down_TH_omega_comparison), 
          " ".join(str(v) for v in down_DH_omega_comparison), 
          " ".join(str(v) for v in down_SH_omega_comparison)])                                                                                                                                                     

x.add_row(["9", "TH rate > 1.0 and omega 1.0"] + ["NA", "NA", "NA"])

x.add_row(["10", "DH rate > 1.0 and omega 1.0"] + ["NA", "NA", "NA"])
x.add_row(["11" , "Number of files with p<0.05 for DHvsSH LRT"] + ["NA", "Value", "NA"])
x.add_row(["12", "[What happened in these files? From 11.]"] + ["-", "-", "-"])  

print(x)



# =============================================================================
# End of file
# =============================================================================













