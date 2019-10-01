#Jordan Zehr and Alexander G. Lucaci


clear

echo "HYPHY PIPELINE PROGRAM"

HYPHY="/Users/alex/hyphy/HYPHYMP"
LIBPATH="/Users/alex/hyphy/res"
DATA_DIR="/Users/alex/Documents/TRIPLE_HITS/Preprocessing/HIVDB-2017-DNA/HIV1-2017-Filtered/"
BATCH_FILE_PRE="/Users/alex/hyphy-analyses/codon-msa/pre-msa.bf"
BATCH_FILE_POST="/Users/alex/hyphy-analyses/codon-msa/post-msa.bf"


echo "Starting analysis"
echo $HYPHY
echo $LIBPATH
echo $DATA_DIR
echo $BATCH_FILE_PRE

for f in "$DATA_DIR"*.fasta
do
    echo "Processing $f file.."

    $HYPHY LIBPATH=$LIBPATH $BATCH_FILE_PRE --input $f 
done


echo "Running mafft on protein sequences"

for f in "$DATA_DIR"*.fasta
do
   PROTEIN_SEQ=$f"_protein.fas"

   mafft $PROTEIN_SEQ > $f"_protein_aligned.fas"
done

echo $BATCH_FILE_POST

for f in "$DATA_DIR"*.fasta
do
   echo "Post processing $f"
   PROTEIN_MSA=$f"_protein_aligned.fas"

   $HYPHY LIBPATH=$LIBPATH $BATCH_FILE_POST --protein-msa $PROTEIN_MSA --nucleotide-sequences $f"_nuc.fas" --output $f".msa.fas" --compress No
done



#~/hyphy/HYPHYMP LIBPATH=/home/jordanz/hyphy/res pre-msa.bf --input ../../FLTHIV1REV2017DNA.fasta
#mafft FLTHIV1REV2017DNA.fasta_protein.fas > FLTHIV1REV2017DNA.fasta_protein_aligned.fas
#~/hyphy/HYPHYMP LIBPATH=/home/jordanz/hyphy/res post-msa.bf 
#--protein-msa ../../FLTHIV1REV2017DNA.fasta_protein_aligned.fas --nucleotide-sequences ../../FLTHIV1REV2017DNA.fasta_nuc.fas --output ../../FLTHIV1REV2017DNA.msa.fas --compress No
