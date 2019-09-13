#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 14:16:29 2019

@author: alexander lucaci

https://plot.ly/python/scientific-charts/

https://plot.ly/python/box-plots/
"""
# =============================================================================
# Imports
# =============================================================================
import plotly
import plotly.graph_objs as go
import plotly.graph_objects as go
from plotly import tools
import numpy as np 
from scipy import stats
import sys
import os
import json
import ast
import re

# =============================================================================
# Declares
# =============================================================================
fname = sys.argv[1]

#output_dir = "../analysis/SELECTOME_SRV/Plots/"

output_dir = sys.argv[2]
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
path = sys.argv[3] # FITTERS
    
#fname = "Vertebrate_mtDNA.csv"
num_seqs = []
num_sites = []
Dh_vs_Sh = []
TripleH_rates = []
Genename_TripleH = []
significant_LRTpvalue = [0, 0, 0]
columns = ['File name', 'number of sequences', 'number of sites', 'Double-hit vs single-hit - LRT', 'Double-hit vs single-hit - p-value', 'Triple-hit vs double-hit - LRT', 'Triple-hit vs double-hit - p-value', 'Triple-hit vs single-hit - LRT', 'Triple-hit vs single-hit - p-value', 'MG94 with double and triple instantaneous substitutions - AIC-c', 'MG94 with double and triple instantaneous substitutions - Log Likelihood', 'Substitution rate from nucleotide A to nucleotide C', 'Substitution rate from nucleotide A to nucleotide G', 'Substitution rate from nucleotide A to nucleotide T', 'Substitution rate from nucleotide C to nucleotide G', 'Substitution rate from nucleotide C to nucleotide T', 'Substitution rate from nucleotide G to nucleotide T', 'non-synonymous/synonymous rate ratio', 'rate at which 2 nucleotides are changed instantly within a single codon', 'rate at which 3 nucleotides are changed instantly within a single codon', 'MG94 with double instantaneous substitutions - AIC-c', 'MG94 with double instantaneous substitutions - Log Likelihood', 'Substitution rate from nucleotide A to nucleotide C', 'Substitution rate from nucleotide A to nucleotide G', 'Substitution rate from nucleotide A to nucleotide T', 'Substitution rate from nucleotide C to nucleotide G', 'Substitution rate from nucleotide C to nucleotide T', 'Substitution rate from nucleotide G to nucleotide T', 'non-synonymous/synonymous rate ratio', 'rate at which 2 nucleotides are changed instantly within a single codon', 'Standard MG94 - AIC-c', 'Standard MG94 - Log Likelihood', 'Substitution rate from nucleotide A to nucleotide C', 'Substitution rate from nucleotide A to nucleotide G', 'Substitution rate from nucleotide A to nucleotide T', 'Substitution rate from nucleotide C to nucleotide G', 'Substitution rate from nucleotide C to nucleotide T', 'Substitution rate from nucleotide G to nucleotide T', 'non-synonymous/synonymous rate ratio']

AICc = [[], [], []]
diff_AICc = [[], [], []]
LL = [[], [], []]

omegas = [[], [], []]
omegas_pvaluethreshold_THvsDH = [[], [], []]
omegas_pvaluethreshold_DHvsSH = [[], [], []]
omegas_pvaluethreshold_THvsSH = [[], [], []]

TH_distributions = [[], [], []] #25
DH_distributions = [[], [], []] #41
SH_distributions = [[], [], []] #56

TestResults_pvalues = [[], [], []]
LRTs = [[], [], []]

sig_LRTs = [[], [], []]
sig_LRTs_counts = [0, 0, 0]

pvalue_threshold = 0.05

# =============================================================================
# Helper functions
# =============================================================================
def subplot_boxplot(asizes, adesc, species, title, xaxislabel, filename):
    #plotly.offline.init_notebook_mode(connected=False)
    trace0 = go.Box(y=asizes[0], text=adesc[0], name=species[0])
    trace1 = go.Box(y=asizes[1], text=adesc[1], name=species[1])
    trace2 = go.Box(y=asizes[2], text=adesc[2], name=species[2])
    fig = go.Figure(data=[trace0, trace1, trace2])
    fig["layout"].update(title=title)
    output_filename = output_dir+fname.replace(".csv", "").split("/")[-1]
    plotly.offline.plot(fig, filename=output_filename+filename+"_SUBPLOT_Boxplot.html")

def subplot_binnedHisto(asizes, adesc, species, title, xaxislabel, filename):
    #plotly.offline.init_notebook_mode(connected=False)
    trace0 = go.Histogram(x=asizes[0], text=adesc[0], name=species[0], ybins=dict(size=0.01))
    trace1 = go.Histogram(x=asizes[1], text=adesc[1], name=species[1], ybins=dict(size=0.01))
    trace2 = go.Histogram(x=asizes[2], text=adesc[2], name=species[2], ybins=dict(size=0.01))
    fig = go.Figure(data=[trace0, trace1, trace2])
    fig["layout"].update(title=title)
    output_filename = output_dir+fname.replace(".csv", "").split("/")[-1]
    plotly.offline.plot(fig, filename=output_filename+filename+"_SUBPLOT_BinnedHistogram.html")

def subplot_histogram(asizes, adesc, species, title, xaxislabel, filename):
    #plotly.offline.init_notebook_mode(connected=False)
    trace0 = go.Histogram(x=asizes[0], text=adesc[0], name=species[0])
    trace1 = go.Histogram(x=asizes[1], text=adesc[1], name=species[1])
    trace2 = go.Histogram(x=asizes[2], text=adesc[2], name=species[2])
    
    #fig = tools.make_subplots(rows=3, cols=1, subplot_titles=(species[0], species[1],species[2]))
    fig = plotly.subplots.make_subplots(rows=3, cols=1, subplot_titles=(species[0], species[1],species[2]))
    #xaxis, yaxis
    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 2, 1)
    fig.append_trace(trace2, 3, 1)
    fig["layout"].update(title=title)
    fig['layout']['xaxis1'].update(title=xaxislabel)
    fig['layout']['yaxis1'].update(title='Occurences')
    output_filename = output_dir+fname.replace(".csv", "").split("/")[-1]
    plotly.offline.plot(fig, filename=output_filename+filename+"_SUBPLOT_HISTOGRAM.html")

def subplot_histogram_morebins(asizes, adesc, species, title, xaxislabel, filename):
    #global asizes, afilename, adesc
    #plotly.offline.init_notebook_mode(connected=False)
    #trace3 = go.Histogram(x=asizes[3], name=species[3])
    trace0 = go.Histogram(x=asizes[0], text=adesc[0], name=species[0], nbinsx = 100) #
    trace1 = go.Histogram(x=asizes[1], text=adesc[1], name=species[1], nbinsx = 100) #
    trace2 = go.Histogram(x=asizes[2], text=adesc[2], name=species[2], nbinsx = 100) #
    
    #fig = tools.make_subplots(rows=3, cols=1, subplot_titles=(species[0], species[1],species[2]))
    fig = plotly.subplots.make_subplots(rows=3, cols=1, subplot_titles=(species[0], species[1],species[2]))
    
    #xaxis, yaxis
    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 2, 1)
    fig.append_trace(trace2, 3, 1)
    fig["layout"].update(title=title)
    fig['layout']['xaxis1'].update(title=xaxislabel)
    fig['layout']['yaxis1'].update(title='Occurences')
    output_filename = output_dir+fname.replace(".csv", "").split("/")[-1]
    
    plotly.offline.plot(fig, filename=output_filename+filename+"_SUBPLOT_HISTOGRAM_morebins.html")

def plot_histogram_morebins_overlayed(asizes, adesc, species, title, xaxislabel, filename):
    #plotly.offline.init_notebook_mode(connected=False)
    trace0 = go.Histogram(x=asizes[0], text=adesc[0], name=species[0], nbinsx = 100, opacity=0.75) #
    trace1 = go.Histogram(x=asizes[1], text=adesc[1], name=species[1], nbinsx = 100, opacity=0.75) #
    trace2 = go.Histogram(x=asizes[2], text=adesc[2], name=species[2], nbinsx = 100, opacity=0.75) #
    data =[trace0, trace1, trace2]
    layout = go.Layout(barmode='overlay')
    fig = go.Figure(data=data, layout=layout)
    fig["layout"].update(title=title)
    fig['layout']['xaxis1'].update(title=xaxislabel)
    fig['layout']['yaxis1'].update(title='Occurences')
    output_filename = output_dir+fname.replace(".csv", "").split("/")[-1]
    #plotly.offline.plot(fig, filename=output_filename+filename+"_HISTOGRAM_morebins_overlayed.html")
    fig.show()

def plotly_things(numbers, filename, desc1, desc2, desc3): #single historgram
    output_filename = output_dir+fname.replace(".csv", "").split("/")[-1]
    
    #plotly.offline.init_notebook_mode(connected=False)
    
    #plotly.offline.plot({"data": [go.Histogram(x=numbers, text=desc3, nbinsx=450)],"layout": go.Layout(title=desc2, xaxis={'title':desc1}, yaxis={'title':'Occurences'})},filename=output_filename+filename+"_HISTOGRAM.html")
    #print("Saving to file:", output_filename+filename+"_HISTOGRAM.html")
    #print(output_filename)
    #print(filename)
    plotly.offline.plot({"data": [go.Histogram(x=numbers, text=desc3, xbins=dict(size=0.25))],"layout": go.Layout(title=desc2, xaxis={'title':desc1}, yaxis={'title':'Occurences'})},filename=output_filename+filename+"_HISTOGRAM.html")

def plotly_boxplot(numbers, filename, desc1, desc2, desc3): #Single boxplot
    #plotly.offline.init_notebook_mode(connected=False)
    plotly.offline.plot({"data": [go.Box(x=numbers, text=desc3)],"layout": go.Layout(title=desc2, xaxis={'title':desc1}, yaxis={'title':'Occurences'})},filename=filename+"_Boxplot.html")

    
def pass_pvalue_threshold(filename):
    global pvalue_threshold
    
    
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    file_pvalue = json_data["test results"]["Triple-hit vs double-hit"]["p-value"]
    
    
    #print(filename, file_pvalue)
    if float(file_pvalue) < pvalue_threshold:
        passed = True
    else:
        passed = False
        
    return passed



def grouped_boxplot_fromwebsite():
    x = ['day 1', 'day 1', 'day 1', 'day 1', 'day 1', 'day 1',
         'day 2', 'day 2', 'day 2', 'day 2', 'day 2', 'day 2']
    x = ["rate 1"] * 6
    x += ["rate 2"] * 6
    x += ["rate 3"] * 6
    
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=[0.2, 0.2, 0.6, 1.0, 0.5, 0.4, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        x=x,
        name='kale',
        marker_color='#3D9970'
    ))
    fig.add_trace(go.Box(
        y=[0.6, 0.7, 0.3, 0.6, 0.0, 0.5, 0.7, 0.9, 0.5, 0.8, 0.7, 0.2, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        x=x,
        name='radishes',
        marker_color='#FF4136'
    ))
    fig.add_trace(go.Box(
        y=[0.1, 0.3, 0.1, 0.9, 0.6, 0.6, 0.9, 1.0, 0.3, 0.6, 0.8, 0.5, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        x=x,
        name='carrots',
        marker_color='#FF851B'
    ))
    
    fig.update_layout(
        yaxis_title='normalized moisture',
        boxmode='group' # group together boxes of the different traces for each value of x
    )
    fig.show()


def grouped_boxplot_fromwebsite_mod(TH, DH, SH):
    #x = ['day 1', 'day 1', 'day 1', 'day 1', 'day 1', 'day 1',
    #     'day 2', 'day 2', 'day 2', 'day 2', 'day 2', 'day 2']
    
    
    
    print("TH rate 1:", len(TH[0]))
    print("DH rate 1:",len(DH[0]))
    print("SH rate 1:",len(SH[0]))
    
    sum_files = 0
    
    
    for n in range(2):
        print(len(TH[n]))
        print(len(DH[n]))
        print(len(SH[n]))
        
    
    #x = ["rate 1"] * 6
    #x += ["rate 2"] * 6
    #x += ["rate 3"] * 6
    """
    #TH rate 1
    x = ["rate 1"] * len(TH[0]) 
    #DH rate 1
    x += ["rate 1"] * len(DH[0]) 
    #SH rate 1
    x += ["rate 1"] * len(SH[0]) 
    
    #TH rate 2
    x += ["rate 2"] * len(TH[1]) 
    #DH rate 2
    x += ["rate 2"] * len(DH[1]) 
    #SH rate 2
    x += ["rate 2"] * len(SH[1]) 
    
    print(len(x))
    
    #TH rate 3
    x += ["rate 3"] * len(TH[2])
    #DH rate 3
    x += ["rate 3"] * len(DH[2])
    #SH rate 3
    x += ["rate 3"] * len(SH[2])
    """
    
    #y = TH[0] + TH[1]
    #print(len(y))
    fig = go.Figure()
    #Y needs to be the same length as X
    #y = [0.2, 0.2, 0.6, 1.0, 0.5, 0.4, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3]
    
    fig.add_trace(go.Box(
        #y=[10, 0.2, 0.6, 1.0, 0.5, 0.4, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        #y=TH[0]+TH[1]+TH[2],
        y=TH[0] + TH[1] + TH[2],
        x=["rate category 1"] * len(TH[0]) + ["rate category 2"] * len(TH[0]) + ["rate category 3"] * len(TH[2]),
        name='TH', # so all the kales
        marker_color='#3D9970'
    ))
    fig.add_trace(go.Box(
        #y=[100, 0.7, 0.3, 0.6, 0.0, 0.5, 0.7, 0.9, 0.5, 0.8, 0.7, 0.2, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        #y=DH[0]+DH[1]+DH[2],
        y=DH[0] + DH[1] + DH[2],
        x=["rate category 1"] * len(DH[0]) +  ["rate category 2"] * len(DH[1]) +  ["rate category 3"] * len(DH[2]),
        name='DH',
        marker_color='#FF4136'
    ))
    fig.add_trace(go.Box(
        #rate 1..........................rate 2
        #y=[1000, 0.3, 0.1, 0.9, 0.6, 0.6, 500, 1.0, 0.3, 0.6, 0.8, 0.5, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        #y=SH[0]+SH[1]+SH[2],
        y=SH[0] + SH[1] + SH[2],
        x=["rate category 1"] * len(TH[0]) + ["rate category 2"] * len(TH[1]) + ["rate category 3"] * len(TH[2]),
        name='SH',
        marker_color='#FF851B'
    ))
    
    fig.update_layout(
        yaxis_title='Omega value',
        boxmode='group' # group together boxes of the different traces for each value of x
    )
    fig.show()


def grouped_boxplot_sample(TH, DH, SH):
    #https://plot.ly/python/box-plots/
    import plotly.graph_objects as go

    #x = ["rate 1"] * 6
    #x += ["rate 2"] * 6
    #x += ["rate 3"] * 6
    
    """
    print("TH:", len(TH[0]))
    print(len(DH[0]))
    print(len(SH[0]))
    
    print("TH:", len(TH[1]))
    print(len(DH[1]))
    print(len(SH[1]))
    
    print("TH:", len(TH[2]))
    print(len(DH[2]))
    print(len(SH[2]))
    """
    
    x = ["rate 1"] * (len(TH[0]) + len(DH[0]) + len(SH[0]))
    x += ["rate 2"] * (len(TH[1]) + len(DH[1]) + len(SH[1]))
    x += ["rate 3"] * (len(TH[2]) + len(DH[2]) + len(SH[2]))
    
    print(x)
    
    fig = go.Figure()
    """
    Figures 1
    Figures 2
    Figures 3 in each of the 3 rate categories
    
    The y breakdown is as follows
    
    In Figure 3
    The first 6 belong to rate 1
    The middle 6 belong to rate 2
    The final 6 belong to rate 3
    
    
    """
    fig.add_trace(go.Box(
        #y=[0.2, 0.2, 0.6, 1.0, 0.5, 0.4, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        y = TH[0] + DH[0] + SH[0],
        x=x,
        name='TH',
        marker_color='#3D9970'
    ))
    
    fig.add_trace(go.Box(
        #y=[0.6, 0.7, 0.3, 0.6, 0.0, 0.5, 0.7, 0.9, 0.5, 0.8, 0.7, 0.2, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        y = TH[1] + DH[1] + SH[1],
        x=x,
        name='DH',
        marker_color='#FF4136'
    ))
    
    fig.add_trace(go.Box(   
        #y=[0.1, 0.3, 0.1, 0.9, 0.6, 0.6, 0.9, 1.0, 0.3, 0.6, 0.8, 0.5, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        y = TH[2] + DH[2] + SH[2],
        x=x,
        name='SH',
        marker_color='#FF851B'
    ))
    
    fig.update_layout(
        yaxis_title='normalized moisture',
        boxmode='group' # group together boxes of the different traces for each value of x
    )
    fig.show()
    
    
    
    

def grouped_boxplot(TH, DH, SH):
    import plotly.graph_objects as go

    #x = ['day 1', 'day 1', 'day 1', 'day 1', 'day 1', 'day 1', 'day 2', 'day 2', 'day 2', 'day 2', 'day 2', 'day 2']
    #print(len(TH[9]), len(DH[0], ))
    """
    #TH rate 1
    x = ["rate 1"] * len(TH[0]) 
    #DH rate 1
    x += ["rate 1"] * len(DH[0]) 
    #SH rate 1
    x += ["rate 1"] * len(SH[0]) 
    
    #TH rate 2
    x += ["rate 2"] * len(TH[1]) 
    #DH rate 2
    x += ["rate 2"] * len(DH[1]) 
    #SH rate 2
    x += ["rate 2"] * len(SH[1]) 
    
    #TH rate 3
    x += ["rate 3"] * len(TH[2])
    #DH rate 3
    x += ["rate 3"] * len(DH[2])
    #SH rate 3
    x += ["rate 3"] * len(SH[2])
    """
    
    x = ["rate 1"] * (len(TH[0]) + len(DH[0]) + len(SH[0]))
    print(len(x))
    x += ["rate 2"] * (len(TH[1]) + len(DH[1]) + len(SH[1]))
    print(len(x))
    x += ["rate 3"] * (len(TH[2]) + len(DH[2]) + len(SH[2]))
    print("x3:", len(x))


    """    
    y1 = TH[0] + DH[0] + SH[0]
    print(len(y1))
    
    y2 = TH[1] + DH[1] + SH[1]
    print(type(y2), len(y2))
    
    y3 = TH[2] + DH[2] + SH[2]
    print(len(y3))
    
    print("y:", len(y1+y2+y3))
    """
    
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        #y=[0.2, 0.2, 0.6, 1.0, 0.5, 0.4, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        y = TH[0] + DH[0] + SH[0],
        x=x,
        name='kale',
        marker_color='#3D9970'
    ))
    fig.add_trace(go.Box(
        #y=[0.6, 0.7, 0.3, 0.6, 0.0, 0.5, 0.7, 0.9, 0.5, 0.8, 0.7, 0.2, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        y = TH[1] + DH[1] + SH[1],
        x=x,
        name='radishes',
        marker_color='#FF4136'
    ))
    fig.add_trace(go.Box(
        #y=[0.1, 0.3, 0.1, 0.9, 0.6, 0.6, 0.9, 1.0, 0.3, 0.6, 0.8, 0.5, 0.2, 0.7, 0.9, 0.1, 0.5, 0.3],
        y = TH[2] + DH[2] + SH[2],
        x=x,
        name='carrots',
        marker_color='#FF851B'
    ))
    
    fig.update_layout(
        yaxis_title='normalized moisture',
        boxmode='group' # group together boxes of the different traces for each value of x
    )
    fig.show()


# =============================================================================
# Main subroutine
# =============================================================================
print("CSV FILE:", fname)

with open(fname, "r") as f: #THE CSV FILE
    count = 0
    numlines = 0
    SIG_THvsDH = 0 #Number of files with triple hit rate > 1.0 and Significant (p<0.05) Proportion Triple-hit vs double-hit (%)
    SIG_THvsSH = 0 #Number of files with triple hit rate > 1.0 and Significant (p<0.05) Proportion Triple-hit vs single-hit (%)
    SIG_THvsDHorTHvsSH = 0
    SIG_DHvsSH = 0
    count_timp_TH = 0
    count_timp_DH = 0 
    count_timp_SH = 0
    while True:
        line = f.readline().strip()
        if line == "": break
    
        if count == 0:
            count += 1
            continue #Skip header line
            
        numlines += 1
        
        
        data = line.split(",") #header
        
        #start measuring the data
        
        num_seqs.append(int(data[1]))
        num_sites.append(int(data[2]))
        
        TripleH_rates.append(float(data[19]))
            
        if float(data[19]) > 1.0: #data[19] = "rate at which 3 nucleotides are changed instantly within a single codon"
            Genename_TripleH.append([float(data[19]), data[0]]) # <- ADD THIS FUNCTIONALITY TO THE CSV PARSER. WHICH GENES with rates above 1.0, names, space demilited and values space delmiited
        
            if float(data[6]) < pvalue_threshold: #Triple-hit vs double-hit
                #print(float(data[6]), float(data[8]))
                SIG_THvsDH += 1
                #print(data[0]+".FITTER.json", data[1], data[2])
                
            if float(data[8]) < pvalue_threshold: #Triple-hit vs single-hit
                SIG_THvsSH += 1
                
            if float(data[6]) < pvalue_threshold or float(data[8]) < pvalue_threshold:
                SIG_THvsDHorTHvsSH +=1
                
            if float(data[4]) < pvalue_threshold: #Double-hit vs single-hit - p-value
                SIG_DHvsSH += 1
                   
        #Significant non-zero Triple Hits
        if float(data[6]) < pvalue_threshold: significant_LRTpvalue[0] += 1 #counts 
           #print(data[8])
        if float(data[8]) < pvalue_threshold: significant_LRTpvalue[1] += 1 #counts
            #print("SIG",data[8])
        if float(data[4]) < pvalue_threshold: significant_LRTpvalue[2] += 1 #counts
        
        #AICc
        AICc[0].append(float(data[9])) #MG94 with double and triple instantaneous substitutions - AIC-c
        AICc[1].append(float(data[31])) #MG94 with double instantaneous substitutions - AIC-c
        AICc[2].append(float(data[52])) #Standard MG94 - AIC-c
        
        #AICc Differences between them.
        diff_AICc[0].append(float(data[52]) - float(data[31])) #Difference AICc 1H vs 2H
        diff_AICc[1].append(float(data[52]) - float(data[9])) #Difference AICc 1H vs 3H
        diff_AICc[2].append(float(data[31]) - float(data[9])) #Difference AICc 2H vs 3H
    
        #log(L)
        LL[0].append(float(data[10])) #MG94 with double and triple instantaneous substitutions - Log Likelihood
        LL[1].append(float(data[32])) #MG94 with double instantaneous substitutions - Log Likelihood
        LL[2].append(float(data[53])) #Standard MG94 - Log Likelihood
        
        #LRTs
        LRTs[0].append(float(data[3])) #Double-hit vs single-hit
        LRTs[1].append(float(data[5])) #Triple-hit vs double-hit
        LRTs[2].append(float(data[7])) #Triple-hit vs single-hit 
        
        #Significant LRTs
        if float(data[4]) < pvalue_threshold:
            sig_LRTs[0].append(float(data[3])) #Double-hit vs single-hit
        if float(data[6]) < pvalue_threshold:
            sig_LRTs[1].append(float(data[5])) #Triple-hit vs double-hit
        if float(data[8]) < pvalue_threshold:
            sig_LRTs[2].append(float(data[7])) #Triple-hit vs single-hit 
                 
        #Omegas
        omegas[0].append(float(data[17])) #MG94 with double and triple instantaneous substitutions
        omegas[1].append(float(data[39])) #MG94 with double instantaneous substitutions
        omegas[2].append(float(data[60])) #Standard MG94
        
        
        #Omegas pvalue thresholded 
        
        
        #this is accessing the CSV and reading line by line.
        
        
        #if pass_pvalue_threshold(fname) == True: 
        if float(data[6]) < pvalue_threshold: ##TH vs DH LRT pvalue
            #omegas_pvaluethreshold_THvsDH[0].append(float(data[17]))
            omegas_pvaluethreshold_THvsDH[0].append(float(data[17])) #MG94 with double and triple instantaneous substitutions
            omegas_pvaluethreshold_THvsDH[1].append(float(data[39])) #MG94 with double instantaneous substitutions
            omegas_pvaluethreshold_THvsDH[2].append(float(data[60])) #Standard MG94
        
        if float(data[4]) < pvalue_threshold: #DH vs SH LRT pvalue
            omegas_pvaluethreshold_THvsSH[0].append(float(data[17])) #MG94 with double and triple instantaneous substitutions
            omegas_pvaluethreshold_THvsSH[1].append(float(data[39])) #MG94 with double instantaneous substitutions
            omegas_pvaluethreshold_THvsSH[2].append(float(data[60])) #Standard MG94
            
        if float(data[8]) < pvalue_threshold: #TH vs SH LRT pvalue
            omegas_pvaluethreshold_DHvsSH[0].append(float(data[17])) #MG94 with double and triple instantaneous substitutions
            omegas_pvaluethreshold_DHvsSH[1].append(float(data[39])) #MG94 with double instantaneous substitutions
            omegas_pvaluethreshold_DHvsSH[2].append(float(data[60])) #Standard MG94
        
        
        #Test Results (p-values)
        TestResults_pvalues[0].append(float(data[4])) #Double-hit vs single-hit - p-value
        TestResults_pvalues[1].append(float(data[6])) #Triple-hit vs double-hit - p-value
        TestResults_pvalues[2].append(float(data[8])) #Triple-hit vs single-hit - p-value
        
        #print(ast.literal_evaldata([25]))
        x1 = data[25].replace("[", "").replace(" ", "").replace('"', '')
        x2 = data[27].replace("[", "").replace(" ", "")
        x3 = data[29].replace("[", "").replace(" ", "")
        #print("TH:", [x1], [x2],[x3])
        
        y1 = data[46].replace("[", "").replace(" ", "").replace('"', '')
        y2 = data[48].replace("[", "").replace(" ", "")
        y3 = data[50].replace("[", "").replace(" ", "")
        #print("DH:", [y1], [y2],[y3])
        
        z1 = data[66].replace("[", "").replace(" ", "").replace('"', '')
        z2 = data[68].replace("[", "").replace(" ", "")
        z3 = data[70].replace("[", "").replace(" ", "")
        #print("SH:", [z1], [z2],[z3])
        
        #print(len(data))
        
        #re.findall(r'"\s*([^"]*?)\s*"', x)
        #print(data[0], x)
        
        x_threshold = 25
        
        if float(x1) < x_threshold and float(x2) < x_threshold and float(x3) < x_threshold:
            TH_distributions[0].append(float(x1)) #TH rate 1
            TH_distributions[1].append(float(x2)) #TH rate 2
            TH_distributions[2].append(float(x3)) #TH rate 3
        else:
            print("TH violated:", count_timp_TH)
            count_timp_TH += 1
        
        if float(y1) < x_threshold and float(y2) < x_threshold and float(y3) < x_threshold:
            DH_distributions[0].append(float(y1)) #DH rate 1
            DH_distributions[1].append(float(y2)) #DH rate 3
            DH_distributions[2].append(float(y3)) #DH rate 1
        else:
            print("DH violated:", count_timp_DH)
            count_timp_DH += 1
           
        if float(z1) < x_threshold and float(z2) < x_threshold and float(z3) < x_threshold:
            SH_distributions[0].append(float(z1)) #SH rate 1
            SH_distributions[1].append(float(z2)) #SH rate 2
            SH_distributions[2].append(float(z3)) #SH rate 3
        else:
            print("SH violated:", count_timp_SH)
            count_timp_SH += 1
        
        
        """
        TH_distributions[0].append(data[25][0][0]) #TH rate 1
        TH_distributions[1].append(data[25][1][0]) #TH rate 2
        TH_distributions[2].append(data[25][2][0]) #TH rate 3
        
        DH_distributions[0].append(data[41][0][0]) #DH rate 1
        DH_distributions[1].append(data[41][1][0]) #DH rate 3
        DH_distributions[2].append(data[41][2][0]) #DH rate 1
        
        SH_distributions[0].append(data[56][0][0]) #SH rate 1
        SH_distributions[1].append(data[56][1][0]) #SH rate 2
        SH_distributions[2].append(data[56][2][0]) #SH rate 3
        """
        
    
        
        
        
        
       
"""    
files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(".json")] 
for file in files:
    if pass_pvalue_threshold(file) == True: 
        #omegas_pvaluethreshold_THvsDH[0].append(float(data[17]))
        omegas_pvaluethreshold_THvsDH[0].append(float(data[17])) #MG94 with double and triple instantaneous substitutions
        omegas_pvaluethreshold_THvsDH[1].append(float(data39])) #MG94 with double instantaneous substitutions
        omegas_pvaluethreshold_THvsDH[2].append(float(data[60])) #Standard MG94      
