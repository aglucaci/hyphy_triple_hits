#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 19:51:20 2020

@author: Alexander G. Lucaci
"""



import os


#Step 1 - Process Data
"""
Reads through the data, sees where we have files that agree (overlap in both aBSREL and aBSREL-MH).
Creates an intermediate file, a csv file of input filenames, delta cAIC and delta LRT p-values
"""

os.system("python Model.py")


# Step 2 - Create visuals

"""
Inputs the csv file created above, creates histograms.

"""