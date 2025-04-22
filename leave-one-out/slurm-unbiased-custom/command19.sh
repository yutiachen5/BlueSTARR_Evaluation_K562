#!/bin/sh
hostname && nvidia-smi && python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/K562/leave-one-out/config-custom/K562_chr19.config /datacommons/igvf-pm/K562/leave-one-out/data-unbiased /datacommons/igvf-pm/K562/leave-one-out/slurm-unbiased-custom/outputs/
