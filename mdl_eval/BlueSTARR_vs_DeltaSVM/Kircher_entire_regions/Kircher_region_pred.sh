#!/bin/sh
#
#SBATCH --get-user-env
#SBATCH -A majoroslab
#SBATCH -J MUTATE
#SBATCH -o /hpc/group/igvf/K562/mdl_eval/BlueSTARR_vs_DeltaSVM/Kircher_entire_regions/Kircher_region_pred.out
#SBATCH -e /hpc/group/igvf/K562/mdl_eval/BlueSTARR_vs_DeltaSVM/Kircher_entire_regions/Kircher_region_pred.err
#SBATCH --exclusive
#SBATCH --gres=gpu:1
#SBATCH -p gpu-common,scavenger-gpu,biostat-gpu,majoroslab-gpu,igvf-gpu
#SBATCH --mem=20000
#SBATCH --cpus-per-task=1
#

hostname && nvidia-smi && 
source ~/.bashrc
module load BigWig
conda activate /hpc/home/yc583/envs/tf2
python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/mutator2-parent.py /hpc/group/igvf/K562/full-set/300bp/slurms/train-unbiased-normalized/outputs/K562-7 /hpc/group/igvf/K562/mdl_eval/BlueSTARR_vs_DeltaSVM/Kircher_entire_regions/Kircher_region_chunk.txt 300 3000 /hpc/group/igvf/K562/mdl_eval/BlueSTARR_vs_DeltaSVM/Kircher_entire_regions/Kircher_region_pred.txt