"""     

# =============================================================================
# Make plots here.
# =============================================================================  
     
#print(TH_distributions)
#print(omegas)

#print("Plotting")
#grouped_boxplot_sample(TH_distributions, DH_distributions, SH_distributions)
#grouped_boxplot_fromwebsite()
#grouped_boxplot_fromwebsite_mod(TH_distributions, DH_distributions, SH_distributions)
#grouped_boxplot(TH_distributions, DH_distributions, SH_distributions)

#sys.exit(50)

"""
grouped_boxplot(TH_distributions, DH_distributions, SH_distributions)

#sys.exit(3)

subplot_boxplot(TH_distributions, ["","",""], ["rate 1","rate 2","rate 3"], "Models comparison - TH rates", "TH", "TH_F")

print(stats.describe(TH_distributions[2]))
#sys.exit(2)
#for item in TH_distributions[2]: print(item, type(item))

subplot_boxplot(DH_distributions, ["","",""], ["rate 1","rate 2","rate 3"], "Models comparison - DH rates", "DH", "DH_F")

subplot_boxplot(SH_distributions, ["","",""], ["rate 1","rate 2","rate 3"], "Models comparison - SH rates", "SH", "SH_F")


subplot_boxplot([TH_distributions[0], DH_distributions[0], SH_distributions[0]], ["","",""], ["TH","DH","SH"], "Models comparison - THDHSH rate 1", "THDHSH", "THDHSH_rate1")

