#!/bin/sh
hostname && nvidia-smi && python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/K562/leave-one-out/config-mse/K562_chr20.config /datacommons/igvf-pm/K562/leave-one-out/data-normalized /datacommons/igvf-pm/K562/leave-one-out/slurm-normalized/outputs/
