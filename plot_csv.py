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
# =============================================================================
# Declares
# =============================================================================
fname = "output_withcol.csv"
num_seqs = []
num_sites = []
Dh_vs_Sh = []
TripleH_rates = []
Genename_TripleH = []
significant_TripleH = [0, 0]
columns = ['File name', 'number of sequences', 'number of sites', 'Double-hit vs single-hit - LRT', 'Double-hit vs single-hit - p-value', 'Triple-hit vs double-hit - LRT', 'Triple-hit vs double-hit - p-value', 'Triple-hit vs single-hit - LRT', 'Triple-hit vs single-hit - p-value', 'MG94 with double and triple instantaneous substitutions - AIC-c', 'MG94 with double and triple instantaneous substitutions - Log Likelihood', 'Substitution rate from nucleotide A to nucleotide C', 'Substitution rate from nucleotide A to nucleotide G', 'Substitution rate from nucleotide A to nucleotide T', 'Substitution rate from nucleotide C to nucleotide G', 'Substitution rate from nucleotide C to nucleotide T', 'Substitution rate from nucleotide G to nucleotide T', 'non-synonymous/synonymous rate ratio', 'rate at which 2 nucleotides are changed instantly within a single codon', 'rate at which 3 nucleotides are changed instantly within a single codon', 'MG94 with double instantaneous substitutions - AIC-c', 'MG94 with double instantaneous substitutions - Log Likelihood', 'Substitution rate from nucleotide A to nucleotide C', 'Substitution rate from nucleotide A to nucleotide G', 'Substitution rate from nucleotide A to nucleotide T', 'Substitution rate from nucleotide C to nucleotide G', 'Substitution rate from nucleotide C to nucleotide T', 'Substitution rate from nucleotide G to nucleotide T', 'non-synonymous/synonymous rate ratio', 'rate at which 2 nucleotides are changed instantly within a single codon', 'Standard MG94 - AIC-c', 'Standard MG94 - Log Likelihood', 'Substitution rate from nucleotide A to nucleotide C', 'Substitution rate from nucleotide A to nucleotide G', 'Substitution rate from nucleotide A to nucleotide T', 'Substitution rate from nucleotide C to nucleotide G', 'Substitution rate from nucleotide C to nucleotide T', 'Substitution rate from nucleotide G to nucleotide T', 'non-synonymous/synonymous rate ratio']
n = 13292

AICc = [[], [], []]
LL = [[], [], []]

# =============================================================================
# Helper functions
# =============================================================================
def subplot_boxplot(asizes, adesc, species, title, xaxislabel, filename):
    #global asizes, afilename, adesc
    plotly.offline.init_notebook_mode(connected=False)
    #trace3 = go.Histogram(x=asizes[3], name=species[3])
    trace0 = go.Box(y=asizes[0], text=adesc[0], name=species[0])
    trace1 = go.Box(y=asizes[1], text=adesc[1], name=species[1])
    trace2 = go.Box(y=asizes[2], text=adesc[2], name=species[2])
    
    #fig = tools.make_subplots(rows=3, cols=1, subplot_titles=(species[0], species[1],species[2]))
    #fig = [trace0, trace1, trace2]
    fig = go.Figure(data=[trace0, trace1, trace2])
    #xaxis, yaxis
    #fig.append_trace(trace0, 1, 1)
    #fig.append_trace(trace1, 2, 1)
    #fig.append_trace(trace2, 3, 1)
    
    fig["layout"].update(title=title)
    #fig['layout']['xaxis1'].update(title=xaxislabel)
    #fig['layout']['yaxis1'].update(title='Occurences')
    #fig["layout"]["legend"].update(x=1.02)
    #fig["layout"].update(height=600)
    #fig["layout"].update(width=600)
    #fig["layout"]["legend"].update(xanchor="right")
    #fig["layout"]["legend"].update(yanchor="top")

    plotly.offline.plot(fig, filename=filename+"_SUBPLOT_Boxplot.html")

def subplot_histogram(asizes, adesc, species, title, xaxislabel, filename):
    #global asizes, afilename, adesc
    plotly.offline.init_notebook_mode(connected=False)
    #trace3 = go.Histogram(x=asizes[3], name=species[3])
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
    #fig["layout"]["legend"].update(x=1.02)
    #fig["layout"].update(height=600)
    #fig["layout"].update(width=600)
    #fig["layout"]["legend"].update(xanchor="right")
    #fig["layout"]["legend"].update(yanchor="top")
    plotly.offline.plot(fig, filename=filename+"_SUBPLOT_HISTOGRAM.html")


def plotly_things(numbers, filename, desc1, desc2, desc3): #single historgram
    plotly.offline.init_notebook_mode(connected=False)
    plotly.offline.plot({"data": [go.Histogram(x=numbers, text=desc3)],"layout": go.Layout(title=desc2, xaxis={'title':desc1}, yaxis={'title':'Occurences'})},filename=filename+"_HISTOGRAM.html")

def plotly_boxplot(numbers, filename, desc1, desc2, desc3): #Single boxplot
    plotly.offline.init_notebook_mode(connected=False)
    plotly.offline.plot({"data": [go.Box(x=numbers, text=desc3)],"layout": go.Layout(title=desc2, xaxis={'title':desc1}, yaxis={'title':'Occurences'})},filename=filename+"_Boxplot.html")

# =============================================================================
# Main subroutine
# =============================================================================
    
