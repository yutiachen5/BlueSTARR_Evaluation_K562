#!/bin/bash
#SBATCH -o query.out
#SBATCH -e query.err
#SBATCH -A majoroslab
#SBATCH -p majoroslab-gpu,igvf-gpu
#SBATCH --mem=10G

module load NCBI-BLAST


QUERY="/hpc/group/igvf/K562/full-set/300bp/data-normalized/all.fasta"
DATABASE="/hpc/group/igvf/K562/leave-one-out/BlueSTARR/leave-one-out/BLASTN/all_indexed"
OUTPUT="/hpc/group/igvf/K562/leave-one-out/BlueSTARR/leave-one-out/BLASTN/all_aligned_300.txt"
EVALUE="1e-5"
OUTFMT="6"


blastn -query $QUERY -db $DATABASE -out $OUTPUT -evalue $EVALUE -outfmt $OUTFMT -sum_stats true -perc_identity 90.0 -word_size 100
echo "Query completed. Results saved to "$OUTPUT