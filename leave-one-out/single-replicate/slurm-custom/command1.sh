#!/bin/sh
hostname && nvidia-smi && python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/BlueSTARR-multitask-rep.py /datacommons/igvf-pm/K562/leave-one-out/config-custom/K562_chr1.config /datacommons/igvf-pm/K562/leave-one-out/single-replicate/data-unbiased-single-rep /datacommons/igvf-pm/K562/leave-one-out/single-replicate/slurm-custom/outputs/
