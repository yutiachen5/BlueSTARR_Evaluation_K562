#!/bin/sh
hostname && nvidia-smi && python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/BlueSTARR-multitask-rep.py /datacommons/igvf-pm/K562/leave-one-out/config-mse/K562_chrX.config /datacommons/igvf-pm/K562/leave-one-out/single-replicate/data-unbiased-single-rep /datacommons/igvf-pm/K562/leave-one-out/single-replicate/slurm-mse/outputs/
