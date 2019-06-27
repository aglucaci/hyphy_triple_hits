# hyphy_triple_hits

parse_fitter_json.py
-take fitter jsons produced by FitMultiModel.bf and processes them to csv for downstream analysis.
-Is this a better to do this?

plot_csv.py
-takes csv from above and generates plots (bar, box, subplots, overlays, etc).

Serine_to_Serine.py
-to understand codon changes, allows for LRT p-value & ER thresholding 
-uses some code from "grab_site_substituion_data.py "

grab_site_substituion_data.py 
-For circos, creates the data matrix which is used to generate the plot.

plot_2LogEvidenceRatio.py
-Generates 2*LN*EvidenceRatio plots.

analysis_EvidenceRatio.py
-an attempt at analyzing (and thresholding for significant sites) of Evidence ratios

directoryscanner.py
-used for submitting jobs to cluster, outdated
