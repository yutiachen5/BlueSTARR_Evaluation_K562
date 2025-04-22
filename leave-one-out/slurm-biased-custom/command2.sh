#!/bin/sh
hostname && nvidia-smi && python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/K562/leave-one-out/config-custom/K562_chr2.config /datacommons/igvf-pm/K562/leave-one-out/data-biased /datacommons/igvf-pm/K562/leave-one-out/slurm-biased-custom/outputs/
