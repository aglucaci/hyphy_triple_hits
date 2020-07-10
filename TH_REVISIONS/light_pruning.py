#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 20:35:01 2020

@author: Alexander G Lucaci
"""
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

import os, sys
import re


#Need to modify the ID of the fasta to just the first part, before the first space

#Also change the chars to all upper space.

FOLDER = "selectome_v06_Euteleostomi-nt_masked"

OUTPUT_DIR = FOLDER + "_mod_remove_N"

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)
    
    
numbers = re.compile ("^\.[0-9]+$")







for root, dirs, files in os.walk(FOLDER):
    for n, each_file in enumerate(files):
        name, ext = os.path.splitext(each_file)
        if len(ext) > 0 and ext in ['.fas'] or numbers.match (ext):
            file = os.path.join (root, name + ext)
            
            print(n, "Processing:", file)
            #print(name, ext)
            
            output_filename = os.path.join(OUTPUT_DIR, name + ext)
            #print("\t", os.path.join(OUTPUT_DIR, name + ext)) 
            
            if os.path.exists(output_filename):
                os.remove(output_filename)
                        
            with open(file, "r") as handle:
                for record in SeqIO.parse(handle, "fasta"): 
                    ID = record.id
                    SEQ = record.seq.upper()
                    #Comment line below to get Original
                    SEQ = str(SEQ).upper().replace("N", "?")
                    

                       
                    # Write to file    
                    with open(output_filename, "a+") as output_handle:
                        #Original
                        #SeqIO.write(SeqRecord(SEQ, id=ID, description=""), output_handle, "fasta")
                        try:
                            SeqIO.write(SeqRecord(Seq(SEQ), id=ID, description=""), output_handle, "fasta")
                        except:
                            print("ERROR:", SEQ)
                            sys.exit(10)
                    output_handle.close()
                            
                    
                #end for
            #end with
        #end if
    #end inner for
#end outer for