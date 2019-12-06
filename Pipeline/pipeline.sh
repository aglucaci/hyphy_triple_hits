#!/bin/bash 
clear
echo "## ANALYSIS PIPELINE FOR Multiple Instantaneous Substitutions (MIS) NEW RESULTS"
echo "## Updated 12-4-2019"
echo "Current date : $(date) @ $(hostname)"
echo "WD: "$(pwd)

#Do variable for FITTERS folder


# USER CAN SET THIS PRIOR TO THE PIPELINE RUNNING
# PROJECT DIRECTORY

BASEDIRECTORY="/Users/alex/Documents/MIS_NEW_RESULTS"

TAG="PETROV"
FITTERS="/Users/alex/Documents/MIS_NEW_RESULTS/Data/"$TAG

CSVFILE=$TAG"_SRV_nr.csv"
CSVFILEV02=$TAG"_SRV_nr_v02.csv"

CIRCOSTEXTFILE1="CIRCOS_"$TAG"_SRV_TH_nr.txt"

#This is all TH's thresholded for THvsDH LRT  p value 0.05
CIRCOSTEXTFILE2="CIRCOS_"$TAG"_SRV_nr_Thresholded_p0_05.txt"

CIRCOSTEXTFILE3="CIRCOS_"$TAG"_SRV_DH_nr.txt"

OUTPUT_FOLDER=$BASEDIRECTORY"/Analysis/"$TAG"_SRV_nr"


#TAG=""
#FITTERS="/Users/alex/Documents/MIS_NEW_RESULTS/SELECTOME"
#CSVFILE="SELECTOME_SRV_nr.csv"
#CSVFILEV02="SELECTOME_SRV_nr_v02.csv"
#CIRCOSTEXTFILE1="CIRCOS_SELECTOME_SRV_nr.txt"

#This is all TH's thresholded for THvsDH LRT  p value 0.05
#CIRCOSTEXTFILE2="CIRCOS_SELECTOME_SRV_nr_Thresholded_p0_05.txt"

#OUTPUT_FOLDER=$BASEDIRECTORY"/SELECTOME_SRV_nr"

#Skip creating Evidence ratio plots? 1 for yes, 0 for no (This can take awhile)
SKIP_EVIDENCERATIOPLOTS=1

# ^^^^^^ USER CAN SET THIS PRIOR TO THE PIPELINE RUNNING ^^^^^^^^
echo "FITTERS FOLDER: "$FITTERS
echo "File count: "$(ls $FITTERS | wc -l)
echo ""

[ -d $OUTPUT_FOLDER ] || mkdir $OUTPUT_FOLDER

#If output file exists, skip
# ==============================================================================
# pipeline_circos_grab_site_substitution_data.py <FITTERS DIRECTORY> <OUTPUTTXT>
# ==============================================================================
echo "(1) Running: pipeline_circos_grab_site_substitution_data.py"
echo "    Saving to: "$OUTPUT_FOLDER/$CIRCOSTEXTFILE1
echo "    Logfile: "$OUTPUT_FOLDER/pipeline_circos_grab_site_substitution_data.txt 

#rm -f $OUTPUT_FOLDER/$CIRCOSTEXTFILE
#[[ -e $OUTPUT_FOLDER/$CIRCOSTEXTFILE ]] || 
[[ -e $OUTPUT_FOLDER/$CIRCOSTEXTFILE1 ]] || python pipeline_circos_grab_site_substitution_data.py $FITTERS $OUTPUT_FOLDER/$CIRCOSTEXTFILE1 10000 > $OUTPUT_FOLDER/pipeline_circos_grab_site_substitution_data.txt 
#python pipeline_circos_grab_site_substitution_data.py $FITTERS $OUTPUT_FOLDER/$CIRCOSTEXTFILE

# ==============================================================================
# pipeline_circos_grab_site_substitution_data.py <FITTERS DIRECTORY> <OUTPUTTXT>
# ==============================================================================
echo ""
echo "(1.1) Running: pipeline_circos_grab_site_substitution_data.py"
echo "    Saving to: "$OUTPUT_FOLDER/$CIRCOSTEXTFILE2
echo "    Logfile: "$OUTPUT_FOLDER/pipeline_circos_grab_site_substitution_data_pvalue.txt 

[[ -e $OUTPUT_FOLDER/$CIRCOSTEXTFILE2 ]] || python pipeline_circos_grab_site_substitution_data.py $FITTERS $OUTPUT_FOLDER/$CIRCOSTEXTFILE2 0.05 > $OUTPUT_FOLDER/pipeline_circos_grab_site_substitution_data_pvalue.txt 

# ==============================================================================
# pipeline_circos_grab_site_substitution_data.py <FITTERS DIRECTORY> <OUTPUTTXT>
# ==============================================================================
echo ""
echo "(1.2) Running: pipeline_circos_grab_site_substitution_data_DH.py"
echo "    Saving to: "$OUTPUT_FOLDER/$CIRCOSTEXTFILE3
echo "    Logfile: "$OUTPUT_FOLDER/pipeline_circos_grab_site_substitution_data_DH.txt

[[ -e $OUTPUT_FOLDER/$CIRCOSTEXTFILE3 ]] || python pipeline_circos_grab_site_substitution_data_DH.py $FITTERS $OUTPUT_FOLDER/$CIRCOSTEXTFILE3 > $OUTPUT_FOLDER/pipeline_circos_grab_site_substitution_data_DH.txt