subplot_boxplot([TH_distributions[1], DH_distributions[1], SH_distributions[1]], ["","",""], ["TH","DH","SH"], "Models comparison - THDHSH rate 2", "THDHSH", "THDHSH_rate2")

subplot_boxplot([TH_distributions[2], DH_distributions[2], SH_distributions[2]], ["","",""], ["TH","DH","SH"], "Models comparison - THDHSH rate 3", "THDHSH", "THDHSH_rate3")
#sys.exit(1)
plotly_things(TripleH_rates, "_TH_RATES", "rate at which 3 nucleotides are changed instantly within a single codon", "Triple Mutation hit rate histogram", "Rate value")
"""


"""
plotly_things(num_seqs, "NUMSEQS", "Number of sequences", "Number of sequences analyzed per gene family", "Number of sequences analyzed per gene family")
plotly_things(num_sites, "NUMSITES", "Number of sites (Alignment length)", "Number of sites analyzed", "Number of sites aligned")

subplot_histogram(AICc, ["","",""], ["MG94 with double and triple instantaneous substitutions","MG94 with double instantaneous substitutions","Standard MG94"], "Models comparison - AICc", "AICc", "AICc")
subplot_histogram_morebins(AICc, ["","",""], ["MG94 with double and triple instantaneous substitutions","MG94 with double instantaneous substitutions","Standard MG94"], "Models comparison - AICc", "AICc", "AICc")
"""

#subplot_histogram_morebins(diff_AICc, ["","",""], ["Difference AICc 1H vs 2H", "Difference AICc 1H vs 3H","Difference AICc 2H vs 3H"], "Models comparison - difference of AICc", "Difference-AICc", "Difference-AICc")
plot_histogram_morebins_overlayed(diff_AICc, ["","",""], ["Difference AICc 1H vs 2H", "Difference AICc 1H vs 3H","Difference AICc 2H vs 3H"], "Models comparison - difference of AICc", "Difference-AICc", "Difference-AICc")

"""
subplot_histogram(LL, ["","",""], ["MG94 with double and triple instantaneous substitutions","MG94 with double instantaneous substitutions","Standard MG94"], "Models comparison - log(L)", "Log Likelihoods", "LogLikelihoods")

