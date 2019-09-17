#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 15:38:23 2019

@author: alexander lucaci


Used to make, generate data for

#Figure 2, delta omega relative to SH

https://plot.ly/python/axes/
"""
# =============================================================================
# imports
# =============================================================================
import json
import plotly
import plotly.graph_objects as go
import os


# =============================================================================
# Declares
# =============================================================================
path = "/Users/alex/Documents/TRIPLE_HITS/SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"
files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(".json")]



# =============================================================================
# helper functions
# =============================================================================
def read_json(filename):
    
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

def subplot_boxplot(TH_omegas, DH_omegas, SH_omegas, filename):
    
    #plotly.offline.init_notebook_mode(connected=False)
    
    ##trace0 = go.Box(y=asizes[0], text=adesc[0], name=species[0])
    #trace1 = go.Box(y=asizes[1], text=adesc[1], name=species[1])
    #trace2 = go.Box(y=asizes[2], text=adesc[2], name=species[2])
    
    trace0 = go.Box(y=TH_omegas, name = "delta Omega values (THvsSH)")
    trace1 = go.Box(y=DH_omegas, name = "delta Omega values (DHvsSH)")
    trace2 = go.Box(y=SH_omegas, name= "SH Omega values")
    
    
    #fig = go.Figure(data=[trace0, trace1, trace2])
    
    fig = go.Figure(data=[trace0, trace1, trace2])
    
    fig["layout"].update(title="")
    #fig.update_xaxes(title_font=dict(size=24, family='Courier', color='black'))
    #fig.update_yaxes(title_font=dict(size=24, family='Courier', color='black'))
    fig.update_yaxes(tickfont=dict(family='Rockwell', color='black', size=18))
    
    #output_filename = output_dir+fname.replace(".csv", "").split("/")[-1]
    #output_filename = file
    
    #plotly.offline.plot(fig, filename=output_filename+filename+"_SUBPLOT_Boxplot.html")
    plotly.offline.plot(fig, filename=filename+"_SUBPLOT_Boxplot.html")



# =============================================================================
# Main subrtn
# =============================================================================

deltaTH_values = []
deltaDH_values = []
SH_omega_values = []

#scan through fitters
print("scanning through fitters:", len(files))
for n, file in enumerate(files):
    #grab SH omega
    #grab DH, TH omega
    if n % 1000 == 0: print(n)
    TH_omega, DH_omega, SH_omega = read_json(file) #returns omegas

    #delta TH omega = TH - SH
    deltaTH = float(TH_omega) - float(SH_omega)

    #delta DH omega = DH - SH
    deltaDH = float(DH_omega) - float(SH_omega)

    
    #sif float(SH_omega) > 10: continue
    
    deltaTH_values.append(deltaTH)
    deltaDH_values.append(deltaDH)
    SH_omega_values.append(SH_omega)

#plots 
print("plotting")
#subplot_boxplot(deltaTH_values, deltaDH_values, "TEST")
subplot_boxplot(deltaTH_values, deltaDH_values, SH_omega_values, "TEST")

#plot TH omega
#plot DH omega


