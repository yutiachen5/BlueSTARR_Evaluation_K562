#!/bin/sh
#
#SBATCH --get-user-env
#SBATCH -A majoroslab
#SBATCH -J attention-layer
#SBATCH -o /datacommons/igvf-pm/K562/leave-one-out/attention-layer/slurm/attention-layer-4.out
#SBATCH -e /datacommons/igvf-pm/K562/leave-one-out/attention-layer/slurm/attention-layer-4.err
#SBATCH --exclusive
#SBATCH --gres=gpu:1
#SBATCH -p majoroslab-gpu
#SBATCH --nice=100
#SBATCH --mem=102400
#SBATCH --cpus-per-task=1
#
hostname && nvidia-smi && python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/BlueSTARR-multitask-K562.py /datacommons/igvf-pm/K562/leave-one-out/attention-layer/config/K562_chr1_4.config /datacommons/igvf-pm/K562/leave-one-out/data-normalized /datacommons/igvf-pm/K562/leave-one-out/attention-layer/slurm/outputs-4/
