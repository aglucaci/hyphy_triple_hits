#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 14:16:29 2019

@author: alexander lucaci

https://plot.ly/python/scientific-charts/
"""
# =============================================================================
# Imports
# =============================================================================
import plotly
import plotly.graph_objs as go
from plotly import tools
import numpy as np 
from scipy import stats
import sys
import os

# =============================================================================
# Declares
# =============================================================================
fname = sys.argv[1]

#output_dir = "../analysis/SELECTOME_SRV/Plots/"

output_dir = sys.argv[2]
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
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
    fig = tools.make_subplots(rows=3, cols=1, subplot_titles=(species[0], species[1],species[2]))
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
    fig = tools.make_subplots(rows=3, cols=1, subplot_titles=(species[0], species[1],species[2]))
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
    plotly.offline.plot(fig, filename=output_filename+filename+"_HISTOGRAM_morebins_overlayed.html")

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

# =============================================================================
# Main subroutine
# =============================================================================

with open(fname) as f:
    count = 0
    numlines = 0
    SIG_THvsDH = 0 #Number of files with triple hit rate > 1.0 and Significant (p<0.05) Proportion Triple-hit vs double-hit (%)
    SIG_THvsSH = 0 #Number of files with triple hit rate > 1.0 and Significant (p<0.05) Proportion Triple-hit vs single-hit (%)
    SIG_THvsDHorTHvsSH = 0
    SIG_DHvsSH = 0

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
        
        #Test Results (p-values)
        TestResults_pvalues[0].append(float(data[4])) #Double-hit vs single-hit - p-value
        TestResults_pvalues[1].append(float(data[6])) #Triple-hit vs double-hit - p-value
        TestResults_pvalues[2].append(float(data[8])) #Triple-hit vs single-hit - p-value
        
# =============================================================================
# Make plots here.
# =============================================================================  
        

plotly_things(TripleH_rates, "_TH_RATES", "rate at which 3 nucleotides are changed instantly within a single codon", "Triple Mutation hit rate histogram", "Rate value")

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

subplot_boxplot(omegas, ["","",""], ["MG94 with double and triple instantaneous substitutions","MG94 with double instantaneous substitutions","Standard MG94"], "Models comparison - Omega values", "Omega", "Omega")

#subplot_histogram(TestResults_pvalues, ["","",""], ["Double-hit vs single-hit - p-value","Triple-hit vs double-hit - p-value","Triple-hit vs single-hit - p-value"], "Models comparison - Fits, TestResults_pvalues", "TestResults_pvalues", "TestResults_pvalues")
subplot_histogram_morebins(TestResults_pvalues, ["","",""], ["Double-hit vs single-hit - p-value","Triple-hit vs double-hit - p-value","Triple-hit vs single-hit - p-value"], "Models comparison - Fits, TestResults_pvalues", "TestResults_pvalues", "TestResults_pvalues")

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

#print("AICc averages:", np.average(np_AICc[0]))
#print(np.average(np_AICc[1]))
#print(np.average(np_AICc[2]))
"""

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
"""

      

# =============================================================================
# End of file
# =============================================================================