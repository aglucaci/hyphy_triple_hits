# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 10:26:20 2019

@author: alexander lucaci

2 * Natural Log * Evidence Ratio (per site)

https://plot.ly/python/line-charts/
https://docs.scipy.org/doc/numpy/reference/generated/numpy.log.html

find /home/aglucaci/TRIPLE_HITS/data/selectome_trip_ammended -empty -type f -delete
ls -lahS ../data/selectome_trip_ammended/*.FITTER.json | wc -l
tar -czvf SELECTOME_TRIP_AMMENDED_FITTER_JSON.tar.gz /SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON

floating points in python; https://docs.python.org/3.4/tutorial/floatingpoint.html
issues with f and mu

 mkdir /home-silverback/aglucaci/TRIPLE_HITS/analysis/SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON_ADDITIONAL
 
 
This script looks to analyze the Evidence ratio data from FITTER.JSON and create some summary statistics

"""

# =============================================================================
# Imports
# =============================================================================
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import json, csv, os, sys
from shutil import copyfile
import csv
from scipy import stats
import sys
import os

# =============================================================================
# Declares
# =============================================================================

# --- SELECTOME_TRIP_AMMENDED_SRV
#directory = r"E:\SELECTOME_TRIP_AMMENDED_SRV\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"
#output_dir = r"E:\SELECTOME_TRIP_AMMENDED_SRV\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON_HTML"
directory = sys.argv[1]
output_dir = sys.argv[2]
fname = sys.argv[3]

#fname = "analysis_" #Output file
pvalue_threshold = 0.05

custom_analysis = {}
custom_analysis["NumOfSites"] = [] #Number of sites for significant files. What is the average?

#https://cdn.kastatic.org/ka-perseus-images/f5de6355003ee322782b26404ef0733a1d1a61b0.png
#SERINE_CODONS = ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"]
TH_Sites_avg = []

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# =============================================================================
# Helper functions
# =============================================================================

def load_json(filename, file_count):
    print()
    print("(" + str(file_count) + ") Loading:", filename)
    
    with open(filename, "r") as fh:
        json_data = json.load(fh)
        TH = json_data["Evidence Ratios"]["Three-hit"][0]
        DH = json_data["Evidence Ratios"]["Two-hit"][0]
        SITES = json_data["input"]["number of sites"] #can also calculated from the len of DH or TH
        THvsDH_LRT_pvalue = json_data["test results"]["Triple-hit vs double-hit"]["p-value"]
        Site_subs = json_data["Site substitutions"]
    fh.close()
    
    return TH, DH, np.arange(0, int(SITES)), Site_subs, THvsDH_LRT_pvalue

def plotly_basicline(data_x, data_y_TH, data_y_DH, output_title, output):
    global output_dir
    
    # Create trace(s)
    trace0 = go.Scatter(x = data_x, y = data_y_TH, mode = 'lines+markers', name="Three Hit", opacity=0.75)
    trace1 = go.Scatter(x = data_x, y = data_y_DH, mode = 'lines+markers', name="Double Hit", opacity=0.75)
    data = [trace0, trace1]
    
    layout = dict(title = '2*LN(Evidence Ratio), Number of Sites = ' + str(len(data_x)) + ", " + output_title, 
                  xaxis = dict(title = 'SITE'), 
                  yaxis = dict(title = '2*LN(Evidence Ratio)'),)
    
    fig = dict(data=data, layout=layout)
    
    output_file = os.path.join(output_dir, output_title + ".html")
    
    print("() SAVING:", output_file)
    plot(fig, filename=output_file, auto_open=False) #auto_open=False for sanity.
    
# =============================================================================
# Main subrout.
# =============================================================================
def main_sub(filename, output_title, file_count):
    global fname, pvalue_threshold, TH_Sites_avg 
    
    #Load data from .FITTER.json
    EvidenceRatio_TH, EvidenceRatio_DH, Sites, Site_subs, THvsDH_LRT_pvalue = load_json(filename, file_count)

    if float(THvsDH_LRT_pvalue) >= pvalue_threshold: return
    
    # -- Analysis
    #given the evidence ratio values.
    #generate mean
    #threshold is 3x the mean.
    print("Triple hit Evidence Ratio mean:", np.mean(EvidenceRatio_TH))
    print("Double hit Evidence Ratio mean:", np.mean(EvidenceRatio_DH))
    
    Threshold_TH = 3 * np.mean(EvidenceRatio_TH)
    Threshold_DH = 3 * np.mean(EvidenceRatio_DH)
    
    print("Triple hit - Threshold", Threshold_TH)
    print("Double hit - Threshold", Threshold_DH)
    print("Number of Sites:", len(Sites))
    
    msg = []
    msg.append(filename.split("\\")[-1]) 
    msg.append(str(len(Sites)))
    msg.append(str(np.mean(EvidenceRatio_TH)))
    msg.append(str(np.mean(EvidenceRatio_DH)))
    msg.append(str(Threshold_TH))
    msg.append(str(Threshold_DH)) #
    
    #filter
    #http://book.pythontips.com/en/latest/map_filter.html
    Filtered_Threshold_TH = list(filter(lambda x: x > Threshold_TH, EvidenceRatio_TH))
    Filtered_Threshold_DH = list(filter(lambda x: x > Threshold_DH, EvidenceRatio_DH))
    
    print("THvsDH LRT pvalue:", THvsDH_LRT_pvalue)
    msg.append(str(THvsDH_LRT_pvalue))
    
    if Filtered_Threshold_TH > []:
        msg.append(str(len(Filtered_Threshold_TH)))
        
        print("Number of TH sites:", len(Filtered_Threshold_TH))
        TH_Sites_avg.append(len(Filtered_Threshold_TH))
        
        #post prociessing
        for i, item in enumerate(EvidenceRatio_TH):
            if item in Filtered_Threshold_TH:          
                try:
                    print("TH_ Location, Value:", i, item, Site_subs[str(i)])
                    msg.append("{" + str(i) + ": " + str(Site_subs[str(i)]) + "}")
                    
                    #Serine analysis
                    
                except:
                    print("TH_ Location, Value:", i, item, "SITE SUB NOT FOUND IN JSON")
                    msg.append("{" + str(i) + ": " + "NA" + "}")
    else: 
        msg.append("0") #Spacer for Number of TH Sites
        msg.append("NA") #Spacer for Location, Value
        

    #write msg to file.
    with open(os.path.join(output_dir,fname), 'a') as f:
        #for item in msg:
            #f.write("%s\n" % item)
        #f.write(", ".join(msg) + "\n")
        f.write("\t ".join(msg) + "\n")
    f.close()
                
    
# =============================================================================
# Starting program..
# =============================================================================
print("() Starting Evidence ratio analysis")
file_count, count = 0, 0 #For Analysis, Plotting respectively.

# -- Init. Output file
header = ["Filename", "Total Num of Sites", "TH Mean", "DH Mean", "TH Threshold", "DH Threshold", "THvsDH_LRT_pvalue", "TH - Num of Sites", "TH Sites Location & Codon"]
with open(os.path.join(output_dir,fname), 'w') as f:
    f.write("\t ".join(header) + "\n")
f.close()

print("() Checking for json files in:", directory)

for root, dirs, files in os.walk(directory):
    for each_file in files:
        name, ext = os.path.splitext(each_file)
        if ext == ".json":
            existing = os.path.join(output_dir, name + ext)
            # -- For Analysis
            existing = os.path.join(directory, name + ext)
            main_sub(existing, each_file, file_count)
            file_count += 1
            if file_count == 12: break
            
            
# SUMARY STATISTICS
print("\n", stats.describe(np.asarray(TH_Sites_avg)))


# =============================================================================
# End of file
# =============================================================================
