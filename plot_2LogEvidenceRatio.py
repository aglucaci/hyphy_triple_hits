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
"""

# =============================================================================
# Imports
# =============================================================================
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import numpy as np
import json, csv, os
from shutil import copyfile

#copyfile(src, dst)
# =============================================================================
# Declares
# =============================================================================
init_notebook_mode(connected=True)

#BUSTED Folder
directory = r"E:\BUSTED_SIM_SRV_FITTER_JSON\BUSTED_SIM_SRV_FITTER_JSON"
#directory = r"E:\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"
#directory = r"E:\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON_ADDITIONAL\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON_ADDITIONAL" #check this against output dir

##output_dir = r"E:\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON_HTML" #main one
output_dir = r"E:\BUSTED_SIM_SRV_FITTER_JSON\BUSTED_SIM_SRV_FITTER_JSON_HTML"

#output_dir_suppl = r"E:\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON_HTML\Supplement"
#output_dir_suppl_FITTERs = r"E:\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON_HTML\Supplement\FITTER_JSON"
#filename = ["allOis1_D_100_replicate.1.FITTER.json"]

#Parse the json
#Three_hit = [1.001390014360347, 0.9979394029716767, 0.9991241285782849, 1.00127426088317, 0.9985354235854298, 0.9984709455099117, 1.002073311216048, 1.001780281971484, 0.9996103496053033, 1.000756993536668, 1.001991321041256, 1.001680820654508, 1.00463814088762, 1.000043670384645, 0.9981814422553464, 1.000678275074349, 0.9983030440783975, 0.9996434577286832, 0.9998273490880808, 1.000902611347252, 1.001958611016499, 1.000046518632957, 0.9994021901316387, 0.9997382936142335, 1.001932067658296, 0.9987912194703059, 0.9970088386992207, 1.002281105509041, 0.9996634241867047, 0.9997124432731236, 1.000049727304403, 0.9994444639708604, 0.9986522408602755, 1.001944188684811, 1.000299876184699, 0.9976521575025862, 1.001401018378705, 1.001480452953043, 0.9976724401957808, 0.9991589066816811, 0.9980252536464759, 0.9990782285301462, 1.00214852768521, 0.9997288393086416, 0.9985201710290084, 0.9989490074603672, 0.9997767649428708, 0.9982451577557709, 1.002567689222285, 0.9986099280119436, 1.000206099410766, 1.000126910387006, 0.9993446275647343, 0.9996217929220677, 0.9976373949883331, 0.9981304397515073, 1.000014505775352, 0.9998711377442343, 1.001557516147573, 1.000089944257751, 0.9984067241725637, 0.9967236504002286, 0.9997132423844047, 1.000451679998051, 0.9988674849245973, 1.001340793810113, 0.9998968296868783, 1.00362294982541, 0.9986113684723351, 0.9977371138640617, 1.003307041682187, 1.000291931367852, 0.9996722442165997, 1.00057035685794, 1.001882078864379, 1.000082967573986, 0.998013258374147, 0.9985417296750307, 1.000512134400817, 0.9988388596103609, 0.9991457648894445, 1.002090322042013, 0.9986149003824069, 1.002970044779094, 0.9977407796450749, 0.9977958728480721, 1.001302552432428, 1.001144734810204, 1.002224581906339, 0.999915145175538, 0.9998619476056276, 0.9989105462984541, 0.9991141643247188, 1.00274718246144, 1.000506606291668, 1.001665385765126, 0.997853069830942, 1.001697027866775, 1.000640339735564, 0.9998218926358561] 
#Two_hit = [1.039479893074982, 0.9584559219606087, 0.9901336700991945, 1.152559507094038, 0.9586173761887439, 1.016569360345624, 1.208177463815821, 0.9470135564853616, 1.025054516566709, 0.9464091830177789, 0.9300909287718737, 1.152917404407017, 0.9834476270960291, 0.8711940985852985, 1.061717481734901, 1.041085748092181, 0.9179235293566413, 0.9470630951136433, 1.039981478503493, 1.019721180587162, 0.9886727326545284, 0.8451116097129812, 1.083881391375342, 1.087613495081031, 0.9459363428649024, 1.049605447841679, 1.120979810616649, 0.7929542359680789, 1.012819825425229, 0.9235488100648367, 0.923709021864677, 0.9692405791705493, 0.8944321248637757, 0.8719705673641486, 1.16202007998144, 0.9246369133142935, 1.05826347189908, 1.051470821893931, 1.013197320818225, 0.969902622574994, 0.8629295841538404, 1.068643335191989, 1.096398738862263, 0.9975678356560851, 1.103052632465649, 0.9259020358296548, 0.9349972573791201, 1.016736936774541, 1.014814598230592, 0.9021998002614513, 1.093779131396377, 1.014388408602677, 1.028342867217236, 1.036390530672396, 0.9825809788658478, 1.049960479628028, 1.105449398434692, 0.8818555529732883, 1.063534189348788, 0.9353434686535685, 0.8661731212374516, 0.9598372156966245, 0.9744800261515797, 1.017680932624984, 1.039124020074141, 0.9679371471477695, 0.986969754257685, 1.113959039760175, 1.010800648718586, 1.197823810172021, 1.14283556798233, 1.047536203363688, 1.167197913599269, 0.9542432632192275, 0.9695313863981695, 1.003308370250275, 1.134924738421028, 0.8559839407497793, 1.035339860472845, 0.9257905708477286, 0.9542217626376227, 0.9337222528956067, 1.033223858505008, 0.9239636717933107, 0.9561732832024701, 1.040970844714394, 0.8288869004373101, 1.08703760095394, 1.13206902340612, 1.023346063792786, 1.059489076056475, 1.025429412044061, 1.001245664670473, 0.9930811388098317, 1.009575481401908, 1.072553923312042, 1.155138332686375, 0.9837695079656531, 1.138731012690168, 1.025937391333278] 

#Sites = [range(len(Three_hit))]
#Sites = np.arange(1, len(Three_hit)+1)
#print(Sites)
#print(np.log(2))

# =============================================================================
# Helper functions
# =============================================================================

def load_json(filename):
    print("() Loading:", filename)
    with open(filename, "r") as fh:
        json_data = json.load(fh)
        #print(json_data["Evidence Ratios"]["Three-hit"])
        #print(json_data["Evidence Ratios"]["Two-hit"])
        #print(json_data["input"]["number of sites"])
        TH = json_data["Evidence Ratios"]["Three-hit"][0]
        DH = json_data["Evidence Ratios"]["Two-hit"][0]
        SITES = json_data["input"]["number of sites"] #can also calculated from the len of DH or TH
    fh.close()
    return TH, DH, np.arange(1, int(SITES) + 1) #1-Index
    #return TH, DH, np.arange(0, int(SITES))

def plotly_basicline(data_x, data_y_TH, data_y_DH, output_title, output):
    global output_dir
    #print("()DEBUG:", output_dir)
    # Create trace(s)
    trace0 = go.Scatter(x = data_x, y = data_y_TH, mode = 'lines+markers', name="Three Hit", opacity=0.75)
    trace1 = go.Scatter(x = data_x, y = data_y_DH, mode = 'lines+markers', name="Double Hit", opacity=0.75)
    data = [trace0, trace1]
    
    layout = dict(title = '2*LN(Evidence Ratio), Number of Sites = ' + str(len(data_x)) + ", " + output_title, 
                  xaxis = dict(title = 'SITE'), 
                  yaxis = dict(title = '2*LN(Evidence Ratio)'),)
    
    fig = dict(data=data, layout=layout)
    
    #plot(data, filename='basic-line_2LogN_EvidenceRATIO.html')
    #plot(fig, filename='basic-line_2LogN_EvidenceRATIO.html')
    
    #plot(fig, filename=output+".html")
    #output_dir = r"E:\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON\SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON_HTML"
    #output_file = os.path.join(output_dir_suppl, output_title + ".html")
    #print(output, output_title, output_file)
    
    #plot(fig, filename=output_file, auto_open=False) #auto_open=False for sanity.
    output_file = os.path.join(output_dir, output_title + ".html")
    print("() SAVING:", output_file)
    plot(fig, filename=output_file, auto_open=False) #auto_open=False for sanity.
    
# =============================================================================
# Main subrout.
# =============================================================================
def main_sub(filename, output_title):
    #print("()MAINSUB:", filename)
    #Load data from .FITTER.json
    EvidenceRatio_TH, EvidenceRatio_DH, Sites = load_json(filename)
    #print(EvidenceRatio_TH)
    
    #Transform evidence ratios by applying 2*LN(evidence_ratio)
    tx2_Ln_EvidenceRatio_TH = 2*np.log(EvidenceRatio_TH) 
    tx2_Ln_EvidenceRatio_DH = 2*np.log(EvidenceRatio_DH)
    
    #print("()MAINSUB[2]:", filename)
    #Plot (simple line) the two traces on the same plot.
    plotly_basicline(Sites, tx2_Ln_EvidenceRatio_TH, tx2_Ln_EvidenceRatio_DH, output_title, filename)
    
    
# =============================================================================
# Starting program..
# =============================================================================
#main_sub(filename[0])
count = 0
for root, dirs, files in os.walk(directory):
    for each_file in files:
        name, ext = os.path.splitext(each_file)
        if ext == ".json":
            #existing = os.path.join(directory, name + ext)
            existing = os.path.join(output_dir, name + ext)
            if not os.path.isfile(existing + ".html"):
                existing = os.path.join(directory, name + ext)
                #copy_FITTER = os.path.join(output_dir_suppl_FITTERs, name + ext)
                count +=1
                print(count, "Generating plot:", existing) #, each_file, [ext])
                #if not os.path.isfile(copy_FITTER): copyfile(existing, copy_FITTER)
                main_sub(existing, each_file)
            
# =============================================================================
# End of file
# =============================================================================
            
            
            
"""
def plotly_basicline_COLORTEST(data_x, data_y_TH, data_y_DH, output):
    trace0 = go.Scatter(x = data_x, y = data_y_TH, mode = 'lines+markers', name="Three Hit")
    trace1 = go.Scatter(x = data_x, y = data_y_DH, mode = 'lines+markers', name="Double Hit")
    data = [trace0, trace1]
    layout = dict(title = '2*LN(Evidence Ratio), Number of Sites = ' + str(len(data_x)) + ", " + output, 
                  xaxis = dict(title = 'SITE', gridcolor='rgb(255,255,255)'), 
                  yaxis = dict(title = '2*LN(Evidence Ratio)', gridcolor='rgb(255,255,255)'),
                  paper_bgcolor='rgba(0,0,0,0.15)',
                  plot_bgcolor="RGBA(0,0,0,0.15)",)
    fig = dict(data=data, layout=layout)
    plot(fig, filename=output+".html")