with open(fname) as f:
    count = 0
    line = f.readline()
    while True:
        line = f.readline().strip()
        if line == "": break
        data = line.split(",")
        
        num_seqs.append(int(data[1]))
        num_sites.append(int(data[2]))
        TripleH_rates.append(float(data[19]))
            
        if float(data[19]) > 1.0: #data[19] = "rate at which 3 nucleotides are changed instantly within a single codon"
            #print(float(data[19]), data[0])
            Genename_TripleH.append([float(data[19]), data[0]]) # <- ADD THIS FUNCTIONALITY TO THE CSV PARSER. WHICH GENES with rates above 1.0, names, space demilited and values space delmiited

        #Significant non-zero Triple Hits
        if float(data[19]) > 0.0:
           #data[6] =  "Triple-hit vs double-hit"
           #data[8] = Triple-hit vs single-hit"
           if float(data[6]) < 0.05: significant_TripleH[0] += 1 #counts
           if float(data[8]) < 0.05: significant_TripleH[1] += 1 #counts

        #AICc
        AICc[0].append(float(data[9])) #MG94 with double and triple instantaneous substitutions - AIC-c
        AICc[1].append(float(data[20])) #MG94 with double instantaneous substitutions - AIC-c
        AICc[2].append(float(data[30])) #Standard MG94 - AIC-c
        
        #log(L)
        LL[0].append(float(data[10])) #MG94 with double and triple instantaneous substitutions - Log Likelihood
        LL[1].append(float(data[21])) #MG94 with double instantaneous substitutions - Log Likelihood
        LL[2].append(float(data[31])) #Standard MG94 - Log Likelihood
        
        #Significant LRTs

        count += 1
        
# =============================================================================
# Make plots here.
# =============================================================================       
#plotly_things(TripleH_rates, "TH_RATES", "rate at which 3 nucleotides are changed instantly within a single codon", "Triple Mutation hit rate histogram", "Rate value")
#plotly_things(num_seqs, "NUMSEQS", "Sequence size distribution", "Number of seqeuences analyzed", "Number of sequences per file analyzed")
#plotly_things(num_sites, "NUMSITES", "Number of sites (Alignment length)", "Number of sites analyzed", "Number of sites aligned")

#subplot_histogram(AICc, ["","",""], ["MG94 with double and triple instantaneous substitutions","MG94 with double instantaneous substitutions","Standard MG94"], "Models comparison - AICc", "AICc", "AICc")
#subplot_histogram(LL, ["","",""], ["MG94 with double and triple instantaneous substitutions","MG94 with double instantaneous substitutions","Standard MG94"], "Models comparison - log(L)", "Log Likelihoods", "LogLikelihoods")
   

#plotly_boxplot(num_sites, "NUMSITES", "Number of sites (Alignment length)", "Number of sites analyzed", "Number of sites aligned")     
#subplot_boxplot(AICc, ["","",""], ["MG94 with double and triple instantaneous substitutions","MG94 with double instantaneous substitutions","Standard MG94"], "Models comparison - AICc", "AICc", "AICc")


# =============================================================================
# Summary Statistics
# =============================================================================
print("## SUMMARY STATISTICS ##", "\n")
print("Triple Hit Rates max:", max(TripleH_rates), "min:", min(TripleH_rates), "N =", len(TripleH_rates))
TripleH_rates = np.asarray(TripleH_rates)
print(stats.describe(TripleH_rates))
print()
#print(sorted(TripleH_rates))

print("Number of files containing genes with triple hit rate > 1.0:", len(Genename_TripleH)) #NOW HAVE TO GO INTO EACH FILE AND PICK THE GENE NAMES WITH rates above 1 <- do in CSV creator.

#For what proportion of these rates was there a significant p-value for non-zero triple hits?
#if "rate at which 3 nucleotides are changed instantly within a single codon" > 0.0 then
#if "Triple-hit vs double-hit" or Triple-hit vs single-hit", p value < 0.05, count it and indicate which

print(significant_TripleH, n, "\n", "Signicicant Proportion Triple-hit vs double-hit (%):", (significant_TripleH[0]/n)*100, "\n", "Significant Proprotion Triple-hit vs single-hit (%):", (significant_TripleH[1]/n)*100)
print()
print("Average number of sequences:", sum(num_seqs)/ len(num_seqs))
print(stats.describe(np.asarray(num_seqs)))
print("Average number of sites:", sum(num_sites)/ len(num_sites))
print(stats.describe(np.asarray(num_sites)))


#print("AICc averages:", np.average(np_AICc[0]))
#print(np.average(np_AICc[1]))
#print(np.average(np_AICc[2]))

print()
np_AICc = np.asarray(AICc)
print("AICc summary Stats")
print("#MG94 with double and triple instantaneous substitutions#\n", stats.describe(np_AICc[0]))
print("#MG94 with double instantaneous substitutions#\n", stats.describe(np_AICc[1]))
print("Standard MG94#\n", stats.describe(np_AICc[2]))
      
print()    
np_LL = np.asarray(LL)
print("log(L) summary Stats")
print("#MG94 with double and triple instantaneous substitutions#\n", stats.describe(np_LL[0]))
print("#MG94 with double instantaneous substitutions#\n", stats.describe(np_LL[1]))
print("#Standard MG94#\n", stats.describe(np_LL[2]))

# =============================================================================
# End of file
# =============================================================================
#To Do AICc histo between the 3 models. (Make 3 histos)
#To Do log(L) histo between the 3 models. (Make 3 histos)
#Significant (p < 0.05) LRT comparison between models. (3 histos).. meaning LRT Values which are significant
#number of sites histo


"""
#pvalues comparison between models (histos)
#Omega value boxplots betwee nmodels.
#LRT, p value comparison. Which model is better? Highest LRT with p < 0.05
#as above but for AICc
#Triple hit rate histo.
"""