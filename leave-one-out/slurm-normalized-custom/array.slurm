#!/bin/sh
#
#SBATCH --get-user-env
#SBATCH -J k562-normalized
#SBATCH -o /datacommons/igvf-pm/K562/leave-one-out/slurm-normalized-custom/outputs/%a.out
#SBATCH -e /datacommons/igvf-pm/K562/leave-one-out/slurm-normalized-custom/outputs/%a.err
#SBATCH --exclusive
#SBATCH --gres=gpu:1
#SBATCH --array=1-4%24
#SBATCH -p majoroslab-gpu,scavenger-gpu
#SBATCH --nice=100
#SBATCH --mem=102400
#SBATCH --cpus-per-task=1
#
/datacommons/igvf-pm/K562/leave-one-out/slurm-normalized-custom/command${SLURM_ARRAY_TASK_ID}.sh
