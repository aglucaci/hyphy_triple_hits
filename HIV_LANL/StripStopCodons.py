# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 12:38:23 2019

@author: admin



@usage
"""

import os

#list of stop codons
#Universal

STOP_CODONS = ["TAA", "TAG", "TGA"]

FASTA_DIRECTORY = r"C:\Users\admin\Documents\HIV_LANL\HIVDB-2017-DNA\HIV1-2017-Filtered"

OUTPUT_DIRECTORY = FASTA_DIRECTORY + "\ForHyphy"

if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)


#Read in fasta files from directory
filenames = [FASTA_DIRECTORY+"/"+f.name for f in os.scandir(FASTA_DIRECTORY) if f.name.endswith(".fasta")]

def process_sequence(sequence):
    print("in process sequence")
    print([sequence[-4:].strip()])
    
    last_3_nts = sequence[-4:].strip()
    
    if last_3_nts in STOP_CODONS:
        #sequence minus the end.
        print("Stripping Stop Codon")
        print("Oriignal:")
        print(sequence)
        print()
        print("Stripped")
        print(sequence[:-4])
        
        stripped_sequence = sequence[:-4]
        
        write_fasta(output_filename, str(stripped_sequence))
        
    print()
    

def read_fasta(file):
    sequence = ""
    
    carrot_count = 0
    
    with open(file, "r") as f:
        
        
        for n, line in enumerate(f):
            #print(n, [line])
            
            
            if line[0] == ">": #start of a sequence
                if carrot_count > 0: process_sequence(sequence)
                
                sequence = line
                carrot_count += 1
                continue
                
            sequence += line
            


def write_fasta(output_file, data):
    print("in write fasta")
    print("Writing to:", output_file)
    with open(output_file, "a+") as f:
        f.writelines(data+"\n")
    f.close()
    
    












#cycle through alignment
for n, file in enumerate(filenames):
    print("Processing:", n, file)
    output_filename = os.path.join(OUTPUT_DIRECTORY, file.split("/")[1])
    #print(output_filename)
    read_fasta(file)

    

#if the last 3 characters end in a stop codon


#write to file.