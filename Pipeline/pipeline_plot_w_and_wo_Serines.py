# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 10:06:01 2019

@author: alexander lucaci


https://plot.ly/python/bar-charts/

https://community.plot.ly/t/different-colors-for-bars-in-barchart-by-their-value/6527/7
"""

# =============================================================================
# Imports
# =============================================================================
import json, csv, os
import plotly, sys
import plotly.graph_objs as go
from plotly import tools

# =============================================================================
# Declares
# =============================================================================
#With Serine Fitters (aka the originals)
#fitters = r"E:\SELECTOME_TRIP_AMMENDED_SRV\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"
#fitters = "/Users/alex/Documents/TRIPLE_HITS/SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON" #originals
fitters = sys.argv[1]


#without Serines, based on the FitMultiMode_cpl.bf and MG_REV_TRIP_serineless.bf
#wo_serine_fitters = r"E:\SELECTOME_TRIP_AMMENDED_SRV\W-O_SERINES_pvalueand10x"
#wo_serine_fitters = "/Users/alex/Documents/TRIPLE_HITS/WO_SERINE_pvalue0-005_Thres_10x"
wo_serine_fitters = sys.argv[2]

#Look for this ending.
file_ending = ".FITTER.json"

output_directory = sys.argv[3]

#This needs to be generated.
#filenames_by_class = ["allfiles.txt", "p0-05.txt", "p0-005.txt", "p0-005_Threshold_3x_.txt", "p0-005_Threshold_10x_.txt"]
pvalue_threshold = 0.05
# ============================================================================
# Helper functions
# =============================================================================
def diff(b, a): #b is the original, a is the without serine
    return float(b)-float(a)

def plot(x, y, title, output):
    #plotly.offline.init_notebook_mode(connected=False)
    data = [
    go.Bar(
        x = x,
        y = y,
        #base = [-500,-600,-700],
        marker = dict(color = ['red' if val < 0 else 'blue' for val in y])#name = 'expenses'
        )]
    fig = go.Figure(data=data)
    #fig["layout"].update(title="TH Rate differences (with and without Serines) Total cases: Num neg. cases: ")
    fig["layout"].update(title=output.replace(".html", "") + " - " + title)
    #fig['layout']['xaxis1'].update(title=xaxislabel)
    fig['layout']['yaxis1'].update(title='TH rate difference (original - without serine)')
    plotly.offline.plot(fig, filename=output)
    #plotly.offline.plot(fig, filename='pV0-005_Thres10x_diff_THrate.html')

def read_json_returnTHrate(filename):
    with open(filename, "r") as fh:
        json_data = json.load(fh, strict=False)
        fh.close()
    return json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["parameters"]["rate at which 3 nucleotides are changed instantly within a single codon"]



# =============================================================================
# Main subroutine
# =============================================================================
def main(files):
    """ Data processing """
    plot_data_holder = {}                 
    filecount = 0
    numnegatives = 0
    num_zerochange = 0
    
    for i, file in enumerate(files): #WO SERINES
        #print("Loading:", i, file)
        #print("Reading:", file)
        file_a = read_json_returnTHrate(file) # without serines
        #print(os.path.join(fitters, file.split("\\")[-1]))
        
        try:
            file_b = read_json_returnTHrate(os.path.join(fitters, file.split("/")[-1])) #original
        except:
            continue
        
        #print(i+1, file.split("/")[-1], file_b, file_a, diff(file_b,file_a))
        
        #print("Trying diff")
        try:
            #print("in diff")
            plot_data_holder[file.split("/")[-1]] = diff(file_b, file_a)  #ORIGINAL - WO_SERINE
            #IF NEGATIVE, WO_SERINE RATE IS HIGHER THAN ORIGINAL
            #IF POSITIVE, ORIGINAL IS HIGHER THAN WO_SERINE
            if diff(file_b,file_a) < 0: numnegatives += 1
            #print(diff(file_b,file_a))
            if diff(file_b,file_a) == 0.0: num_zerochange += 1
            filecount += 1
        except:
            continue
        
        #if i == 100: break


    """ Plotting """
    print("\t() Plotting pairs:", len(plot_data_holder), "files")
    print("\t", "Number of Negative values (WO_SERINE RATE IS HIGHER THAN ORIGINAL):", numnegatives, (numnegatives/len(plot_data_holder))*100)
    print("\t", "Number of No change values:", num_zerochange, (num_zerochange/len(plot_data_holder))*100)
    
    x, y = [], []
    for key in plot_data_holder.keys():
         x.append(key)
         y.append(plot_data_holder[key])
    #print("\t", numnegatives, str((numnegatives/filecount)*100) + "%")
    asapercent = round((numnegatives/filecount)*100, 2)
    #print("\t", asapercent)
    title = "TH Rate differences (with and without Serines) Total cases: " + str(filecount) +  " Num neg. cases: " + str(numnegatives) + " (" + str(asapercent) + "%)"
    plot(x, y, title, output_filename)
  
    
def pass_pvalue_threshold(filename):
    global pvalue_threshold
    
    
    with open(filename, "r") as fh:
        json_data = json.load(fh)
    fh.close()
    
    file_pvalue = json_data["test results"]["Triple-hit vs double-hit"]["p-value"]
    
    if float(file_pvalue) < pvalue_threshold:
        passed = True
    else:
        passed = False
        
    return passed
# =============================================================================
# Main
# =============================================================================
#by_file_class = False
by_file_class = sys.argv[4]

print("\t() Init")

""" The setup. """

if by_file_class == "False": 
    print([by_file_class])
    #plot(['2016','2017','2018'], [-500,-600,-700])
    #sys.exit(1)
    path = wo_serine_fitters
    #files = [path+"\\"+f.name for f in os.scandir(path) if f.name.endswith(file_ending)]
    files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(file_ending)]
    #print(", ".join(["#", "Filename", "Original TH rate", "W/O Serine TH Rate", "Difference (Original-W/O)"]))
    output_filename = output_directory + "W_AND_WO_SERINES.html"
    print("\t() Saving to:", output_filename)
    main(files)  
    

if by_file_class == "True":
    print([by_file_class])
    #by file class?
    print("() Processing by file class, which means p-value threshold")
    #path = sys.argv[1]
    path = wo_serine_fitters
    files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(file_ending)]
    filenames_by_class = [file for file in files if pass_pvalue_threshold(file) == True]
    output_filename = output_directory + "W_AND_WO_SERINES_pvalue_threshold.html"
    print("\t() Saving pvalue_thresholded to:", output_filename)
    main(filenames_by_class)       
    

sys.exit(3) # --- ##

# =============================================================================
# Extra code 
# =============================================================================



""" Data processing """
plot_data_holder = {}                 
filecount = 0
numnegatives = 0

for i, file in enumerate(files):
    #print("Loading:", i, file)
    file_a = read_json_returnTHrate(file) # without serines
    #print(os.path.join(fitters, file.split("\\")[-1]))
    file_b = read_json_returnTHrate(os.path.join(fitters, file.split("/")[-1])) #original
    print(i+1, file.split("/")[-1], file_b, file_a, diff(file_b,file_a))
    plot_data_holder[file.split("/")[-1]] = diff(file_b,file_a) 
    #if i == 100: break
    if diff(file_b,file_a) < 0: numnegatives += 1
    filecount += 1

""" Plotting """
 
x, y = [], []
for key in plot_data_holder.keys():
     x.append(key)
     y.append(plot_data_holder[key])
print(numnegatives, str((numnegatives/filecount)*100) + "%")
asapercent = round((numnegatives/filecount)*100, 2)
print(asapercent)
title = "TH Rate differences (with and without Serines) Total cases: " + str(filecount) +  " Num neg. cases: " + str(numnegatives) + " (" + str(asapercent) + "%)"
plot(x, y, title, output_filename)



"""
#--- sorted version
import collections
sorted_plot_data_holder = collections.OrderedDict(plot_data_holder)
x, y = [], []
for key in sorted_plot_data_holder.keys():
     x.append(key)
     y.append(sorted_plot_data_holder[key])
print(numnegatives, str((numnegatives/filecount)*100) + "%")
asapercent = round((numnegatives/filecount)*100, 2)
print(asapercent)
title = "TH Rate differences (with and without Serines) Total cases: " + str(filecount) +  " Num neg. cases: " + str(numnegatives) + " (" + str(asapercent) + "%)"
plot(x, y, title)
"""

# =============================================================================
# End of file
# =============================================================================
