#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 18:29:13 2019

@author: alex
"""

# =============================================================================
# Imports
# =============================================================================
import plotly, sys
import plotly.graph_objs as go
from plotly import tools
import sys

# =============================================================================
# Declares
# =============================================================================
#molecular function

#biological process

#protein class
#Total # Genes: 86831
#Total # protein class hits: 55658

filename_proteinclass = "pantherChart-ProteinClass.txt"
filename_biologicalprocess = "pantherChart-BiologicalProcess.txt"
filename_molecularfunctions = "pantherChart-MolecularFunction.txt"

"""
https://www.nature.com/articles/s41598-018-33323-z#Sec9

Try to do similar to this articles Figure 3, but vertical
"""

# =============================================================================
# Helper function
# =============================================================================
def plot(x_in, y_in, title, output):
    #plotly.offline.init_notebook_mode(connected=False)
    print("in plot")
    #data = [go.Bar(x = y_in, y = x_in)]
    
    data = [
    go.Bar(
        x = y_in,
        y = x_in,
        #base = [-500,-600,-700],
        #marker = dict(color = ['red' if val < 0 else 'blue' for val in y])#name = 'expenses'
        
        marker = dict(color='rgb(158,202,225)', line_color='rgb(8,48,107)'),
        orientation='h'
        #marker = dict(color='rgb(255, 178, 102)', line_color='rgb(153, 76, 0)')
        )]
    
    print("in plot 2")
    fig = go.Figure(data= [go.Bar(x = y_in, y = x_in)])
    #fig["layout"].update(title="TH Rate differences (with and without Serines) Total cases: Num neg. cases: ")
    fig["layout"].update(title=title)
    
    #fig.update_xaxes(title_font=dict(size=32, family='Courier', color='black'))
    #fig.update_yaxes(title_font=dict(size=32, family='Courier', color='black'))
    fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='black', size=22))
    fig.update_yaxes(tickfont=dict(family='Rockwell', color='black', size=22))
    #fig.update_xaxes(tickangle=45, tickfont=dict(family='Rockwell', color='crimson', size=14))
    
    #fig['layout']['xaxis1'].update(title=xaxislabel)
    fig['layout']['yaxis1'].update(title='')
    
    fig['layout']['yaxis'].update(dict(autorange="reversed"))
    plotly.offline.plot(fig, filename=output)
    #plotly.offline.plot(fig, filename='pV0-005_Thres10x_diff_THrate.html')
    
    

#ORANGE
#RGB 255, 178, 102
#line = RGB 255, 128, 0
# =============================================================================
# Main subroutine
# =============================================================================
def main(filename, title, output):
    
    with open(filename, "r", encoding='UTF-8') as f:
        data = f.read()
    #print(len(data))
    
    #print(type(data))
    #print([data])
    
    count = []
    dict_class_and_count = {}

    for n, line in enumerate(data.split("\n")):
        print("Current line:", n, line)
        
        try:
            counter = line.split("\t")[2]
            dclass = line.split("\t")[1]
        except:
            pass
        
        #print(counter, protein_class)
        dict_class_and_count[dclass] = int(counter)
        #print(counter)
        count.append(int(counter))
        
        
    #for n, line in enumerate(f):
    #    data = line.read()
    #    print(data)
    
    #sys.exit(1)
    #x = sum(count)
    
    #print(x)
    
    #print(1043/x)
    
    print("Plotting")
    
    #x = filenames
    #y = values
    x = []  
    y = []
    
    #for k in dict_proteinclass_and_count:
    #        x.append(k)
    #        y.append(dict_proteinclass_and_count[k])
            
    #print(x)       
    
    print("\n SORTED")
    
    item_sum = 0
    for key, value in sorted(dict_class_and_count.items(), key=lambda item: item[1], reverse=True):
        item_sum += int(value)
    
    print("TOTAL:", item_sum )
    
    for key, value in sorted(dict_class_and_count.items(), key=lambda item: item[1], reverse=True):
        print("%s: %s" % (key, value))
        x.append(key)
        
        y_value = round((int(value)/item_sum), 4)
        print(y_value )
        y.append(y_value)
    
    
    
    
    #plot(x, y, "    Gene Ontology - Protein Class", "GO_ProteinClass.html")
    #if filename
    print()
    print(x)
    print(y)
    print(title)
    print(output)
    plot(x, y, title, output)
    
    
# =============================================================================
# 
# =============================================================================
print("plotting")

main(filename_proteinclass,"Gene Ontology - Protein Class as a fraction (n=55658)", "GO_ProteinClass_asafraction_22pt.html")

sys.exit(1)
    
main(filename_proteinclass, "    Gene Ontology - Protein Class", "GO_ProteinClass.html")

main(filename_proteinclass,"    Gene Ontology - Protein Class as a fraction", "GO_ProteinClass_asafraction.html")

main(filename_biologicalprocess,"    Gene Ontology - Biological Process", "GO_biologicalprocess.html")

main(filename_molecularfunctions,"    Gene Ontology - Molecular Functions", "GO_molecularfunctions.html")
# =============================================================================
# end of file
# =============================================================================
