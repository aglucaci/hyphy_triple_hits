# hyphy_triple_hits

### parse_fitter_json.py: 
    -take fitter jsons produced by FitMultiModel.bf and processes them to csv for downstream analysis.  
    -Is there a better way to do this?  

### plot_csv.py
    -takes csv from above and generates plots (bar, box, subplots, overlays, etc).  
    -also provides some statistical analysis of the CSV.  

### Serine_to_Serine.py
    -to understand codon changes, allows for LRT p-value & ER thresholding 
    -uses some code from "grab_site_substituion_data.py "

### physiochemical_triple_changes.py
    -a modification of the Serine_to_Serine.py script.
    -Checks for physiochemical changes with respect to the R group (Nonpolar, Polar, Aromatic, Positive, Negative)
    -Used to make a sankey diagram for viz.

### grab_site_substitution_data.py 
    -For circos, creates the data matrix which is used to generate the plot.

### plot_2LogEvidenceRatio.py
    -Generates 2*LN*EvidenceRatio plots.

### analysis_EvidenceRatio.py
    -an attempt at analyzing (and thresholding for significant sites) of Evidence ratios

### directoryscanner.py
     -used for submitting jobs to cluster, outdated
     
### filescanner.py
     -a modification of directoryscanner.py
     -takes a text file as input, which contains a list of filenames to run analysis on
     -used for submitting jobs to cluster ONLY on these filenames

### NEXUS_Datatype_P_DNA.py
    -ammends/corrects some mislabelling of Selectome datasets
    -DNA sequences labelled as Protein

### plot_pvalue_vs_seqlength.py 
    -a modificiation of the plot_csv.py
    -used to created pvalue versus sequence length scatterplots.
    
    
### convert_nexus_to_fasta.py
    -part of testing realignment
    -takes input as a nexus file
    -can output aligned or unaligned fasta files.
    
### run_alignstat.R
    -used to run alignstat (generates quality scores for alignments)
    
