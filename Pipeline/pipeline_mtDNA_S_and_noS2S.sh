#!/bin/bash 
clear
echo "## ANALYSIS PIPELINE FOR TRIPLE HITS"
echo "Used for mtDNA analysis"
echo "Current date : $(date) @ $(hostname)"
echo "WD: "$(pwd)
echo ""


#Do variable for FITTERS folder
#VERTEBRATEfitters="/Users/alex/Documents/TRIPLE_HITS/mtDNA/Vertebrate_mtDNA_FITTERS"
#INVERTEBRATEfitters="/Users/alex/Documents/TRIPLE_HITS/mtDNA/Invertebrate_mtDNA_FITTERS"
#COMBINEDfitters="/Users/alex/Documents/TRIPLE_HITS/mtDNA/updatedAnalysis_mtDNA_combined(FASTA_AND_FITTERS)"



# USER CAN SET THIS PRIOR TO THE PIPELINE RUNNING
BASEDIRECTORY="/Users/alex/Documents/TRIPLE_HITS"

FITTERS="/Users/alex/Documents/TRIPLE_HITS/mtDNA/Vertebrate_mtDNA_FITTERS"
FITTERS_NOSS="/Users/alex/Documents/TRIPLE_HITS/mtDNA_noS2S/updatedAnalysis_mtDNA_combined_FITTERS"
CSVFILE="mtDNA_noS2S_Vertebrate_SRV.csv"
CIRCOSTEXTFILE="mtDNA_noS2S_Vertebrate_SRV.txt"
OUTPUT_FOLDER="../analysis/mtDNA_noS2S/Vertebrate"

#FITTERS="/Users/alex/Documents/TRIPLE_HITS/mtDNA/Invertebrate_mtDNA_FITTERS"
#FITTERS_NOSS="/Users/alex/Documents/TRIPLE_HITS/mtDNA_noS2S/updatedAnalysis_mtDNA_combined_FITTERS"
#CSVFILE="mtDNA_noS2S_Invertebrate_SRV.csv"
#CIRCOSTEXTFILE="mtDNA_noS2S_Invertebrate_SRV.txt"
#OUTPUT_FOLDER="../analysis/mtDNA_noS2S/Invertebrate"


# ^^^^^^ USER CAN SET THIS PRIOR TO THE PIPELINE RUNNING ^^^^^^^^

[ -d $OUTPUT_FOLDER ] || mkdir $OUTPUT_FOLDER

#If output file exists, skip

# ==============================================================================
# pipeline_circos_grab_site_substitution_data.py <FITTERS DIRECTORY> <OUTPUTTXT>
# ==============================================================================
echo "(1) Running: pipeline_circos_grab_site_substitution_data.py"
echo "    Saving to: "$OUTPUT_FOLDER/$CIRCOSTEXTFILE

[[ -e $OUTPUT_FOLDER/$CIRCOSTEXTFILE ]] || python pipeline_circos_grab_site_substitution_data.py $FITTERS $OUTPUT_FOLDER/$CIRCOSTEXTFILE > $OUTPUT_FOLDER/pipeline_circos_grab_site_substitution_data.txt

# ==============================================================================
# pipeline_parse_fitter_json.py <FITTERS DIRECTORY> <OUTPUTCSV>
# ==============================================================================
echo ""
echo "(2) Running: pipeline_parse_fitter_json.py"
echo "    Saving to: "$OUTPUT_FOLDER/$CSVFILE

[[ -e $OUTPUT_FOLDER/$CSVFILE ]] || python pipeline_parse_fitter_json.py $FITTERS $OUTPUT_FOLDER/$CSVFILE


# ==============================================================================
# pipeline_plot_csv.py <INPUTCSV> <OUTPUT DIR>
# ==============================================================================
echo ""
echo "(3) Running: pipeline_plot_csv.py"
echo "    Saving to: "$OUTPUT_FOLDER/Plots

[ -e $OUTPUT_FOLDER/pipeline_plot_csv.txt ] || python pipeline_plot_csv.py $OUTPUT_FOLDER/$CSVFILE $OUTPUT_FOLDER/Plots/ > $OUTPUT_FOLDER/pipeline_plot_csv.txt

# ==============================================================================
# pipeline_pvalue_vs_seqlength.py <INPUTCSV>
# ==============================================================================
echo ""
echo "(4) Running: pipeline_pvalue_vs_seqlength.py"
echo "    Saving to: "$OUTPUT_FOLDER/Plots/pvalue_vs_seqlength

#[ -d $OUTPUT_FOLDER/Plots/pvalue_vs_seqlength ] || mkdir $OUTPUT_FOLDER/Plots/pvalue_vs_seqlength
[ -d $OUTPUT_FOLDER/Plots/pvalue_vs_seqlength ] || python pipeline_pvalue_vs_seqlength.py $OUTPUT_FOLDER/$CSVFILE $OUTPUT_FOLDER/Plots/pvalue_vs_seqlength/

# ==============================================================================
# pipeline_plot_2LogEvidenceRatio.py <FITTERDIR> <OUTPUT_DIR>
# ==============================================================================
echo ""
echo "(5) Running: pipeline_plot_2LogEvidenceRatio.py"
echo "    This creates the 2*Ln*Evidence ratio plots"
[ -d $OUTPUT_FOLDER/Plots/EvidenceRatioPlots ] || python pipeline_plot_2LogEvidenceRatio.py $FITTERS $OUTPUT_FOLDER/Plots/EvidenceRatioPlots > $OUTPUT_FOLDER/pipeline_plot_2LogEvidenceRatio.txt

# ==============================================================================
# pipeline_spatial_analysis_THDHSH.py <FITTERDIR> <OUTPUT_DIR>
# ==============================================================================
echo ""
echo "(6) Running: pipeline_spatial_analysis_THDHSH.py"
echo "    Saving to: "$OUTPUT_FOLDER/Plots/spatial_analysis
[ -d $OUTPUT_FOLDER/Plots/spatial_analysis ] || python pipeline_spatial_analysis_THDHSH.py $FITTERS $OUTPUT_FOLDER/Plots/spatial_analysis/ > $OUTPUT_FOLDER/pipeline_spatial_analysis_THDHSH.txt

# ==============================================================================
# pipeline_plot_w_and_wo_Serines.py <FITTERS> <NOS2S_FITTERS> <Output_Dir>
# ==============================================================================
echo ""
echo "(7) Running: pipeline_plot_w_and_wo_Serines.py"
[ -e $OUTPUT_FOLDER/pipeline_plot_w_and_wo_Serines.txt ] || python pipeline_plot_w_and_wo_Serines.py $FITTERS $FITTERS_NOSS $OUTPUT_FOLDER/Plots/ > $OUTPUT_FOLDER/pipeline_plot_w_and_wo_Serines.txt

echo ""
echo " () Done"
# ==============================================================================
# End of pipeline
# ==============================================================================
