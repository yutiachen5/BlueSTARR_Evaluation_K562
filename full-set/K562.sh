#!/bin/sh
#
#SBATCH --get-user-env
#SBATCH -A majoroslab
#SBATCH -J k562
#SBATCH -o /datacommons/igvf-pm/K562/full-set/K562.out
#SBATCH -e /datacommons/igvf-pm/K562/full-set/K562.err
#SBATCH --exclusive
#SBATCH --gres=gpu:1
#SBATCH -p scavenger-gpu,majoroslab-gpu
#SBATCH --nice=100
#SBATCH --mem=102400
#SBATCH --cpus-per-task=1
#

hostname && nvidia-smi && python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/K562/full-set/K562.config /datacommons/igvf-pm/K562/full-set/data-normalized /datacommons/igvf-pm/K562/full-set/K562