plotly_boxplot(num_sites, "NUMSITES", "Number of sites (Alignment length)", "Number of sites analyzed", "Number of sites aligned")     
subplot_boxplot(AICc, ["","",""], ["MG94 with double and triple instantaneous substitutions","MG94 with double instantaneous substitutions","Standard MG94"], "Models comparison - AICc", "AICc", "AICc")
"""

"""
subplot_boxplot(omegas, ["","",""], ["MG94 with double and triple instantaneous substitutions","MG94 with double instantaneous substitutions","Standard MG94"], "Models comparison - Omega values", "Omega", "Omega")
subplot_boxplot(omegas_pvaluethreshold_THvsDH, ["","",""], ["MG94 with double and triple instantaneous substitutions","MG94 with double instantaneous substitutions","Standard MG94"], "Models comparison - Omega values (pvalue thresholded) THvsDH", "Omega", "Omega_pvaluethreshold_THvsDH")
subplot_boxplot(omegas_pvaluethreshold_THvsSH, ["","",""], ["MG94 with double and triple instantaneous substitutions","MG94 with double instantaneous substitutions","Standard MG94"], "Models comparison - Omega values (pvalue thresholded) THvsSH", "Omega", "Omega_pvaluethreshold_THvsSH")
subplot_boxplot(omegas_pvaluethreshold_DHvsSH, ["","",""], ["MG94 with double and triple instantaneous substitutions","MG94 with double instantaneous substitutions","Standard MG94"], "Models comparison - Omega values (pvalue thresholded) DHvsSH", "Omega", "Omega_pvaluethreshold_DHvsSH")