"""

"""
#N = 500
#random_x = np.linspace(0, 1, N)
#random_y = np.random.randn(N)

# Create a trace
trace0 = go.Scatter(x = Sites, y = 2*np.log(Three_hit))

trace1 = go.Scatter(x = Sites, y = 2*np.log(Two_hit))

data = [trace0, trace1]

plot(data, filename='basic-line_2LogN_EvidenceRATIO.html')
"""

# --- # --- #





""" Sample data from: allOis1_D_100_replicate.1.FITTER.json """

"""
"Evidence Ratios":{
   "Three-hit":    [
[1.001390014360347, 0.9979394029716767, 0.9991241285782849, 1.00127426088317, 0.9985354235854298, 0.9984709455099117, 1.002073311216048, 1.001780281971484, 0.9996103496053033, 1.000756993536668, 1.001991321041256, 1.001680820654508, 1.00463814088762, 1.000043670384645, 0.9981814422553464, 1.000678275074349, 0.9983030440783975, 0.9996434577286832, 0.9998273490880808, 1.000902611347252, 1.001958611016499, 1.000046518632957, 0.9994021901316387, 0.9997382936142335, 1.001932067658296, 0.9987912194703059, 0.9970088386992207, 1.002281105509041, 0.9996634241867047, 0.9997124432731236, 1.000049727304403, 0.9994444639708604, 0.9986522408602755, 1.001944188684811, 1.000299876184699, 0.9976521575025862, 1.001401018378705, 1.001480452953043, 0.9976724401957808, 0.9991589066816811, 0.9980252536464759, 0.9990782285301462, 1.00214852768521, 0.9997288393086416, 0.9985201710290084, 0.9989490074603672, 0.9997767649428708, 0.9982451577557709, 1.002567689222285, 0.9986099280119436, 1.000206099410766, 1.000126910387006, 0.9993446275647343, 0.9996217929220677, 0.9976373949883331, 0.9981304397515073, 1.000014505775352, 0.9998711377442343, 1.001557516147573, 1.000089944257751, 0.9984067241725637, 0.9967236504002286, 0.9997132423844047, 1.000451679998051, 0.9988674849245973, 1.001340793810113, 0.9998968296868783, 1.00362294982541, 0.9986113684723351, 0.9977371138640617, 1.003307041682187, 1.000291931367852, 0.9996722442165997, 1.00057035685794, 1.001882078864379, 1.000082967573986, 0.998013258374147, 0.9985417296750307, 1.000512134400817, 0.9988388596103609, 0.9991457648894445, 1.002090322042013, 0.9986149003824069, 1.002970044779094, 0.9977407796450749, 0.9977958728480721, 1.001302552432428, 1.001144734810204, 1.002224581906339, 0.999915145175538, 0.9998619476056276, 0.9989105462984541, 0.9991141643247188, 1.00274718246144, 1.000506606291668, 1.001665385765126, 0.997853069830942, 1.001697027866775, 1.000640339735564, 0.9998218926358561] 
    ],
   "Two-hit":    [
[1.039479893074982, 0.9584559219606087, 0.9901336700991945, 1.152559507094038, 0.9586173761887439, 1.016569360345624, 1.208177463815821, 0.9470135564853616, 1.025054516566709, 0.9464091830177789, 0.9300909287718737, 1.152917404407017, 0.9834476270960291, 0.8711940985852985, 1.061717481734901, 1.041085748092181, 0.9179235293566413, 0.9470630951136433, 1.039981478503493, 1.019721180587162, 0.9886727326545284, 0.8451116097129812, 1.083881391375342, 1.087613495081031, 0.9459363428649024, 1.049605447841679, 1.120979810616649, 0.7929542359680789, 1.012819825425229, 0.9235488100648367, 0.923709021864677, 0.9692405791705493, 0.8944321248637757, 0.8719705673641486, 1.16202007998144, 0.9246369133142935, 1.05826347189908, 1.051470821893931, 1.013197320818225, 0.969902622574994, 0.8629295841538404, 1.068643335191989, 1.096398738862263, 0.9975678356560851, 1.103052632465649, 0.9259020358296548, 0.9349972573791201, 1.016736936774541, 1.014814598230592, 0.9021998002614513, 1.093779131396377, 1.014388408602677, 1.028342867217236, 1.036390530672396, 0.9825809788658478, 1.049960479628028, 1.105449398434692, 0.8818555529732883, 1.063534189348788, 0.9353434686535685, 0.8661731212374516, 0.9598372156966245, 0.9744800261515797, 1.017680932624984, 1.039124020074141, 0.9679371471477695, 0.986969754257685, 1.113959039760175, 1.010800648718586, 1.197823810172021, 1.14283556798233, 1.047536203363688, 1.167197913599269, 0.9542432632192275, 0.9695313863981695, 1.003308370250275, 1.134924738421028, 0.8559839407497793, 1.035339860472845, 0.9257905708477286, 0.9542217626376227, 0.9337222528956067, 1.033223858505008, 0.9239636717933107, 0.9561732832024701, 1.040970844714394, 0.8288869004373101, 1.08703760095394, 1.13206902340612, 1.023346063792786, 1.059489076056475, 1.025429412044061, 1.001245664670473, 0.9930811388098317, 1.009575481401908, 1.072553923312042, 1.155138332686375, 0.9837695079656531, 1.138731012690168, 1.025937391333278] 
    ]

"""
