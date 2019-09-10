#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 10:52:03 2019

@author: alexander lucaci

To aid in the analysis of spatial domains around TH sites.


Logic is as follows


Total number of jsons

Lets focus on files where TH is preferred over DH (LRT, p<=0.05)
How many files is this?

How many of these files have 1 TH site 10x above the Evidence Ratio mean?


"""

# =============================================================================
# Imports
# =============================================================================
import os
import sys
import plotly
import plotly.graph_objs as go
import json
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.subplots import make_subplots

# =============================================================================
# Declares
# =============================================================================
path = "/Users/alex/Documents/TRIPLE_HITS/SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"
THRESHOLD_TH_VALUE = 10 #(10x) the mean
pvalue_threshold = 0.05


# =============================================================================
# Helper functions
# =============================================================================
def diff_count(from_codon, to_codon):
    count = 0
    if from_codon[0] != to_codon[0]: count += 1
    if from_codon[1] != to_codon[1]: count += 1
    if from_codon[2] != to_codon[2]: count += 1
    return count

def load_json(filename):
    #print("() Loading:", filename)
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    TH = json_data["Evidence Ratios"]["Three-hit"][0]
    DH = json_data["Evidence Ratios"]["Two-hit"][0]
    SITES = json_data["input"]["number of sites"] #can also calculated from the len of DH or TH
    return TH, DH, np.arange(1, int(SITES) + 1)


def plotly_subplot():
    fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))

    print("here")
    
    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]),
                  row=1, col=1)
    
    fig.add_trace(go.Scatter(x=[20, 30, 40], y=[50, 60, 70]),
                  row=1, col=2)
    
    fig.add_trace(go.Scatter(x=[300, 400, 500], y=[600, 700, 800]),
                  row=2, col=1)
    
    fig.add_trace(go.Scatter(x=[4000, 5000, 6000], y=[7000, 8000, 9000]),
                  row=2, col=2)
    
    fig.update_layout(height=500, width=700,
                      title_text="Multiple Subplots with Titles")
    
    #fig.show()
    plot(fig) #auto_open=False for sanity.


def plotly_subplot_mod(data_x, data_y_TH, data_y_DH, output_title, output):
    
    """
    Arguments are all lists of lists, and the number of elements should match up.
    
    tx2_Ln_EvidenceRatio_TH
    
    """
    global THRESHOLD_TH_VALUE
    #how many elements do we have?
    num_items = len(data_x)
    print("Number of items:", num_items)
    #lets force a fixed column number = 10
    num_cols = 10
    
    num_rows = int(num_items / num_cols) + 1
    
    print("Rows X Columns:", num_rows, num_cols)
    
    for item in output_title:
        #item.replace("Euteleostomi.", "")
        #rplace .nex.FITTER.json
        #item.replace(".nex.FITTER.json", "")
        #item.replace(".nex.FITTER.json", "")
        pass
        
    subplot_titles = output_title
    
    #fig = make_subplots(
    #rows=2, cols=2,
    #subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))
    
    fig = make_subplots(rows = num_rows, cols = num_cols, subplot_titles = subplot_titles)
    

    #print("here")
    
    row_count = 1
    col_count = 1
    
    horizontal_line = []
    plot_count = 1
    
    for item in range(num_items): # just the count.
        if col_count == 11:
            row_count += 1
            col_count = 1
        
        #print("Adding:", row_count, col_count)
        
        fig.add_trace(go.Scatter(x=data_x[item], y=data_y_TH[item], opacity=0.75),
                  row=row_count, col=col_count)
        
        fig.add_trace(go.Scatter(x=data_x[item], y=data_y_DH[item], opacity=0.75),
                  row=row_count, col=col_count)
        
        Threshold_TH = THRESHOLD_TH_VALUE * np.mean(data_y_TH[item])
        #print("TH threshold multiplier:", THRESHOLD_TH_VALUE)
        horizontal_line.append({'type': 'line','y0':Threshold_TH,'y1': Threshold_TH,'x0':0, 
                              'x1':len(data_y_TH[item]),
                              'xref':'x' + str(plot_count),
                              'yref':'y' + str(plot_count),
                              'line': {'color': 'black','width': 1}})
        
        col_count += 1
        plot_count += 1
        
        
    """
    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]),
                  row=1, col=1)
    
    fig.add_trace(go.Scatter(x=[20, 30, 40], y=[50, 60, 70]),
                  row=1, col=2)
    
    fig.add_trace(go.Scatter(x=[300, 400, 500], y=[600, 700, 800]),
                  row=2, col=1)
    
    fig.add_trace(go.Scatter(x=[4000, 5000, 6000], y=[7000, 8000, 9000]),
                  row=2, col=2)
    
    """
    """
    hzln = {'type': 'line','y0':50,'y1': 50,'x0':0, 
                              'x1':1000,
                              'xref':'x1',
                              'yref':'y1',
                              'line': {'color': 'red','width': 2}}
    """
    
    #fig['layout'].update(shapes=[hzln])
    #for hz in horizontal_line:
    #    fig['layout'].update(shapes=[hz])
    #print(horizontal_line)
    
    fig['layout'].update(shapes=horizontal_line)
    
    for i in fig['layout']['annotations']:
        #i['font'] = dict(size=10,color='#ff0000')
        i['font'] = dict(size=4)
    
    fig.update_layout(height=700, width=1400,
                      title_text="Spatial analysis, [THvsDH (LRT, p<=0.05)] (X axis = Site, Y axis = 2[ln(ER)]")
    
    #fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='crimson', size=14))
    fig.update_xaxes(tickfont=dict(size=6))
    fig.update_yaxes(tickfont=dict(size=6))
    
    #fig.show()
    fig.update_layout(showlegend=False)
    
    
    
    
    
    plot(fig) #auto_open=False for sanity.
    
    


def plotly_basicline(data_x, data_y_TH, data_y_DH, output_title, output):
    global output_dir
    
    trace0 = go.Scatter(x = data_x, y = data_y_TH, mode = 'lines+markers', name="Three Hit", opacity=0.75)
    trace1 = go.Scatter(x = data_x, y = data_y_DH, mode = 'lines+markers', name="Double Hit", opacity=0.75)
    
    data = [trace0, trace1]
    
    layout = dict(title = '2*LN(Evidence Ratio), Number of Sites = ' + str(len(data_x)) + ", " + output_title, 
                  xaxis = dict(title = 'SITE'), 
                  yaxis = dict(title = '2*LN(Evidence Ratio)'),)
    
    fig = dict(data=data, layout=layout)
    
    #output_file = os.path.join(output_dir, output_title + ".html")
    output_file = output_title + ".html"
    print("() SAVING:", output_file)
    
    plot(fig, filename=output_file, auto_open=True) #auto_open=False for sanity.


def EvidenceRatio_threshold(filename):
    global THRESHOLD_TH_VALUE
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    EvidenceRatio_TH = json_data["Evidence Ratios"]["Three-hit"][0]
    Threshold_TH = THRESHOLD_TH_VALUE * np.mean(EvidenceRatio_TH)
    site_info = []
    for n, i in enumerate(EvidenceRatio_TH):
        if float(i) > Threshold_TH:
            site_info.append(n)
    return site_info

    
def pvalue_thresholded(filename):
    global pvalue_threshold
    
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    THvsDH_LRT_pvalue = json_data["test results"]["Triple-hit vs double-hit"]["p-value"]
    
    if float(THvsDH_LRT_pvalue) > pvalue_threshold: 
        return False
    else:
        return True

# =============================================================================
# Main subroutne
# =============================================================================

#plotly_subplot()
#sys.exit(1)


files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(".json")]


print("Total number of files (.json):", len(files))


count = 0
thresholded_files = []
for filename in files:
    if pvalue_thresholded(filename):
        thresholded_files.append(filename) #holds the thresholded files
        count += 1
print("Files which pass p-value threshold THvsDH (LRT, p<=0.05):", count)


count = 0
for filename in files:
    if len(EvidenceRatio_threshold(filename)) > 0:
        count += 1
print("Number of files which have 1 TH site 10x above the Evidence Ratio mean?", count)

count = 0
x10_thresholded_files = []
for filename in thresholded_files:
    if len(EvidenceRatio_threshold(filename)) > 0: #returns the site where ER is at least 10x above mean
        x10_thresholded_files.append(filename) #holds the 10x above mean thresholded files
        count += 1
print("Number of THRESHOLDED files which have 1 TH site 10x above the Evidence Ratio mean?", count)



#Lets raise the mean multiplier
count = 0
THRESHOLD_TH_VALUE = 50
x50_thresholded_files = []
for filename in thresholded_files:
    if len(EvidenceRatio_threshold(filename)) > 0: #returns the site where ER is at least 10x above mean
        x50_thresholded_files.append(filename) #holds the 10x above mean thresholded files
        count += 1
print("Number of THRESHOLDED files which have 1 TH site 50x above the Evidence Ratio mean?", count)

#return it back to "normal"
THRESHOLD_TH_VALUE = 10 #MAKE SURE THIS AGREES WITH ITS INIT. IN DECLARES


count = 0
x3_x10_thresholded_files = []
for filename in thresholded_files:
    if len(EvidenceRatio_threshold(filename)) >= 3: #returns the site where ER is at least 10x above mean
        x3_x10_thresholded_files.append(filename) #holds the 10x above mean thresholded files
        count += 1
print("Number of THRESHOLDED files which have 3 TH site 10x above the Evidence Ratio mean?", count)


#lets compare the above.
#print("How many of these files are in common?:", len(set(thresholded_files).symmetric_difference(set(x10_thresholded_files))))
#print("How many of these files are in common?:", len(set(x10_thresholded_files).symmetric_difference(set(thresholded_files))))

""" take the first couple and subplot """

subplot_Sites = []
subplot_tx2_Ln_EvidenceRatio_TH = []
subplot_tx2_Ln_EvidenceRatio_DH = []
subplot_output_title = []
subplot_filename = []

#for filename in x10_thresholded_files:
for filename in x3_x10_thresholded_files:

#for filename in x50_thresholded_files:
    EvidenceRatio_TH, EvidenceRatio_DH, Sites = load_json(filename)
    
    #Transform evidence ratios by applying 2*LN(evidence_ratio)
    #np.log is the natural log
    #np,log10 is base 10
    
    tx2_Ln_EvidenceRatio_TH = 2 * np.log(EvidenceRatio_TH) 
    tx2_Ln_EvidenceRatio_DH = 2 * np.log(EvidenceRatio_DH)
    
    #print("()MAINSUB[2]:", filename)
    #Plot (simple line) the two traces on the same plot.
    
    output_title = filename.split("/")[-1]
    
    #plotly_basicline(Sites, tx2_Ln_EvidenceRatio_TH, tx2_Ln_EvidenceRatio_DH, output_title, filename)
    
    #Need to store the above for later.
    
    subplot_Sites.append(Sites)
    subplot_tx2_Ln_EvidenceRatio_TH.append(tx2_Ln_EvidenceRatio_TH)
    subplot_tx2_Ln_EvidenceRatio_DH.append(tx2_Ln_EvidenceRatio_DH)
    subplot_output_title.append(output_title)
    subplot_filename.append(filename)
    

print("Plotting")
plotly_subplot_mod(subplot_Sites, subplot_tx2_Ln_EvidenceRatio_TH, subplot_tx2_Ln_EvidenceRatio_DH, subplot_output_title, subplot_filename)
    
    
    






# =============================================================================
# End of file
# =============================================================================
