# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 08:09:50 2019

@author: alexander lucaci
"""

#cycle through the selectome files

#p value thresholded

#is this a TH site? above 3x mean

#is there another TH site within 5, 10, 20 sites of this one?
## if so, count

#is there a DH site within 5, 10, 20 sites of this TH site?
## if so, count

#plot this

#filename (Y)
#number of TH sites within 10 sites of original.

#meaning, there are a number of TH sites with a lot of other TH or DH sites near it.
#very active sites
# =============================================================================
# Imports
# =============================================================================
import os
import json
import numpy as np
import plotly
import plotly.graph_objs as go

# =============================================================================
# Declares
# =============================================================================
SELECTOME = r"E:\SELECTOME_TRIP_AMMENDED_SRV\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"
#SELECTOME = r"E:\TRIPLE HITS\WO_SERINES_ALLFILES_FITTERS_JSON\WO_SERINES_ALLFILES_FITTERS_JSON"

files = [f for r, d, f in os.walk(SELECTOME)]
existing = [os.path.join(SELECTOME, file) for file in files[0]]
#name, ext = os.path.splitext(each_file)
THRESHOLD_TH_VALUE = 3

# =============================================================================
# Helper functions
# =============================================================================
def diff_count(from_codon, to_codon):
    count = 0
    if from_codon[0] != to_codon[0]: count += 1
    if from_codon[1] != to_codon[1]: count += 1
    if from_codon[2] != to_codon[2]: count += 1
    return count

def pvalue_thresholded(filename):
    pvalue_threshold = 0.005
    with open(filename, "r") as fh:
        json_data = json.load(fh)
        THvsDH_LRT_pvalue = json_data["test results"]["Triple-hit vs double-hit"]["p-value"]
        #EvidenceRatio_TH = json_data["Evidence Ratios"]["Three-hit"][0]
        #Site_subs = json_data["Site substitutions"]
        
    fh.close()
    if float(THvsDH_LRT_pvalue) >= pvalue_threshold: 
        return False
    else:
        return True

def EvidenceRatio(filename):
    #num_ER_thresholded_sites = 0
    with open(filename, "r") as fh:
        json_data = json.load(fh)
        EvidenceRatio_TH = json_data["Evidence Ratios"]["Three-hit"][0]
        Site_subs = json_data["Site substitutions"]
    fh.close()
    Threshold_TH = THRESHOLD_TH_VALUE * np.mean(EvidenceRatio_TH)
    #Filtered_Threshold_TH = list(filter(lambda x: x > Threshold_TH, EvidenceRatio_TH))
    #Need site info. and ER at site
    site_info = []
    for n, i in enumerate(EvidenceRatio_TH):
        if float(i) > Threshold_TH:
            #print(n, i)
            site_info.append(n)
    if len(site_info) > 0:
        return site_info, Site_subs
    else:
        return 0, 0
    """
        if len(Filtered_Threshold_TH) > 0 and Filtered_Threshold_TH != None:
            print("FILTERED TH:", Filtered_Threshold_TH)
            num_ER_thresholded_sites += len(Filtered_Threshold_TH) 
            #site subs
            print(Site_subs.keys())
            return num_ER_thresholded_sites, Filtered_Threshold_TH
    """ 
            
def sites_within_a_bin(site_info, site_subs, binsize):
    print(" calculating bin size:", binsize)
    print(" Sites:", site_info)
    #print(site_subs.keys())
    site_subs_lst = [key for key in site_subs.keys()]
    print(" All site subs:", site_subs_lst)
    #out of all of the site subs
    #take item n0 in list site_info
    #is there another site_sub within a binsize window?
    #if yes, 
        #is another TH occuring within the site?
        #count it
    return_dict = {}
    for site in site_info:
        #how many site in site_subs_lst are within the binsize window?
        #Given the site
        print("Comparing:", type(site), site)
        for site_sub in site_subs_lst:
            x = abs(int(site_sub) - int(site))
            if x <= binsize:
                print(int(site), "to", int(site_sub), "binsize:", type(binsize), int(site_sub) - int(site))
                #Is a triple change occuring?
                #print("CODONs FROM:", site_subs[site_sub].keys())
                for key in site_subs[site_sub].keys():
                    #print(site_subs[site_sub][key])
                    #print(key, "CODON TO:", site_subs[site_sub][key].keys())
                    for codon_to in site_subs[site_sub][key].keys():
                        if diff_count(key, codon_to) == 3:
                            print(key, "codon to", codon_to)
                            try:
                                return_dict[site] += 1
                            except:
                                return_dict[site] = 1
        print()
    #return a dict
    #key = site in site_info 
    #value = a count of number TH changes occuring within the binsize
    return return_dict

"""
another way to think about this may be to just take the site_subs list
look for all TH changes
and ask how many fall within a binsize window of each other
"""

def bar_chart(x, y, title, output, filenames):
    #https://plot.ly/python/bar-charts/
    #import plotly.express as px
    
    data = [go.Scatter3d(
            x=x,
            y=y,
            z=[f.split("| ")[1] for f in filenames],
            text=filenames,
            mode='markers'
    )]
    
    #data = [go.Bar(
    #        x=['giraffes', 'orangutans', 'monkeys'],
    #        y=[20, 14, 23]
    #)]
    layout = go.Layout(
    #title='testresults, , pvalue versus seq.length.',
    title=title,
    xaxis=dict(title='Number of TH sites within codon window',
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
    yaxis=dict(
        title='Occurences',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ))
        
    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(tickvals=[2, 5,10, 15, 20])
    plotly.offline.plot(fig, filename=output)


def bar_chart_original(x, y, title, output, filenames):
    #https://plot.ly/python/bar-charts/
    
    data = [go.Scatter(
            x=x,
            y=y,
            mode = 'markers',
            text=filenames,
            marker=dict(size=16, line=dict(color="black", width=1))
    )]
    
    #data = [go.Bar(
    #        x=['giraffes', 'orangutans', 'monkeys'],
    #        y=[20, 14, 23]
    #)]
    layout = go.Layout(
    #title='testresults, , pvalue versus seq.length.',
    title=title,
    xaxis=dict(title='Number of TH sites within codon window',
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
    yaxis=dict(
        title='Occurences',
        titlefont=dict(
            size=16,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ))
        
    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(tickvals=[2, 5,10, 15, 20])
    plotly.offline.plot(fig, filename=output)


# =============================================================================
# Main subroutine
# =============================================================================
#cycle through the selectome files
cnt_passed = 0
total_files = 0

site10_window_x = [] #binsize
site10_window_y = [] #values
site10_window_filenames = [] #filename

site5_window_x = [] #binsize
site5_window_y = [] #values
site5_window_filenames = [] #filename

site20_window_x = [] #binsize
site20_window_y = [] #values
site20_window_filenames = [] #filename

site15_window_x = [] #binsize
site15_window_y = [] #values
site15_window_filenames = [] #filename

site2_window_x = [] #binsize
site2_window_y = [] #values
site2_window_filenames = [] #filename

for n, item in enumerate(existing):
    total_files += 1
    if os.path.isfile(item): #exists
        name, ext = os.path.splitext(item)      
        if ext == ".json":
            x = pvalue_thresholded(item)
            if x == True: #passed p-value threshold
                cnt_passed += 1
                #process for TH Sites
                print("(" + str(n) + ") processing..")
                site_info, site_subs = EvidenceRatio(item)
                
                if type(site_info) == list:
                    print("", name.replace(SELECTOME, ""), "TH SITES:", site_info)
                    print("", site_subs.keys())
                    #is there another TH Site within 5, 10, 20 sites of any in the list?
                    site_window10 = sites_within_a_bin(site_info, site_subs, 10)
                    site_window5 = sites_within_a_bin(site_info, site_subs, 5)
                    site_window20 = sites_within_a_bin(site_info, site_subs, 20)
                    site_window15 = sites_within_a_bin(site_info, site_subs, 15)
                    site_window2 = sites_within_a_bin(site_info, site_subs, 2)
                    
                    print("Plot this:", os.path.basename(item), site_window10)
                    #bar_chart()
                    for key in site_window10.keys(): 
                        site10_window_y.append(site_window10[key])
                        site10_window_filenames.append("Site: " + str(key) + " | " + os.path.basename(item))
                        
                    for key in site_window5.keys(): 
                        site5_window_y.append(site_window5[key])
                        site5_window_filenames.append("Site: " + str(key) + " | " + os.path.basename(item))
                        
                    for key in site_window20.keys(): 
                        site20_window_y.append(site_window20[key])
                        site20_window_filenames.append("Site: " + str(key) + " | " + os.path.basename(item))
                        
                    for key in site_window15.keys(): 
                        site15_window_y.append(site_window15[key])
                        site15_window_filenames.append("Site: " + str(key) + " | " + os.path.basename(item))
                        
                    for key in site_window2.keys(): 
                        site2_window_y.append(site_window2[key])
                        site2_window_filenames.append("Site: " + str(key) + " | " + os.path.basename(item))
                    
                else:
                    print(" Nothing to do, continue")
                
    #if cnt_passed == 20: break


# =============================================================================
# Plotting
# =============================================================================
print("Plotting")    

#x = [10, 10, 10, 5, 5, 5, 20, 20, 20]
#y = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#filenames = ["a.html"] * len(x)
#bar_chart(x, y, "TEST TITLE", "test_scatter_thsiteanalysis_binned.html", filenames)
"""
x = [10] * len(site10_window_y)
y = site10_window_y
filenames = site10_window_filenames
bar_chart(x, y, "TEST TITLE", "test_scatter_thsiteanalysis_binned.html", filenames)
x = [5] * len(site5_window_y)
y = site5_window_y
filenames = site5_window_filenames
bar_chart(x, y, "TEST TITLE", "test_scatter_thsiteanalysis_binned.html", filenames)

