#!/bin/sh
#
#SBATCH --get-user-env
#SBATCH -A majoroslab
#SBATCH -J K562
#SBATCH -o /work/igvf-pm/K562/full-set/600bp/slurms/train-unbiased-normalized/outputs/%a.out
#SBATCH -e /work/igvf-pm/K562/full-set/600bp/slurms/train-unbiased-normalized/outputs/%a.err
#SBATCH --exclusive
#SBATCH --gres=gpu:1
#SBATCH --array=1-10%10
#SBATCH -p gpu-common,scavenger-gpu,biostat-gpu,majoroslab-gpu,igvf-gpu
#SBATCH --nice=100
#SBATCH --mem=102400
#SBATCH --cpus-per-task=1
#
/work/igvf-pm/K562/full-set/600bp/slurms/train-unbiased-normalized/command${SLURM_ARRAY_TASK_ID}.sh