# ==============================================================================
# pipeline_parse_fitter_json.py <FITTERS DIRECTORY> <OUTPUTCSV>
# ==============================================================================
echo ""
echo "(2) Running: pipeline_parse_fitter_json.py"
echo "    Saving to: "$OUTPUT_FOLDER/$CSVFILE
[[ -e $OUTPUT_FOLDER/$CSVFILE ]] || python pipeline_parse_fitter_json.py $FITTERS $OUTPUT_FOLDER/$CSVFILE

# ==============================================================================
# pipeline_parse_FITTERS_v02.py <FITTERS DIRECTORY> <OUTPUTCSV>
# Will output branch lengths and total tree length.
# ==============================================================================
echo ""
echo "(2a) Running: pipeline_parse_FITTERS_v02.py"
echo "    Saving to: "$OUTPUT_FOLDER/$CSVFILE
[[ -e $OUTPUT_FOLDER/$CSVFILEV02 ]] || python pipeline_parse_FITTERS_v02.py $FITTERS $OUTPUT_FOLDER/$CSVFILEV02

# ==============================================================================
# pipeline_plot_csv.py <INPUTCSV>
# ==============================================================================
echo ""
echo "(3) Running: pipeline_plot_csv.py"
echo "    Saving to: "$OUTPUT_FOLDER/Plots
echo "    Logfile: "$OUTPUT_FOLDER/pipeline_plot_csv.txt
[ -d $OUTPUT_FOLDER/Plots ] || python pipeline_plot_csv.py $OUTPUT_FOLDER/$CSVFILE $OUTPUT_FOLDER/Plots/ $FITTERS > $OUTPUT_FOLDER/pipeline_plot_csv.txt
#python pipeline_plot_csv.py $OUTPUT_FOLDER/$CSVFILE $OUTPUT_FOLDER/Plots/ $FITTERS
#python pipeline_plot_csv.py $OUTPUT_FOLDER/$CSVFILE $OUTPUT_FOLDER/Plots/

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
if [ $SKIP_EVIDENCERATIOPLOTS -eq 0 ]
then
    [ -d $OUTPUT_FOLDER/Plots/EvidenceRatioPlots ] || python pipeline_plot_2LogEvidenceRatio.py $FITTERS $OUTPUT_FOLDER/Plots/EvidenceRatioPlots
else
    echo "    Skipping.."
fi

# ==============================================================================
# pipeline_analysis_EvidenceRatio.py <FITTER_DIR> <OUTPUT_DIR> <OUTPUT_FILENAME>
# ==============================================================================
echo ""
echo "(6) Running: pipeline_analysis_EvidenceRatio.py"
echo "    This creates some summary statistics for my Evidence Ratios"
[ -e $OUTPUT_FOLDER/pipeline_analysis_EvidenceRatio_log.txt ] || python pipeline_analysis_EvidenceRatio.py $FITTERS $OUTPUT_FOLDER "pipeline_analysis_EvidenceRatio.txt" > $OUTPUT_FOLDER/pipeline_analysis_EvidenceRatio_log.txt

# ==============================================================================
# pipeline_spatial_analysis_THDHSH.py <FITTERDIR> <OUTPUT_DIR>
# ==============================================================================
#echo ""
#echo "(7) Running: pipeline_spatial_analysis_THDHSH.py"
#echo "    Saving to: "$OUTPUT_FOLDER/Plots/spatial_analysis
#[ -d $OUTPUT_FOLDER/Plots/spatial_analysis ] || python pipeline_spatial_analysis_THDHSH.py $FITTERS $OUTPUT_FOLDER/Plots/spatial_analysis > $OUTPUT_FOLDER/pipeline_spatial_analysis_THDHSH.txt

# ==============================================================================
# spatial analysis part 2
# ==============================================================================
echo ""
echo "(7.2) Running: pipeline_spatialanalysis_09102019.py"
echo "    This is an updated (version 2.0) of the spatial analysis."
python pipeline_spatialanalysis_09102019.py $FITTERS $OUTPUT_FOLDER/Plots/spatial_analysis/

# ==============================================================================
# pipeline_plot_w_and_wo_Serines.py <FITTERS> <NOS2S_FITTERS> <Output_Dir>
# ==============================================================================
echo ""
echo "(8) Running: pipeline_plot_w_and_wo_Serines.py"
echo "    This looks at the contribution of Serines to TH signal"

if [ ! -z $FITTERS_NOSS ]
then
    echo "    Testing all files"
    [ -e $OUTPUT_FOLDER/pipeline_plot_w_and_wo_Serines.txt ] || python pipeline_plot_w_and_wo_Serines.py $FITTERS $FITTERS_NOSS $OUTPUT_FOLDER/Plots/ > $OUTPUT_FOLDER/pipeline_plot_w_and_wo_Serines.txt False
    echo "    pvalue thresholding"
    [ -e $OUTPUT_FOLDER/pipeline_plot_w_and_wo_Serines_pvalue_threshold.txt ] || python pipeline_plot_w_and_wo_Serines.py $FITTERS $FITTERS_NOSS $OUTPUT_FOLDER/Plots/ > $OUTPUT_FOLDER/pipeline_plot_w_and_wo_Serines_pvalue_threshold.txt True
else
    echo "    Skipping..."
fi

echo ""
echo " () Done"


# ==============================================================================
# End of pipeline
# ==============================================================================

# ==============================================================================
# 
# ==============================================================================
