#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 16:32:26 2019

@author: alex


http://phylogeny.lirmm.fr/phylo_cgi/data_converter.cgi
"""
# =============================================================================
# Imports
# =============================================================================
import os, sys
#from Bio import SeqIO
from Bio import SeqIO, Nexus
from Bio.Alphabet import IUPAC
from Bio.Nexus import Nexus

# =============================================================================
# Declares
# =============================================================================
path2 = "/Users/alex/Documents/TRIPLE_HITS/Realignment_testing/fasta/"
path = "/Users/alex/Documents/TRIPLE_HITS/selectome_trip_ammended/"

#filenames = [path + "/" + f.name for f in os.scandir(path) if f.name.endswith(".nex")]
#filenames = ["ENSGT00390000000220.Euteleostomi.002.nex", "ENSGT00530000063148.Euteleostomi.001.nex"]


allfiles = os.listdir(path)
filenames = []

for file in allfiles: 
    #if ".nex" in file:
    filenames.append(path + file)
        
        
# =============================================================================
# Helper functions
# =============================================================================
def writetofile(filename, data, mode):
    #print(filename, data, mode)
    with open(filename, mode) as f:
        if mode == "w+": 
            f.write(data)
            return
        f.write(data + "\n")
    f.close()

def process_nexus_to_fasta(filename, labels, sequences):
    global path2
    #for item in range(len(labels)):
    #    print(labels)
    print("PROCESS:", len(labels), len(sequences))
    if len(labels) == 0: #ERROR
        writetofile("errors.log", filename, "a+")
        return
    #for n, item in enumerate(sequences):
    #    print(n, labels[n], item)
    #print(path + "fasta/" + filename.split("/")[-1].replace(".nex", ".fasta"))
    output_file = path2 + filename.split("/")[-1].replace(".nex", ".fasta")
    
    if os.path.exists(output_file): writetofile(output_file, "", "w+")
    
    for n, item in enumerate(sequences):
        #print(">" + labels[n] + "\n" + item)
        writetofile(output_file, ">" + labels[n] + "\n" + item, "a+")
    
    #print(sequences)
    
def read_nexus(filename):
    print("Opening:", filename)
    labels = []
    aligned_sequences = [] # or {}
    unaligned_sequences = []
    fasta_aligned_data = {}
    fasta_unaligned_data = {}
    TAXLABELS = False
    MATRIX = False
    
    with open(filename, "r") as f:
        for n, line in enumerate(f):
            #print(n, [line])
            
            #taxa labels
            if TAXLABELS == True and "END" in line:
                TAXLABELS = False
                
            if TAXLABELS == True: #processing the labels
                #print("GRAB:", [line])
                data = line.replace("\t\t", "")
                data = data.replace(";\n", "")
                data = data.replace("'", "")
                for item in data.split(" "):
                    if item != "":
                        labels.append(item)
                print("READ NEXUS:", len(labels), labels)
                if len(labels) == 0: #ERROR
                    writetofile("errors.log", filename, "a+")
                    continue
                
            if "TAXLABELS" in line:
                #next line is the taxa labels, grab them
                TAXLABELS = True

            # -- matrix
            if MATRIX == True and "END" in line:
                MATRIX = False
            
            if MATRIX == True: #assigning sequences to labels
                #print("MATRIX:", [line.strip().replace(";", "")])
                sequence = line.strip().replace(";", "")
                aligned_sequences.append(sequence)
                unaligned_sequences.append(sequence.replace("-", ""))
             
            if "MATRIX" in line: MATRIX = True
        f.close()
    #after all that is done for a single, process
    
    process_nexus_to_fasta(filename, labels, unaligned_sequences)
# =============================================================================
# Main
# =============================================================================
    

print("Number of files:", len(filenames))
print()

#sys.exit(10)

for n, file in enumerate(filenames):
    
    #full_filename = path + file
    #full_filename = path + "" + file
    full_filename = file
    output_file = path+""+full_filename.replace(".nex", ".fasta").split("/")[-1]
    #p#rint(file)
    print(n, "Full path:", full_filename)
    print(n, "Output:", output_file)
    print()
    
    read_nexus(full_filename)
    #break
    
    

# =============================================================================
# End of file
# =============================================================================

#filenames = []
#filenames.append("ENSGT00530000063148.Euteleostomi.001.nex")
#filenames.append("ENSGT00390000000220.Euteleostomi.002.nex")

#full_filename = path + filename

"""
from Bio import SeqIO
for record in SeqIO.parse(full_filename, "nexus"):
    #print(record.id)
    pass
"""