x = [20] * len(site20_window_y)
y = site20_window_y
filenames = site20_window_filenames
bar_chart(x, y, "TEST TITLE", "test_scatter_thsiteanalysis_binned.html", filenames)
"""

x = [10] * len(site10_window_y) + [5] * len(site5_window_y) + [20] * len(site20_window_y) + [15] * len(site20_window_y) + [2] * len(site20_window_y)
y = site10_window_y + site5_window_y + site20_window_y + site15_window_y + site2_window_y
filenames = site10_window_filenames + site5_window_filenames + site20_window_filenames + site15_window_filenames + site2_window_filenames


bar_chart(x, y, "TEST TITLE", "test_scatter_thsiteanalysis_binned.html", filenames)

"""
Each dot represents, a specific site within an alignment
which is surrounded by X number of triple hit changes within a Y (number of sites) window

Sites may have more changes than the Y sized window because each individual site can have more than 1 TH change.
"""
# =============================================================================
# Summary
# =============================================================================

print()
print("### Summary ###")
print("total number of files processed:", total_files)
print("number of files which passed p-value threshold:", cnt_passed)
print( "Number of sites, binsize 10:", len(site10_window_y))
print(site10_window_y)
print( "Number of sites, binsize 5:",len(site5_window_y))
print( "Number of sites, binsize 20:",len(site20_window_y))
print( "Number of sites, binsize 15:",len(site15_window_y))
print( "Number of sites, binsize 2:",len(site2_window_y))

        
# =============================================================================
# End of file
# =============================================================================
#print(len(files[0]))
#print(len(existing))
#print(existing)

"""
files = []
cnt = 0



for r, d, f in os.walk(SELECTOME):
    print(os.path.join(SELECTOME, str(f)))
    
    
    
    #print(n, f)
    
    #for file in f:
    #    print(os.path.join(r, f))
    
    #files.append(f)
    print(len(f))
    files = f
    cnt += 1

print(cnt)
    
print(len(files))
#print(files)

#for file in files:
#    print(os.path.join(SELECTOME, file))
"""