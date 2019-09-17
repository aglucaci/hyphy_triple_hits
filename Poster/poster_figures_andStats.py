#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 15:38:23 2019

@author: alexander lucaci


Used to make, generate data for

#Figure 2, delta omega relative to SH
"""

# =============================================================================
# Declares
# =============================================================================
path = "/Users/alex/Documents/TRIPLE_HITS/SELECTOME_TRIP_AMMENDED_SRV_FITTER_JSON"
files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(".json")]


#Figure 2, delta omega relative to SH



#scan through fitters

#grab SH omega

#grab DH, TH omega

#delta TH omega = TH - SH

#delta DH omega = DH - SH


#plots 

#plot TH omega
#plot DH omega


