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
fitters = "/Users/alex/Documents/TRIPLE_HITS/SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON" #originals

#without Serines, based on the FitMultiMode_cpl.bf and MG_REV_TRIP_serineless.bf
#wo_serine_fitters = r"E:\SELECTOME_TRIP_AMMENDED_SRV\W-O_SERINES_pvalueand10x"
wo_serine_fitters = "/Users/alex/Documents/TRIPLE_HITS/WO_SERINE_pvalue0-005_Thres_10x"

#Look for this ending.
file_ending = ".FITTER.json"

filenames_by_class = ["allfiles.txt", "p0-005.txt", "p0-005_Threshold_3x_.txt", "p0-005_Threshold_10x_.txt"]
# =============================================================================
# Helper functions
# =============================================================================
def diff(b, a): #b is the original, a is the without serine
    return float(b)-float(a)

def plot(x, y, title, output):
    plotly.offline.init_notebook_mode(connected=False)
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
# =============================================================================
# Main
# =============================================================================
by_file_class = True
print("() Init")
""" The setup. """
if by_file_class == False: 
    #plot(['2016','2017','2018'], [-500,-600,-700])
    #sys.exit(1)
    path = wo_serine_fitters
    #files = [path+"\\"+f.name for f in os.scandir(path) if f.name.endswith(file_ending)]
    files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(file_ending)]
    #print(", ".join(["#", "Filename", "Original TH rate", "W/O Serine TH Rate", "Difference (Original-W/O)"]))
    output_filename = "default.html"
    
#by file class?
print("() Processing by file class")
if by_file_class == True:
    
    path = "/Users/alex/Documents/TRIPLE_HITS/WO_SERINES_ALLFILES_FITTERS_JSON"
    
    for filename in filenames_by_class:
        files = []
        cnt = 0
        #filename = filenames_by_class[0]
        output_filename = filename.replace(".txt", ".html")
        with open(filename) as f:
            for n, line in enumerate(f):
                exists = path+"/"+line.strip()+file_ending
                if os.path.isfile(exists):
                    #files.append(path+"/"+line.strip()+".FITTER.json")
                    files.append(exists)
                    cnt += 1
            f.close()
        #print(len(files), cnt)
    
        main(files)       
    

sys.exit(3) # --- ##

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
"""
Make table

Model
LogL
omega
2-hit rate and pvalue
3hitrate and pvalue
"""


"""
def read_json_andcsv(filename):
    this_file = {}
    #header = 
    csv_columns = ['No','Name','Country']
    with open(filename, "r") as fh:
        json_data = json.load(fh)
        csv_file = json_data["input"]["file name"].split("/")[-1] + ".csv"
        with open(csv_file, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            count = 0
            csv_columns = ["fits"]
            for n, data in enumerate(json_data.keys()):
                if data in csv_columns:
                    if count == 0:
                        #csvwriter.writerow(json_data.keys())
                        csvwriter.writerow(data)
                        count += 1
                    csvwriter.writerow(json_data[data])
    fh.close()

"""