#subplot_histogram(TestResults_pvalues, ["","",""], ["Double-hit vs single-hit - p-value","Triple-hit vs double-hit - p-value","Triple-hit vs single-hit - p-value"], "Models comparison - Fits, TestResults_pvalues", "TestResults_pvalues", "TestResults_pvalues")
subplot_histogram_morebins(TestResults_pvalues, ["","",""], ["Double-hit vs single-hit - p-value","Triple-hit vs double-hit - p-value","Triple-hit vs single-hit - p-value"], "Models comparison - Fits, TestResults_pvalues", "TestResults_pvalues", "TestResults_pvalues")
"""
#subplot_binnedHisto(TestResults_pvalues, ["","",""], ["Double-hit vs single-hit - p-value","Triple-hit vs double-hit - p-value","Triple-hit vs single-hit - p-value"], "Models comparison - Fits, TestResults_pvalues", "TestResults_pvalues", "TestResults_pvalues")

"""
subplot_boxplot(LRTs, ["","",""], ["Double-hit vs single-hit","Triple-hit vs double-hit","Triple-hit vs single-hit"], "Models comparison - LRT values", "LRTs", "LRTs")
subplot_boxplot(sig_LRTs, ["","",""], ["Double-hit vs single-hit","Triple-hit vs double-hit","Triple-hit vs single-hit"], "Models comparison - Significant (p<0.05) LRT values", "Significant LRTs", "sigLRTs")
"""

# =============================================================================
# Summary Statistics
# =============================================================================
n = numlines

print(" ##################################")
print(" ### --- SUMMARY STATISTICS --- ###")
print(" ##################################\n")
print("Triple Hit Rates max:", max(TripleH_rates), "min:", min(TripleH_rates), "N =", len(TripleH_rates))
TripleH_rates = np.asarray(TripleH_rates)
print(stats.describe(TripleH_rates))
print()

print("Number of files with triple hit rate > 1.0:", len(Genename_TripleH)) #NOW HAVE TO GO INTO EACH FILE AND PICK THE GENE NAMES WITH rates above 1 <- do in CSV creator.
print("^ and are significant (p<" + str(pvalue_threshold) + ") Triple-hit vs double-hit:", SIG_THvsDH)
print("^ and are significant (p<" + str(pvalue_threshold) + ") Triple-hit vs single-hit:", SIG_THvsSH)
print("^ and are significant (p<" + str(pvalue_threshold) + ") Triple-hit vs double-hit or Triple-hit vs single-hit:", SIG_THvsDHorTHvsSH, "\n")

#For what proportion of these rates was there a significant p-value for non-zero triple hits?
#if "rate at which 3 nucleotides are changed instantly within a single codon" > 0.0 then
#if "Triple-hit vs double-hit" or Triple-hit vs single-hit", p value < 0.05, count it and indicate which
print("Number of files: " + str(n), "\n", 
      "Significant (p<" + str(pvalue_threshold) + ") Proportion Triple-hit vs double-hit (%):", (significant_LRTpvalue[0]/n)*100, "\n", 
      "Significant (p<" + str(pvalue_threshold) + ") Proportion Triple-hit vs single-hit (%):", (significant_LRTpvalue[1]/n)*100, "\n",
      "Significant (p<" + str(pvalue_threshold) + ") Proportion Double-hit vs single-hit (%):", (significant_LRTpvalue[2]/n)*100)


print()
print("() Sites and sequences Summary Stats")
print("Average number of sequences:", sum(num_seqs)/ len(num_seqs))
print(stats.describe(np.asarray(num_seqs)))
print("Average number of sites:", sum(num_sites)/ len(num_sites))
print(stats.describe(np.asarray(num_sites)))


"""
#Omegas
omegas[0].append(float(data[17])) #MG94 with double and triple instantaneous substitutions
omegas[1].append(float(data[39])) #MG94 with double instantaneous substitutions
omegas[2].append(float(data[60])) #Standard MG94
"""
print()
print("() Omegas")
print("MG94 with double and triple instantaneous substitutions: ", stats.describe(np.asarray(omegas[0])))
print("MG94 with double instantaneous substitutions: ", stats.describe(np.asarray(omegas[1])))
print("Standard MG94: ", stats.describe(np.asarray(omegas[2])))

print()
print("() Omegas - pvalue theshold THvsDH")
print("MG94 with double and triple instantaneous substitutions: ", stats.describe(np.asarray(omegas_pvaluethreshold_THvsDH[0])))
print("MG94 with double instantaneous substitutions: ", stats.describe(np.asarray(omegas_pvaluethreshold_THvsDH[1])))
print("Standard MG94: ", stats.describe(np.asarray(omegas_pvaluethreshold_THvsDH[2])))


print()
print("() Omegas - pvalue theshold THvsDH")
print("MG94 with double and triple instantaneous substitutions: ", stats.describe(np.asarray(omegas_pvaluethreshold_THvsDH[0])))
print("MG94 with double instantaneous substitutions: ", stats.describe(np.asarray(omegas_pvaluethreshold_THvsDH[1])))
print("Standard MG94: ", stats.describe(np.asarray(omegas_pvaluethreshold_THvsDH[2])))

print()
print("() Omegas - pvalue theshold THvsSH")
print("MG94 with double and triple instantaneous substitutions: ", stats.describe(np.asarray(omegas_pvaluethreshold_THvsSH[0])))
print("MG94 with double instantaneous substitutions: ", stats.describe(np.asarray(omegas_pvaluethreshold_THvsSH[1])))
print("Standard MG94: ", stats.describe(np.asarray(omegas_pvaluethreshold_THvsSH[2])))

print()
print("() Omegas - pvalue theshold DHvsSH")
print("MG94 with double and triple instantaneous substitutions: ", stats.describe(np.asarray(omegas_pvaluethreshold_DHvsSH[0])))
print("MG94 with double instantaneous substitutions: ", stats.describe(np.asarray(omegas_pvaluethreshold_DHvsSH[1])))
print("Standard MG94: ", stats.describe(np.asarray(omegas_pvaluethreshold_DHvsSH[2])))

#print("AICc averages:", np.average(np_AICc[0]))
#print(np.average(np_AICc[1]))
#print(np.average(np_AICc[2]))



print()
np_AICc = np.asarray(AICc)
print("() AICc summary Stats")
print("#MG94 with double and triple instantaneous substitutions\n", stats.describe(np_AICc[0]))
print("#MG94 with double instantaneous substitutions\n", stats.describe(np_AICc[1]))
print("#Standard MG94\n", stats.describe(np_AICc[2]))
      
print()    
np_LL = np.asarray(LL)
print("() log(L) summary Stats")
print("#MG94 with double and triple instantaneous substitutions\n", stats.describe(np_LL[0]))
print("#MG94 with double instantaneous substitutions\n", stats.describe(np_LL[1]))
print("#Standard MG94\n", stats.describe(np_LL[2]))
      

      

# =============================================================================
# End of file
# =============================================================================