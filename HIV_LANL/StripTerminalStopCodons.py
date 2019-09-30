# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 12:38:23 2019

@author: Alexander G. Lucaci

@usage:
    
"""
# =============================================================================
# Imports
# =============================================================================
import os


# =============================================================================
# Declares
# =============================================================================
#list of stop codons
#Universal

STOP_CODONS = ["TAA", "TAG", "TGA"]

FASTA_DIRECTORY = "/Users/alex/Documents/TRIPLE_HITS/Preprocessing/HIVDB-2017-DNA/HIV1-2017-Filtered"

OUTPUT_DIRECTORY = FASTA_DIRECTORY + "/ForHyphy"

if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)


#Read in fasta files from directory
filenames = [FASTA_DIRECTORY+"/"+f.name for f in os.scandir(FASTA_DIRECTORY) if f.name.endswith(".fasta")]


# =============================================================================
# Helper functions.
# =============================================================================
"""
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
"""

def internal_stops(sequence):
    global STOP_CODONS
    #remove tag/sequence info
    
    #header = sequence[:tag_index]
    
    tag_index = sequence.find("\n")
    header = sequence[:tag_index]
    
    #print("IN INTERNAL STOPS;", tag_index)
    print("IN INTERNAL STOPS;")
    sequence = sequence[tag_index:]
    
    #clean up newlines
    #print([sequence])
    sequence = sequence.replace("\n", "")
    
    
    #print([sequence])
    
    
    #scan over in bins of 3
    
    codons = [sequence[i:i+3] for i in range(len(sequence)-2, 3)]
    
    for n, codon in enumerate(codons): 
        #print(codon)
        if codon in STOP_CODONS: 
            print("STOP CODON in:", header, "position;", )
            return 1
    
    return 0


def process_sequence(sequence, file):
    global total_num_problematic_sequences
    print("in process sequence")
    #print([sequence[-4:].strip()])
    
    last_3_nts = sequence[-4:].strip()
    
    #Check for STOP codons inside the sequence.
    print()
    print("Checking INTERNAL STOPS.")
    
    """
    print([sequence.replace("\n", "")])
    
    for stop_codon in STOP_CODONS:
        if stop_codon in sequence.replace("\n", ""):
            print("STOP STOP INTERNAL STOP", "#######", stop_codon)
            total_num_problematic_sequences += 1
            break
                  
    print()
    """
    
    total_num_problematic_sequences += internal_stops(sequence)
    
    
    if last_3_nts in STOP_CODONS:
        #sequence minus the end.
        print("Stripping Terminal Stop Codons")
        
        """
        print("Orignal:")
        print(sequence)
        print()
        print("Stripped")
        print(sequence[:-4])
        """
        
        stripped_sequence = sequence[:-4]
        write_fasta(output_filename, str(stripped_sequence))
        
    print()
    

def read_fasta(file):
    global total_num_sequences
    sequence = ""
    
    carrot_count = 0
    
    with open(file, "r") as f:
        
        
        for n, line in enumerate(f):
            #print(n, [line])
            
            
            if line[0] == ">": #start of a sequence
                if carrot_count > 0: 
                    process_sequence(sequence, file)
                    total_num_sequences += 1
                    
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
    
    
# =============================================================================
# Main subroutine.
# =============================================================================

#cycle through alignment
#total_num_sequences = 0
#total_num_problematic_sequences = 0 #number with stop codons inside the sequence.

file_data = []
    
    
for n, file in enumerate(filenames):
    total_num_sequences = 0
    total_num_problematic_sequences = 0 #number with stop codons inside the sequence.
    #if n == 1: break
    print("Processing:", n, file)
    output_filename = os.path.join(OUTPUT_DIRECTORY, file.split("/")[-1])
    #print(output_filename)
    read_fasta(file)
    #total_num_sequences = n

  
    print(file, total_num_sequences, total_num_problematic_sequences)
    
    file_data.append(", ".join([file, str(total_num_sequences), str(total_num_problematic_sequences)]))
    
#if the last 3 characters end in a stop codon


#write to file.
    


for item in file_data: print(item)    
# =============================================================================
# End of file.    
# =============================================================================
