#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:49:59 2019

@author: phylo
"""
import json, csv
import os


#fname = "ENSGT00680000101377.Euteleostomi.001.nex.FITTER.json"
#fout = open(fname + ".csv", "w")


this_row = []

def read_json(filename):
    with open(filename, "r") as fh:
        json_data = json.load(fh)
        
        this_row.append(json_data["input"]["file name"].split("/")[-1])
        this_row.append(json_data["input"]["number of sequences"]) 
        this_row.append(json_data["input"]["number of sites"]) 
        
        
        this_row.append(json_data["test results"]["Double-hit vs single-hit"]["LRT"]) 
        this_row.append(json_data["test results"]["Double-hit vs single-hit"]["p-value"]) 
        this_row.append(json_data["test results"]["Triple-hit vs double-hit"]["LRT"]) 
        this_row.append(json_data["test results"]["Triple-hit vs double-hit"]["p-value"]) 
        this_row.append(json_data["test results"]["Triple-hit vs single-hit"]["LRT"]) 
        this_row.append(json_data["test results"]["Triple-hit vs single-hit"]["p-value"]) 
        
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["AIC-c"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Log Likelihood"])
        
        #"MG94 with double and triple instantaneous substitutions"
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["Substitution rate from nucleotide A to nucleotide C"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["Substitution rate from nucleotide A to nucleotide G"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["Substitution rate from nucleotide A to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["Substitution rate from nucleotide C to nucleotide G"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["Substitution rate from nucleotide C to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["Substitution rate from nucleotide G to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["non-synonymous/synonymous rate ratio"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["rate at which 2 nucleotides are changed instantly within a single codon"])
        this_row.append(json_data["fits"]["MG94 with double and triple instantaneous substitutions"]["Rate Distributions"]["rate at which 3 nucleotides are changed instantly within a single codon"])
        
        #"MG94 with double instantaneous substitutions"
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["Substitution rate from nucleotide A to nucleotide C"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["Substitution rate from nucleotide A to nucleotide G"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["Substitution rate from nucleotide A to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["Substitution rate from nucleotide C to nucleotide G"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["Substitution rate from nucleotide C to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["Substitution rate from nucleotide G to nucleotide T"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["non-synonymous/synonymous rate ratio"])
        this_row.append(json_data["fits"]["MG94 with double instantaneous substitutions"]["Rate Distributions"]["rate at which 2 nucleotides are changed instantly within a single codon"])
        
        #"Standard MG94"
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["Substitution rate from nucleotide A to nucleotide C"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["Substitution rate from nucleotide A to nucleotide G"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["Substitution rate from nucleotide A to nucleotide T"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["Substitution rate from nucleotide C to nucleotide G"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["Substitution rate from nucleotide C to nucleotide T"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["Substitution rate from nucleotide G to nucleotide T"])
        this_row.append(json_data["fits"]["Standard MG94"]["Rate Distributions"]["non-synonymous/synonymous rate ratio"])

        
    fh.close()
    writeto_csv(filename, this_row)

columns = ["file name", "number of sequences", "number of sites", "Double-hit vs single-hit - LRT", "Double-hit vs single-hit - p-value", "Triple-hit vs double-hit - LRT", "Triple-hit vs double-hit - p-value", "Triple-hit vs single-hit - LRT",  "Triple-hit vs single-hit - p-value"]
columns += ["MG94 with double and triple instantaneous substitutions - AIC-c", "MG94 with double and triple instantaneous substitutions - Log Likelihood"]
columns += ["Substitution rate from nucleotide A to nucleotide C", "Substitution rate from nucleotide A to nucleotide G", "Substitution rate from nucleotide A to nucleotide T","Substitution rate from nucleotide C to nucleotide G","Substitution rate from nucleotide C to nucleotide T","Substitution rate from nucleotide G to nucleotide T"]
columns += ["non-synonymous/synonymous rate ratio", "rate at which 2 nucleotides are changed instantly within a single codon","rate at which 3 nucleotides are changed instantly within a single codon"]

columns += ["MG94 with double instantaneous substitutions - AIC-c", "MG94 with double instantaneous substitutions - Log Likelihood"]
columns += ["Substitution rate from nucleotide A to nucleotide C", "Substitution rate from nucleotide A to nucleotide G", "Substitution rate from nucleotide A to nucleotide T","Substitution rate from nucleotide C to nucleotide G","Substitution rate from nucleotide C to nucleotide T","Substitution rate from nucleotide G to nucleotide T"]
columns += ["non-synonymous/synonymous rate ratio", "rate at which 2 nucleotides are changed instantly within a single codon"]

columns += ["Standard MG94 - AIC-c", "Standard MG94 - Log Likelihood"]
columns += ["Substitution rate from nucleotide A to nucleotide C", "Substitution rate from nucleotide A to nucleotide G", "Substitution rate from nucleotide A to nucleotide T","Substitution rate from nucleotide C to nucleotide G","Substitution rate from nucleotide C to nucleotide T","Substitution rate from nucleotide G to nucleotide T"]
columns += ["non-synonymous/synonymous rate ratio"]

#CSV
def writeto_csv(filename, this_row):
    
    
    
    csv_writer = csv.writer(open(filename+".csv", "w"), delimiter=",")
    csv_writer.writerow(columns)
    csv_writer.writerow(this_row)

path = os.getcwd()
files = [path+"/"+f.name for f in os.scandir(path) if f.name.endswith(".json")]

for file in files:
    print(file)
    read_json(file)