#!/bin/bash
#SBATCH -o build.out
#SBATCH -e build.err
#SBATCH -A majoroslab
#SBATCH -p majoroslab-gpu,igvf-gpu
#SBATCH --mem=10G

module load NCBI-BLAST

makeblastdb -in "/hpc/group/igvf/K562/full-set/300bp/data-normalized/all.fasta" -dbtype nucl -out "/hpc/group/igvf/K562/leave-one-out/BlueSTARR/leave-one-out/BLASTN/all_indexed" -hash_index

echo "Custom database built."


