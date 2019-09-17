#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 17:07:40 2019

@author: alex
"""
# =============================================================================
# Imports
# =============================================================================
import json
import os
import scipy
from scipy import stats
from scipy.stats import iqr

# =============================================================================
# Declares
# =============================================================================
path = "/Users/alex/Documents/TRIPLE_HITS/SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"
files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(".json")]

# =============================================================================
# Helper functions
# =============================================================================

def read_json_THDHRate(filename):
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()  
    
    TH_Rate = json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["rate at which 3 nucleotides are changed instantly within a single codon"]
    DH_Rate1 = json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["rate at which 2 nucleotides are changed instantly within a single codon"]
    
    #DH Rate from the DH Model
    DH_Rate2 = json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["rate at which 2 nucleotides are changed instantly within a single codon"]
   
    return TH_Rate, DH_Rate1, DH_Rate2


def read_json_AICc(filename):
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    TH_AICc = json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["AIC-c"]
    DH_AICc = json_data["fits"]["MG94 with double instantaneous substitutions"]["AIC-c"]
    SH_AICc = json_data["fits"]["Standard MG94"]["AIC-c"]
    
    return TH_AICc, DH_AICc, SH_AICc


def read_json_Omegas(filename):
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()

    TH_omega, DH_omega, SH_omega = 0, 0 ,0
    #pvalue_THvsDH_LRT = 0
    
    TH_omega = json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["non-synonymous/synonymous rate ratio"]
    DH_omega = json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["parameters"]["non-synonymous/synonymous rate ratio"]
    SH_omega = json_data["fits"]["Standard MG94"]["Rate Distributions"]["parameters"]["non-synonymous/synonymous rate ratio"]

    #if json_data["test results"]["Triple-hit vs double-hit"]["p-value"] < pvalue_threshold:
    #    pvalue_THvsDH_LRT = 1

    #return pvalue_THvsDH_LRT, TH_omega, DH_omega, SH_omega
    return TH_omega, DH_omega, SH_omega


def mean_and_IQR(Array, desc):
    print("Stats " + desc + "\n", stats.describe(Array))

    print("IQR:", scipy.stats.iqr(Array, rng=(25, 75)))

    print()
    
# =============================================================================
# Main subrtn
# =============================================================================

#TH Rate, DHRate
#DH Rate
    
TH_TH_Rate = []
TH_DH_Rate = []
DH_DH_Rate = []

delta_AICc_THvsSH = []
delta_AICc_DHvsSH = []

delta_omega_THvsSH = []
delta_omega_DHvsSH = []
SH_omega = []

print("Reading through files:", len(files))
for n, file in enumerate(files):
    #Rates
    TH_Rate, DH_Rate1, DH_Rate2 = read_json_THDHRate(file)
    
    TH_TH_Rate.append(float(TH_Rate))
    TH_DH_Rate.append(DH_Rate1)
    DH_DH_Rate.append(DH_Rate2)

    #AICc
    TH_AICc, DH_AICc, SH_AICc = read_json_AICc(file)
    
    delta_AICc_THvsSH.append(float(TH_AICc) - float(SH_AICc))
    delta_AICc_DHvsSH.append(float(DH_AICc) - float(SH_AICc))
    
    
    #Omegas
    TH_omega, DH_omega, SH_omega = read_json_Omegas(file)
    
    delta_omega_THvsSH.append(float(TH_omega) - float(SH_omega))
    delta_omega_DHvsSH.append(float(DH_omega) - float(SH_omega))
    
    
    
print("Descriptive statistics")
#scipy.stats.iqr(x, axis=None, rng=(25,75), scale='raw', nan_policy='propagate', interpolation='linear', keepdims=False)

#print("TH Rate stats:\n", stats.describe(TH_TH_Rate ))
#print("TH Rate IQR:", scipy.stats.iqr(TH_TH_Rate, rng=(25, 75)))


mean_and_IQR(TH_TH_Rate, "TH Rate")
mean_and_IQR(TH_DH_Rate, "TH DH Rate")
mean_and_IQR(DH_DH_Rate, "DH DH Rate")


#delta AICC (mean and IQR)
mean_and_IQR(delta_AICc_THvsSH, "delta AICc THvsSH")
mean_and_IQR(delta_AICc_DHvsSH, "delta AICc DHvsSH")

#delta omega (mean and IQR)
mean_and_IQR(delta_omega_THvsSH, "delta omega THvsSH")
mean_and_IQR(delta_omega_DHvsSH, "delta omega DHvsSH")

