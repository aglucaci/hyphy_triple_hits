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

# =============================================================================
# Declares
# =============================================================================
fname = "output_withcol.csv"
num_seqs = []
num_sites = []
Dh_vs_Sh = []
TripleH_rates = []
Genename_TripleH = []

#pvalues comparison between models (histos)
#Omega value boxplots betwee nmodels.
#LRT, p value comparison. Which model is better? Highest LRT with p < 0.05
#as above but for AICc
#Triple hit rate histo.

significant_TripleH = []

columns = ['File name', 'number of sequences', 'number of sites', 'Double-hit vs single-hit - LRT', 'Double-hit vs single-hit - p-value', 'Triple-hit vs double-hit - LRT', 'Triple-hit vs double-hit - p-value', 'Triple-hit vs single-hit - LRT', 'Triple-hit vs single-hit - p-value', 'MG94 with double and triple instantaneous substitutions - AIC-c', 'MG94 with double and triple instantaneous substitutions - Log Likelihood', 'Substitution rate from nucleotide A to nucleotide C', 'Substitution rate from nucleotide A to nucleotide G', 'Substitution rate from nucleotide A to nucleotide T', 'Substitution rate from nucleotide C to nucleotide G', 'Substitution rate from nucleotide C to nucleotide T', 'Substitution rate from nucleotide G to nucleotide T', 'non-synonymous/synonymous rate ratio', 'rate at which 2 nucleotides are changed instantly within a single codon', 'rate at which 3 nucleotides are changed instantly within a single codon', 'MG94 with double instantaneous substitutions - AIC-c', 'MG94 with double instantaneous substitutions - Log Likelihood', 'Substitution rate from nucleotide A to nucleotide C', 'Substitution rate from nucleotide A to nucleotide G', 'Substitution rate from nucleotide A to nucleotide T', 'Substitution rate from nucleotide C to nucleotide G', 'Substitution rate from nucleotide C to nucleotide T', 'Substitution rate from nucleotide G to nucleotide T', 'non-synonymous/synonymous rate ratio', 'rate at which 2 nucleotides are changed instantly within a single codon', 'Standard MG94 - AIC-c', 'Standard MG94 - Log Likelihood', 'Substitution rate from nucleotide A to nucleotide C', 'Substitution rate from nucleotide A to nucleotide G', 'Substitution rate from nucleotide A to nucleotide T', 'Substitution rate from nucleotide C to nucleotide G', 'Substitution rate from nucleotide C to nucleotide T', 'Substitution rate from nucleotide G to nucleotide T', 'non-synonymous/synonymous rate ratio']

# =============================================================================
# Helper functions
# =============================================================================
def plotly_things(numbers, filename, desc1, desc2, desc3):
    plotly.offline.init_notebook_mode(connected=False)
    plotly.offline.plot({"data": [go.Histogram(x=numbers, text=desc3)],"layout": go.Layout(title=desc2, xaxis={'title':desc1}, yaxis={'title':'Occurences'})},filename=filename+"_HISTOGRAM.html")


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
        
        num_seqs.append(data[1])

        #if "rate" not in data[19]:
            
        TripleH_rates.append(float(data[19]))
            
        if float(data[19]) > 1.0: #data[19] = "rate at which 3 nucleotides are changed instantly within a single codon"
            #print(float(data[19]), data[0])
            Genename_TripleH.append([float(data[19]), data[0]])

        if float(data[19]) > 0.0:
            pass
            
            print(float(data[6]), float(data[8]))
            
            
        
        count += 1
        

#print(num_seqs, len(num_seqs))
#plotly_things(num_seqs, "testhisto", "testdesc")
#print(columns[19])
        
plotly_things(TripleH_rates, "TH_RATES", "rate at which 3 nucleotides are changed instantly within a single codon", "Triple Mutation hit rate histogram", "Rate value")
#plotly_things(num_seqs, "NUMSEQS", "Sequence size distribution", "Number of seqeuences analyzed", "Number of sequences per file analyzed")


print(max(TripleH_rates), min(TripleH_rates), len(TripleH_rates))
#print(sorted(TripleH_rates))
print(len(Genename_TripleH)) #NOW HAVE TO GO INTO EACH FILE AND PICK THE GENE NAMES WITH rates above 1


#For what proportion of these rates was there a significant p-value for non-zero triple hits?
#if "rate at which 3 nucleotides are changed instantly within a single codon" > 0.0 then
#if "Triple-hit vs double-hit" or Triple-hit vs single-hit", p value < 0.05, count it and indicate which







# =============================================================================
# End of file
# =============================================================================
#To Do AICc histo between the 3 models. (Make 3 histos
#Significant (p < 0.05) LRT comparison between models. (3 histos)
#number of sites histo