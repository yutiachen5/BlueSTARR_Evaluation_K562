#!/bin/sh
#
#SBATCH --get-user-env
#SBATCH -A majoroslab
#SBATCH -J k562
#SBATCH -o /work/igvf-pm/K562/mdl_eval/slurm-biased/outputs/K562-biased-custom.out
#SBATCH -e /work/igvf-pm/K562/mdl_eval/slurm-biased/outputs/K562-biased-custom.err
#SBATCH --exclusive
#SBATCH --gres=gpu:1
#SBATCH -p majoroslab-gpu,igvf-gpu
#SBATCH --nice=100
#SBATCH --mem=102400
#SBATCH --cpus-per-task=1
#

python /work/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /work/igvf-pm/K562/leave-one-out/BlueSTARR/K562-custom.config /work/igvf-pm/K562/full-set/data-biased /work/igvf-pm/K562/mdl_eval/slurm-biased/outputs/K562-biased-custom