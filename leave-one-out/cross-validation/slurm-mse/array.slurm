#!/bin/sh
#
#SBATCH --get-user-env
#SBATCH -A majoroslab
#SBATCH -J K562-cv
#SBATCH -o /datacommons/igvf-pm/K562/leave-one-out/cross-validation/slurm-mse/outputs/%a.out
#SBATCH -e /datacommons/igvf-pm/K562/leave-one-out/cross-validation/slurm-mse/outputs/%a.err
#SBATCH --exclusive
#SBATCH --gres=gpu:1
#SBATCH --array=1-24%24
#SBATCH -p majoroslab-gpu,scavenger-gpu
#SBATCH --nice=100
#SBATCH --mem=50000
#SBATCH --cpus-per-task=1
#
/datacommons/igvf-pm/K562/leave-one-out/cross-validation/slurm-mse/command${SLURM_ARRAY_TASK_ID}.sh
