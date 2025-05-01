#=========================================================================
# This is OPEN SOURCE SOFTWARE governed by the Gnu General Public
# License (GPL) version 3, as described at www.opensource.org.
# Copyright (C)2016 William H. Majoros (martiandna@gmail.com).
#=========================================================================
from __future__ import (absolute_import, division, print_function,
   unicode_literals, generators, nested_scopes, with_statement)
from builtins import (bytes, dict, int, list, object, range, str, ascii,
   chr, hex, input, next, oct, open, pow, round, super, filter, map, zip)
import os

#=========================================================================
# Attributes:
#   commands : array of string
#   niceValue : empty, or integer (nice value)
#   memValue : empty, or integer (mem value, in megabytes)
#   queue : partition name
#   threadsValue : number of CPUs requested
# Instance Methods:
#   SlurmWriter()
#   slurm.addCommand(cmd)
#   slurm.nice() # turns on "nice" (sets it to 100 by default)
#   slurm.mem(1500)
#   slurm.threads(16)
#   slurm.setQueue("new,all")
#   slurm.writeArrayScript(slurmDir,jobName,maxParallel,
#                           additional_SBATCH_lines)
#=========================================================================
class SlurmWriter:
    """SlurmWriter"""
    def __init__(self):
        self.commands=[]
        self.niceValue=0
        self.memValue=0
        self.threadsValue=0
        self.queue=None

    def addCommand(self,cmd):
        self.commands.append(cmd)

    def clearCommands(self):
        self.commands=[]

    def nice(self,value=100):
        self.niceValue=value

    def mem(self,value):
        self.memValue=value

    def threads(self,value):
        self.threadsValue=value
        
    def setQueue(self,value):
        self.queue=value

    def writeArrayScript(self,slurmDir,jobName,maxParallel,moreSBATCH=""):
        if(moreSBATCH is None): moreSBATCH=""
        if(int(maxParallel)<1): raise Exception("specify maxParallel parameter")
        moreSBATCH=moreSBATCH.rstrip()
        if(len(moreSBATCH)>0):
            moreSBATCH=moreSBATCH.rstrip()+"\n"
        #moreSBATCH=moreSBATCH+"\n"
        if(self.niceValue>0) :
            moreSBATCH+="#SBATCH --nice="+str(self.niceValue)+"\n"
        if(self.memValue>0):
            moreSBATCH+="#SBATCH --mem="+str(self.memValue)+"\n"
        if(self.threadsValue>0):
            moreSBATCH+="#SBATCH --cpus-per-task="+str(self.threadsValue)+"\n"
        queue=""
        if(len(self.queue)>0):
            queue="#SBATCH -p "+self.queue+"\n"
        if(os.path.exists(slurmDir)):
               os.system("rm -f "+slurmDir+"/*.slurm "+slurmDir+
                         "/outputs/*.output")
        os.system("mkdir -p "+slurmDir+"/outputs")
        commands=self.commands
        numCommands=len(commands)
        numJobs=numCommands

        start = 1 # default: 1
        for i in range(start-1,start-1+numCommands):
            command=commands[i-start+1]
            index=i+1
            filename=slurmDir+"/command"+str(index)+".sh"
            with open(filename,"w") as OUT:
                OUT.write("#!/bin/sh\n")
                OUT.write(command+"\n")
            os.system("chmod +x "+filename) # adds the executable permission 
        filename=slurmDir+"/array.slurm"
        with open(filename,"w") as OUT:
            OUT.write("\n".join(
                    ["#!/bin/sh",
                     "#",
                     "#SBATCH --get-user-env",
                     "#SBATCH -A majoroslab",
                     "#SBATCH -J "+jobName,
                     "#SBATCH -o "+slurmDir+"/outputs/%a.out", # a% job id index
                     "#SBATCH -e "+slurmDir+"/outputs/%a.err",
                     "#SBATCH --exclusive",
                     "#SBATCH --gres=gpu:1",
                    #  "#SBATCH --array=1-"+str(numJobs)+"%"+str(maxParallel),
                     "#SBATCH --array="+str(start)+"-"+str(start-1+numJobs)+"%"+str(maxParallel),
                    #  "#SBATCH --exclude=dcc-youlab-gpu-[01-57]",
                     queue+moreSBATCH+"#",
                     slurmDir+"/command${SLURM_ARRAY_TASK_ID}.sh\n",
                     ]))
    def writeScript(self,slurmFile,outFile,jobName,command,moreSBATCH=""):
        if(moreSBATCH is None): moreSBATCH=""
        moreSBATCH=moreSBATCH.rstrip()
        if(len(moreSBATCH)>0):
            moreSBATCH=moreSBATCH.rstrip()+"\n"
        if(self.niceValue>0) :
            moreSBATCH+="#SBATCH --nice="+str(self.niceValue)+"\n"
        if(self.memValue>0):
            moreSBATCH+="#SBATCH --mem="+str(self.memValue)+"\n"
        if(self.threadsValue>0):
            moreSBATCH+="#SBATCH --cpus-per-task="+str(self.threadsValue)+"\n"
        queue=""
        if(len(self.queue)>0):
            queue="#SBATCH -p "+self.queue+"\n"
        with open(slurmFile,"w") as OUT:
            OUT.write("\n".join(
                    ["#!/bin/sh",
                     "#",
                     "#SBATCH --get-user-env",
                     "#SBATCH -A majoroslab",
                     "#SBATCH -J "+jobName,
                     "#SBATCH -o "+outFile+'.out',
                     "#SBATCH -e "+outFile+'.err',
                     "#SBATCH --exclusive",
                    #  "#SBATCH --exclude=dcc-youlab-gpu-[01-57]",
                     "#SBATCH --gres=gpu:1",
                     queue+moreSBATCH+"#",
                     command
                     ]))

slurm = SlurmWriter()
chr_ls = ['chr'+str(x) for x in range(1,23)]+["X","Y"]
CRE_ls = [str(x) for x in range(1,1065)]
VAR_ls = [str(x) for x in range(1,268)]
fc_ls = ['chr1-b-ap1-b-gr','chr1-b-ap1-f-gr','chr1-f-ap1-b-gr','chr1-f-ap1-f-gr']
labels = ['AZD2906','AZD9567','CORT108297','CpdA','GW870086','Hydrocortisone','Mapracorat','RU486','ZK216348']

# for i in range(0,len(fc_ls)):
# for i in range(0,len(chr_ls)):
for i in range(1,6):
# for i in range(len(VAR_ls)):
# for i in range(len(CRE_ls)):
# for i in range(10):
    # config = chr_ls[i]+'.config'

    # slurm.addCommand('hostname && nvidia-smi && python /hpc/home/yc583/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/K562/leave-one-out/config/'+config+
    #                 ' /datacommons/igvf-pm/K562/leave-one-out/data /datacommons/igvf-pm/K562/leave-one-out/slurm/outputs/')
    # slurm.addCommand('hostname && nvidia-smi && python /hpc/home/yc583/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/A549/leave-one-out/config/'+config+
    #                 ' /datacommons/igvf-pm/A549/leave-one-out/data /datacommons/igvf-pm/A549/leave-one-out/slurm/outputs/')
    # slurm.addCommand('hostname && nvidia-smi && python /hpc/home/yc583/BlueSTARR/BlueSTARR-multitask-aver.py /datacommons/igvf-pm/A549/leave-one-out/Dex-200/config-custom/'+config+
    #                     ' /datacommons/igvf-pm/A549/leave-one-out/Dex-200/data-1-1 /datacommons/igvf-pm/A549/leave-one-out/Dex-200/slurm-1-1/outputs/')
    # slurm.addCommand('hostname && nvidia-smi && python /hpc/home/yc583/BlueSTARR/BlueSTARR-multitask-aver.py /datacommons/igvf-pm/A549/leave-one-out/DMSO-200/config-custom/'+config+
    #                     ' /datacommons/igvf-pm/A549/leave-one-out/DMSO-200/data-1-1 /datacommons/igvf-pm/A549/leave-one-out/DMSO-200/slurm-1-1/outputs/')
    # slurm.addCommand('hostname && nvidia-smi && python /hpc/home/yc583/BlueSTARR/BlueSTARR-multitask-aver.py /datacommons/igvf-pm/A549/leave-one-out/DMSO-200/config-mse/'+config+
    #                     ' /datacommons/igvf-pm/A549/leave-one-out/DMSO-200/data-unbiased /datacommons/igvf-pm/A549/leave-one-out/DMSO-200/slurm/outputs/')
    # slurm.addCommand('hostname && nvidia-smi && python /hpc/home/yc583/BlueSTARR/BlueSTARR-multitask-aver.py /datacommons/igvf-pm/A549/leave-one-out/Dex-200/config-mse/'+config+
    #                     ' /datacommons/igvf-pm/A549/leave-one-out/Dex-200/data-unbiased /datacommons/igvf-pm/A549/leave-one-out/Dex-200/slurm/outputs/')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/cross-validation.py /datacommons/igvf-pm/K562/leave-one-out/config-custom/K562_' + config +
    #                     ' /datacommons/igvf-pm/K562/leave-one-out/data-unbiased /datacommons/igvf-pm/K562/leave-one-out/slurm-unbiased-custom/outputs/ /hpc/home/yc583/BlueSTARR/leave-one-out/cv/cv-full/cv-custom')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/cross-validation.py /datacommons/igvf-pm/K562/leave-one-out/config-custom/K562_' + config +
    #                     ' /datacommons/igvf-pm/K562/leave-one-out/data-normalized /datacommons/igvf-pm/K562/leave-one-out/slurm-normalized-custom/outputs/ /hpc/home/yc583/BlueSTARR/leave-one-out/cv/cv-full/cv-custom-normalized')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/cross-validation.py /datacommons/igvf-pm/K562/leave-one-out/config-mse/K562_' + config +
    #                     ' /datacommons/igvf-pm/K562/leave-one-out/data-normalized /datacommons/igvf-pm/K562/leave-one-out/slurm-normalized-mse/outputs/ /datacommons/igvf-pm/K562/leave-one-out/cross-validation/slurm-normalized-mse/outputs')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/cross-validation.py /datacommons/igvf-pm/K562/leave-one-out/config-mse/' + config +
    #                     ' /datacommons/igvf-pm/K562/leave-one-out/data-unbiased /datacommons/igvf-pm/K562/leave-one-out/slurm-unbiased-mse/outputs/ /datacommons/igvf-pm/K562/leave-one-out/cross-validation/slurm-mse/outputs')
    # slurm.addCommand('hostname && nvidia-smi && python /hpc/home/yc583/BlueSTARR/BlueSTARR-multitask-aver.py /datacommons/igvf-pm/A549/leave-one-out/DMSO-200/config-mse/'+config+
    #                     ' /datacommons/igvf-pm/A549/leave-one-out/DMSO-200/data-normalized /datacommons/igvf-pm/A549/leave-one-out/DMSO-200/slurm-normalized-mse/outputs/')
    # slurm.addCommand('hostname && nvidia-smi && python /hpc/home/yc583/BlueSTARR/BlueSTARR-multitask-aver.py /datacommons/igvf-pm/A549/leave-one-out/Dex-200/config-mse/'+config+
    #                     ' /datacommons/igvf-pm/A549/leave-one-out/Dex-200/data-normalized /datacommons/igvf-pm/A549/leave-one-out/Dex-200/slurm-normalized-mse/outputs/')
    # slurm.addCommand('hostname && nvidia-smi && python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/BlueSTARR-multitask-K562.py /datacommons/igvf-pm/K562/leave-one-out/config-custom/K562_'+config+ 
    #                     ' /datacommons/igvf-pm/K562/leave-one-out/data-normalized /datacommons/igvf-pm/K562/leave-one-out/slurm-normalized-custom/outputs/')
    # slurm.addCommand('hostname && nvidia-smi && python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/BlueSTARR-multitask-K562.py /datacommons/igvf-pm/K562/leave-one-out/config-mse/K562_'+config+ 
    #                     ' /datacommons/igvf-pm/K562/leave-one-out/data-normalized /datacommons/igvf-pm/K562/leave-one-out/slurm-normalized-mse/outputs/')
    # slurm.addCommand('hostname && nvidia-smi && python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/full-set/DMSO-200 /datacommons/igvf-pm/A549/GR-AP1/ref-seq/DMSO-200/'+chr_ls[i]+
    #                         '.txt /datacommons/igvf-pm/A549/GR-AP1/ref-score/DMSO-200/'+chr_ls[i]+'.txt')
    # slurm.addCommand('hostname && nvidia-smi && python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/full-set/Dex-200 /datacommons/igvf-pm/A549/GR-AP1/ref-seq/Dex-200/'+chr_ls[i]+
    #                         '.txt /datacommons/igvf-pm/A549/GR-AP1/ref-score/Dex-200/'+chr_ls[i]+'.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-fc.py /datacommons/igvf-pm/A549/full-set/DMSO-200 /datacommons/igvf-pm/A549/full-set/Dex-200 /datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/generated-seq/single-based/chr1-f-ap1-f-gr.txt /datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/fc-full/Dex-DMSO/single-based/chr1-f-ap1-f-gr-fc.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-fc.py /datacommons/igvf-pm/A549/full-set/DMSO-200 /datacommons/igvf-pm/A549/full-set/Dex-200 /datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/generated-seq/chr1-f-ap1-f-gr.txt /datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/fc-full/Dex-DMSO/chr1-f-ap1-f-gr-fc.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-fc.py /datacommons/igvf-pm/A549/full-set/DMSO-200/DMSO-200-maxpooling /datacommons/igvf-pm/A549/full-set/Dex-200/Dex-200-maxpooling /datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/generated-seq/chr1-f-ap1-f-gr.txt /datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/fc-full/Dex-DMSO/max-pooling/chr1-f-ap1-f-gr-fc.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-fc.py /datacommons/igvf-pm/A549/full-set/DMSO-200/DMSO-200-attention /datacommons/igvf-pm/A549/full-set/Dex-200/Dex-200-attention /datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/generated-seq/chr1-f-ap1-f-gr.txt /datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/fc-full/Dex-DMSO/attention/chr1-f-ap1-f-gr-fc.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-fc.py /datacommons/igvf-pm/A549/full-set/DMSO-200/DMSO-200-pos1 /datacommons/igvf-pm/A549/full-set/Dex-200/Dex-200-pos1 /datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/generated-seq/chr1-f-ap1-f-gr.txt /datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/fc-full/Dex-DMSO/attention-pos/chr1-f-ap1-f-gr-fc.txt')
    # slurm.addCommand('hostname && nvidia-smi && '+'\n'+
    #                 'source ~/.bashrc'+'\n'+
    #                 'module load BigWig'+'\n'+
    #                 'conda activate /hpc/home/yc583/envs/tf2'+'\n'+
    #                 'python /work/igvf-pm/K562/leave-one-out/BlueSTARR/mutator2-parent.py /work/igvf-pm/K562/full-set/K562 /work/igvf-pm/K562/CRE-preds/chunks/CREs'+CRE_ls[i]+
    #                 '.txt 300 3000 /work/igvf-pm/K562/CRE-preds/preds/pred'+CRE_ls[i]+'.txt')
    # slurm.addCommand('hostname && nvidia-smi'+'\n'+
    #                 'python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/BlueSTARR-multitask-A549.py /datacommons/igvf-pm/A549/leave-one-out/DMSO-200/config-mse/A549_'+config+
    #                  ' /datacommons/igvf-pm/A549/leave-one-out/DMSO-200/600-bases/data-normalized /datacommons/igvf-pm/A549/leave-one-out/DMSO-200/600-bases/slurm-normalized-mse/outputs/')
    # slurm.addCommand('hostname && nvidia-smi'+'\n'+
    #                 'python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/BlueSTARR-multitask-A549.py /datacommons/igvf-pm/A549/leave-one-out/Dex-200/config-mse/A549_'+config+
    #                  ' /datacommons/igvf-pm/A549/leave-one-out/Dex-200/600-bases/data-normalized /datacommons/igvf-pm/A549/leave-one-out/Dex-200/600-bases/slurm-normalized-mse/outputs/')
    # slurm.addCommand('hostname && nvidia-smi && python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/full-set/DMSO-200/600-bases/DMSO-200-1 /datacommons/igvf-pm/A549/GR-AP1/ref-seq/DMSO-200/600-bases/'+chr_ls[i]+
    #                         '.txt /datacommons/igvf-pm/A549/GR-AP1/ref-score/DMSO-200/600-bases/'+chr_ls[i]+'.txt')
    # slurm.addCommand('hostname && nvidia-smi && python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/full-set/Dex-200/600-bases/Dex-200 /datacommons/igvf-pm/A549/GR-AP1/ref-seq/Dex-200/600-bases/'+chr_ls[i]+
    #                         '.txt /datacommons/igvf-pm/A549/GR-AP1/ref-score/Dex-200/600-bases/'+chr_ls[i]+'.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-fc.py /datacommons/igvf-pm/A549/full-set/DMSO-200/600-bases/DMSO-200 /datacommons/igvf-pm/A549/full-set/Dex-200/600-bases/Dex-200 /datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/generated-seq/600-bases/'+\
    #                 fc_ls[i] +'.txt /datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/fc-full/Dex-DMSO/600-bases/'+fc_ls[i]+'-fc.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-fc.py /datacommons/igvf-pm/A549/full-set/DMSO-200/600-bases/saved_models/DMSO-200-tf+pos /datacommons/igvf-pm/A549/full-set/Dex-200/600-bases/saved_models/Dex-200-tf+pos '+\
    #                 '/datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/generated-seq/600-bases/tf+pos/'+ fc_ls[i]+'.txt /datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/fc-full/Dex-DMSO/600-bases/tf+pos/'+fc_ls[i]+'-fc.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-fc.py /datacommons/igvf-pm/A549/full-set/DMSO-200/600-bases/saved_models/DMSO-200-1005 /datacommons/igvf-pm/A549/full-set/Dex-200/600-bases/saved_models/Dex-200-1005 '+\
    #                 '/datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/generated-seq/600-bases/'+ fc_ls[i]+'.txt /datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/fc-full/Dex-DMSO/600-bases/default-2/'+fc_ls[i]+'-fc.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/Dex-200-lognormal10-' +str(i)
    #                     +' /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/Dex-200-biased/low_act_5000_test.txt /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/Dex-200-biased/low_act_5000_test_pred_lognormal10_'+str(i)+'.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/Dex-200-unbiased' +str(i)
    #                     +' /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/Dex-200-biased/low_act_5000_test.txt /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_test_pred_unbiased_'+str(i)+'.txt')

    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.003/slurm-unbiased-train/outputs/Dex-200-unbiased-0.003-' +str(i)
    #                     +' /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/Dex-200-biased/low_act_5000_test.txt /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/0.003-positive/low_act_5000_test_pred_unbiased_'+str(i)+'.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.003/slurm-lognormal10-train/outputs/Dex-200-lognormal10-0.003-' +str(i)
    #                     +' /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/Dex-200-biased/low_act_5000_test.txt /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/0.003-positive/low_act_5000_test_pred_lognormal10_'+str(i)+'.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/A549/full-set/BlueSTARR/A549.config /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/0.003-positive '+
    #                     '/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.003/Dex-200-lognormal10-0.003-'+str(i)+' train-lognormal10-'+str(i))
    # slurm.addCommand('python /datacommons/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/A549/full-set/BlueSTARR/A549.config /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/0.003-positive '+
    #                     '/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.01/Dex-200-unbiased-0.003-'+str(i)+' train-unbiased')

    # slurm.addCommand('python /datacommons/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/A549/full-set/BlueSTARR/A549.config /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/0.01-positive '+
    #                     '/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.01/Dex-200-lognormal10-0.01-'+str(i)+' train-lognormal10-'+str(i))
    # slurm.addCommand('python /datacommons/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/A549/full-set/BlueSTARR/A549.config /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/0.01-positive '+
    #                     '/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.01/Dex-200-unbiased-0.01-'+str(i)+' train-unbiased')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.01/slurm-unbiased-train/outputs/Dex-200-unbiased-0.01-' +str(i)
    #                     +' /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/Dex-200-biased/low_act_5000_test.txt /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/0.01-positive/low_act_5000_test_pred_unbiased_'+str(i)+'.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.01/slurm-lognormal10-train/outputs/Dex-200-lognormal10-0.01-' +str(i)
    #                     +' /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/Dex-200-biased/low_act_5000_test.txt /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/0.01-positive/low_act_5000_test_pred_lognormal10_'+str(i)+'.txt')

    # slurm.addCommand('python /datacommons/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/A549/full-set/BlueSTARR/A549.config /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/0.001-positive '+
    #                         '/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.001/Dex-200-lognormal10-0.001-'+str(i)+' train-lognormal10-'+str(i))
    # slurm.addCommand('python /datacommons/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/A549/full-set/BlueSTARR/A549.config /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/0.001-positive '+
    #                         '/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.001/Dex-200-unbiased-0.001-'+str(i)+' train-unbiased')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.001/slurm-lognormal10-train/outputs/Dex-200-lognormal10-0.001-'+str(i)
    #                         +' /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/Dex-200-biased/low_act_5000_test.txt /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/0.001-positive/low_act_5000_test_pred_lognormal10_'+str(i)+'.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.001/slurm-unbiased-train/outputs/Dex-200-lognormal10-0.001-'+str(i)
    #                         +' /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/Dex-200-biased/low_act_5000_test.txt /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/0.001-positive/low_act_5000_test_pred_unbiased_'+str(i)+'.txt')
 
    # slurm.addCommand('python /datacommons/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/A549/full-set/BlueSTARR/A549.config /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/exp-fit-1 '+
    #                         '/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-1-0.005/slurm-lognormal10-train/outputs/Dex-200-lognormal10-0.005-'+str(i)+' train-lognormal10-'+str(i))
    # slurm.addCommand('python /datacommons/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/A549/full-set/BlueSTARR/A549.config /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/exp-fit-2 '+
    #                         '/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-2-0.005/slurm-lognormal10-train/outputs/Dex-200-lognormal10-0.005-'+str(i)+' train-lognormal10-'+str(i))

    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-1-0.005/slurm-lognormal10-train/outputs/Dex-200-lognormal10-0.005-'+str(i)
    #                         +' /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_test.txt /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/exp-fit-1/low_act_5000_test_pred_lognormal_'+str(i)+'.txt')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-2-0.005/slurm-lognormal10-train/outputs/Dex-200-lognormal10-0.005-'+str(i)
    #                         +' /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_test.txt /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/exp-fit-2/low_act_5000_test_pred_lognormal_'+str(i)+'.txt')

    # slurm.addCommand('python /datacommons/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/A549/full-set/BlueSTARR/A549.config /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/exp-fit-1 '+
    #                         '/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-1-0.005/slurm-unbiased-train/outputs/Dex-200-unbiased-0.005-'+str(i)+' train-unbiased')
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-1-0.005/slurm-unbiased-train/outputs/Dex-200-unbiased-0.005-'+str(i)
    #                         +' /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_test.txt /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/exp-fit-1/low_act_5000_test_pred_unbiased_'+str(i)+'.txt')

    # slurm.addCommand('python /datacommons/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask.py /datacommons/igvf-pm/A549/full-set/BlueSTARR/A549.config /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/exp-fit-1 '+
    #                         '/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-1-0.005/slurm-bluestarr-train/outputs/Dex-200-bluestarr-0.005-'+str(i)+' train-bluestarr-'+str(i))
    # slurm.addCommand('python /datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/test-variants-ref.py /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-1-0.005/slurm-bluestarr-train/outputs/Dex-200-bluestarr-0.005-'+str(i)
    #                         +' /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_test.txt /datacommons/igvf-pm/A549/GR-AP1/simulated-seq/data/exp-fit-1/low_act_5000_test_pred_bluestarr_'+str(i)+'.txt')
 
    # slurm.addCommand('python /hpc/group/naderilab/eleanor/Efficient_PLM/aav.py --seed '+str(i+1)+' --path-model /hpc/group/naderilab/navid/efficient_plm_test_a100/saved_models/20250103_1300.sav')
    # slurm.addCommand('python /hpc/group/naderilab/eleanor/Efficient_PLM/ssp.py --seed '+str(i+1)+' --path-model /hpc/group/naderilab/navid/efficient_plm_test_a100/saved_models/20250103_1300.sav')
    # slurm.addCommand('python /hpc/group/naderilab/eleanor/Efficient_PLM/scl.py --seed '+str(i+1)+' --path-model /hpc/group/naderilab/navid/efficient_plm_test_a100/saved_models/20250103_1300.sav')
    # slurm.addCommand('python /hpc/group/naderilab/eleanor/Efficient_PLM/cmp.py --seed '+str(i+1)+' --path-model /hpc/group/naderilab/navid/efficient_plm_test_a100/saved_models/20250103_1300.sav')

    # slurm.addCommand('hostname && nvidia-smi && '+'\n'+
    #                 'source ~/.bashrc'+'\n'+
    #                 'module load BigWig'+'\n'+
    #                 'conda activate /hpc/home/yc583/envs/tf2'+'\n'+
    #                 'python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/mutator2-parent.py /hpc/group/igvf/A549/full-set/DMSO-200/300-bases/slurms/train-unbiased-normalized/outputs/DMSO-1 /hpc/group/igvf/K562/CRE-preds/chunks/CREs'+CRE_ls[i]+
    #                 '.txt 300 3000 /hpc/group/igvf/A549/CRE-preds/DMSO/preds/pred'+CRE_ls[i]+'.txt')

    # slurm.addCommand(
    #                      'python /work/igvf-pm/A549/extra_GCs/prepare_input_biased.py /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/ /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+labels[i]+'/split-biased/ '+labels[i]+' 700000 200000 200000'+'\n'+
    #                      'python /work/igvf-pm/K562/leave-one-out/BlueSTARR/leave-one-out/downsampling/theta.py /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+labels[i]+'/split-biased/all-train-counts.txt.gz /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+labels[i]+'/split-biased/all-train-thetas.txt '+'\n'+
    #                      'python /work/igvf-pm/K562/leave-one-out/BlueSTARR/leave-one-out/downsampling/downsample.py /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+labels[i]+'/split-biased/all-train-thetas.txt ' +
    #                      '/work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+labels[i]+'/split-biased/all-train.fasta /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+labels[i]+'/split-biased/all-train-counts.txt.gz 100 700000 /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+labels[i]+'/split-biased/ train'+'\n'+
    #                      'gzip -f /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+labels[i]+'/split-biased/*.fasta')

    # slurm.addCommand('python /work/igvf-pm/A549/extra_GCs/prepare_input_unbiased.py /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/ /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+labels[i]+'/split-unbiased/ '+labels[i]+' 700000 200000 200000'+'\n'+
    #                  'gzip -f /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+labels[i]+'/split-unbiased/*.fasta')

    # slurm.addCommand('python /work/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /work/igvf-pm/A549/full-set/BlueSTARR/A549-10-layers.config /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+labels[i]+'/split-biased /work/igvf-pm/A549/extra_GCs/600bp/slurms/train-biased/outputs/'+labels[i]+'-biased')
    # slurm.addCommand('python /work/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /work/igvf-pm/A549/full-set/BlueSTARR/A549-10-layers.config /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+labels[i]+'/split-unbiased /work/igvf-pm/A549/extra_GCs/600bp/slurms/train-unbiased/outputs/'+labels[i]+'-unbiased')

    # slurm.addCommand('python /work/igvf-pm/A549/extra_GCs/process_combined.py /work/igvf-pm/alex_b/starrseq_A549_extra_GCs/ /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/ '+labels[i]+'\n'+
    #                 'gzip -f /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+labels[i]+'/*.fasta')

    # slurm.addCommand('python /work/igvf-pm/A549/extra_GCs/process_combined.py /work/igvf-pm/alex_b/starrseq_A549_extra_GCs/ /work/igvf-pm/A549/extra_GCs/600bp/data/ '+labels[i]+'\n'+
    #                 'gzip -f /work/igvf-pm/A549/extra_GCs/600bp/data/'+labels[i]+'/*.fasta')

    # slurm.addCommand('python /work/igvf-pm/A549/extra_GCs/prepare_input_unbiased.py /work/igvf-pm/A549/extra_GCs/600bp/data/ /work/igvf-pm/A549/extra_GCs/600bp/data/'+labels[i]+'/split-unbiased/ '+labels[i]+' 700000 200000 200000'+'\n'+
    #                  'gzip -f /work/igvf-pm/A549/extra_GCs/600bp/data/'+labels[i]+'/split-unbiased/*.fasta')

    # slurm.addCommand('python /hpc/group/igvf/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /hpc/group/igvf/A549/full-set/BlueSTARR/A549.config /hpc/group/igvf/A549/full-set/Dex-200/300-bases/data-normalized /hpc/group/igvf/A549/full-set/Dex-200/300-bases/slurms/train-unbiased-normalized/Dex-'+str(i+1))
    # slurm.addCommand('python /hpc/group/igvf/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /hpc/group/igvf/A549/full-set/BlueSTARR/A549.config /hpc/group/igvf/A549/full-set/DMSO-200/300-bases/data-normalized /hpc/group/igvf/A549/full-set/DMSO-200/300-bases/slurms/train-unbiased-normalized/DMSO-'+str(i+1))
    # slurm.addCommand('python /hpc/group/igvf/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /hpc/group/igvf/K562/full-set/300bp/K562.config /hpc/group/igvf/K562/full-set/300bp/data-normalized /hpc/group/igvf/K562/full-set/300bp/slurms/train-unbiased-normalized/outputs/K562-'+str(i+1))

    # slurm.addCommand('hostname && nvidia-smi && '+'\n'+
    #                 'source ~/.bashrc'+'\n'+
    #                 'module load BigWig'+'\n'+
    #                 'source activate /hpc/home/yc583/envs/tf2'+'\n'+
    #                 'python /hpc/group/igvf/A549/full-set/BlueSTARR/mutator2-parent.py /hpc/group/igvf/K562/full-set/300bp/slurms/train-unbiased-normalized/outputs/K562-7 /hpc/group/igvf/A549/extra_GCs/IGVF_var_preds/chunks/VARs'+VAR_ls[i]+
    #                 '.txt 300 3000 /hpc/group/igvf/A549/extra_GCs/IGVF_var_preds/preds/K562/pred'+VAR_ls[i]+'.txt')

    # slurm.addCommand('hostname && nvidia-smi && '+'\n'+
    #                 'source ~/.bashrc'+'\n'+
    #                 'module load BigWig'+'\n'+
    #                 'source activate /hpc/home/yc583/envs/tf2'+'\n'+
    #                 'python /hpc/group/igvf/A549/full-set/BlueSTARR/mutator2-parent.py /hpc/group/igvf/A549/full-set/DMSO-200/300-bases/slurms/train-unbiased-normalized/DMSO-4 /hpc/group/igvf/A549/extra_GCs/IGVF_var_preds/chunks/VARs'+VAR_ls[i]+
    #                 '.txt 300 3000 /hpc/group/igvf/A549/extra_GCs/IGVF_var_preds/preds/DMSO/pred'+VAR_ls[i]+'.txt')

    # slurm.addCommand('hostname && nvidia-smi && '+'\n'+
    #                 'source ~/.bashrc'+'\n'+
    #                 'module load BigWig'+'\n'+
    #                 'source activate /hpc/home/yc583/envs/tf2'+'\n'+
    #                 'python /hpc/group/igvf/A549/full-set/BlueSTARR/mutator2-parent.py /hpc/group/igvf/A549/full-set/Dex-200/300-bases/slurms/train-unbiased-normalized/Dex-4 /hpc/group/igvf/A549/extra_GCs/IGVF_var_preds/chunks/VARs'+VAR_ls[i]+
    #                 '.txt 300 3000 /hpc/group/igvf/A549/extra_GCs/IGVF_var_preds/preds/Dex/pred'+VAR_ls[i]+'.txt')

    # slurm.addCommand('python /hpc/group/igvf/A549/full-set/BlueSTARR/BlueSTARR-multitask-sim.py /hpc/group/igvf/A549/full-set/BlueSTARR/A549.config '+
    #                 '/hpc/group/igvf/A549/GR-AP1/simulated-seq/data/mound /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/mound/train-0.005/mound-0.005-'+str(i)+' train-lognormal10')

    # slurm.addCommand('python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/test-variants-ref.py /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/mound/train-0.005/mound-0.005-' +str(i)
    #                     +' /hpc/group/igvf/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_installed.txt /hpc/group/igvf/A549/GR-AP1/simulated-seq/data/mound/low_act_5000_installed_pred_'+str(i)+'.txt')

    # slurm.addCommand('python /hpc/group/igvf/A549/full-set/BlueSTARR/BlueSTARR-multitask-sim.py /hpc/group/igvf/A549/full-set/BlueSTARR/A549.config '+
    #                 '/hpc/group/igvf/A549/GR-AP1/simulated-seq/data/bowl /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/train-0.005/bowl-0.005-'+str(i)+' train-lognormal10')

    # slurm.addCommand('python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/test-variants-ref.py /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/train-0.005/bowl-0.005-' +str(i)
    #                     +' /hpc/group/igvf/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_installed.txt /hpc/group/igvf/A549/GR-AP1/simulated-seq/data/bowl/low_act_5000_installed_pred_'+str(i)+'.txt')

    # slurm.addCommand('python /hpc/group/igvf/A549/full-set/BlueSTARR/BlueSTARR-multitask-sim.py /hpc/group/igvf/A549/full-set/BlueSTARR/A549.config '+
    #                 '/hpc/group/igvf/A549/GR-AP1/simulated-seq/data/cliff /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/train-0.005/cliff-0.005-'+str(i)+' train-lognormal10')

    # slurm.addCommand('python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/test-variants-ref.py /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/train-0.005/cliff-0.005-' +str(i)
    #                     +' /hpc/group/igvf/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_installed.txt /hpc/group/igvf/A549/GR-AP1/simulated-seq/data/cliff/low_act_5000_installed_pred_'+str(i)+'.txt')


    # slurm.addCommand('python /hpc/group/igvf/A549/full-set/BlueSTARR/BlueSTARR-multitask-sim.py /hpc/group/igvf/A549/full-set/BlueSTARR/A549.config '+
    #                 '/hpc/group/igvf/A549/GR-AP1/simulated-seq/data/mound /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/mound/no_enrichment_0.5/mound-0.5-'+str(i)+' train-0.5')
    # slurm.addCommand('python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/test-variants-ref.py /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/mound/no_enrichment_0.5/train/mound-0.5-' +str(i)
    #                     +' /hpc/group/igvf/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_installed.txt /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/mound/no_enrichment_0.5/pred/low_act_5000_installed_pred_'+str(i)+'.txt')

    # slurm.addCommand('python /hpc/group/igvf/A549/full-set/BlueSTARR/BlueSTARR-multitask-sim.py /hpc/group/igvf/A549/full-set/BlueSTARR/A549.config '+
    #                 '/hpc/group/igvf/A549/GR-AP1/simulated-seq/data/mound /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/mound/no_enrichment_5/mound-5-'+str(i)+' train-5')
    # slurm.addCommand('python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/test-variants-ref.py /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/mound/no_enrichment_5/train/mound-5-' +str(i)
    #                     +' /hpc/group/igvf/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_installed.txt /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/mound/no_enrichment_5/pred/low_act_5000_installed_pred_'+str(i)+'.txt')

    # slurm.addCommand('python /hpc/group/igvf/A549/full-set/BlueSTARR/BlueSTARR-multitask-sim.py /hpc/group/igvf/A549/full-set/BlueSTARR/A549.config '+
    #                 '/hpc/group/igvf/A549/GR-AP1/simulated-seq/data/bowl /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_0.5/train/bowl-0.5-'+str(i)+' train-0.5')
    # slurm.addCommand('python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/test-variants-ref.py /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_0.5/train/bowl-0.5-' +str(i)
    #                     +' /hpc/group/igvf/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_installed.txt /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_0.5/pred/low_act_5000_installed_pred_'+str(i)+'.txt')

    # slurm.addCommand('python /hpc/group/igvf/A549/full-set/BlueSTARR/BlueSTARR-multitask-sim.py /hpc/group/igvf/A549/full-set/BlueSTARR/A549.config '+
    #                 '/hpc/group/igvf/A549/GR-AP1/simulated-seq/data/bowl /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_3/train/bowl-3.0-'+str(i)+' train-3.0')
    # slurm.addCommand('python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/test-variants-ref.py /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_3/train/bowl-3.0-' +str(i)
    #                     +' /hpc/group/igvf/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_installed.txt /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_3/pred/low_act_5000_installed_pred_'+str(i)+'.txt')

    # slurm.addCommand('python /hpc/group/igvf/A549/full-set/BlueSTARR/BlueSTARR-multitask-sim.py /hpc/group/igvf/A549/full-set/BlueSTARR/A549.config '+
    #                 '/hpc/group/igvf/A549/GR-AP1/simulated-seq/data/bowl /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_10/train/bowl-10.0-'+str(i)+' train-10.0')
    # slurm.addCommand('python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/test-variants-ref.py /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_10/train/bowl-10.0-' +str(i)
    #                     +' /hpc/group/igvf/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_installed.txt /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_10/pred/low_act_5000_installed_pred_'+str(i)+'.txt')

    # slurm.addCommand('python /hpc/group/igvf/A549/full-set/BlueSTARR/BlueSTARR-multitask-sim.py /hpc/group/igvf/A549/full-set/BlueSTARR/A549.config '+
    #                 '/hpc/group/igvf/A549/GR-AP1/simulated-seq/data/cliff /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/no_enrichment_0.5/train/cliff-0.5-'+str(i)+' train-0.5')
    # slurm.addCommand('python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/test-variants-ref.py /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/no_enrichment_0.5/train/cliff-0.5-' +str(i)
    #                     +' /hpc/group/igvf/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_installed.txt /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/no_enrichment_0.5/pred/low_act_5000_installed_pred_'+str(i)+'.txt')

    # slurm.addCommand('python /hpc/group/igvf/A549/full-set/BlueSTARR/BlueSTARR-multitask-sim.py /hpc/group/igvf/A549/full-set/BlueSTARR/A549.config '+
    #                 '/hpc/group/igvf/A549/GR-AP1/simulated-seq/data/cliff /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/no_enrichment_5/train/cliff-5.0-'+str(i)+' train-5.0')
    # slurm.addCommand('python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/test-variants-ref.py /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/no_enrichment_5/train/cliff-5.0-' +str(i)
    #                     +' /hpc/group/igvf/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_installed.txt /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/no_enrichment_5/pred/low_act_5000_installed_pred_'+str(i)+'.txt')

    # slurm.addCommand('python /hpc/group/igvf/A549/full-set/BlueSTARR/BlueSTARR-multitask-sim.py /hpc/group/igvf/A549/full-set/BlueSTARR/A549.config '+
    #                 '/hpc/group/igvf/A549/GR-AP1/simulated-seq/data/cliff /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/enrichment_lognormal10_1.8/train/cliff-1.8-'+str(i)+' train-lognormal10')
    slurm.addCommand('python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/test-variants-ref.py /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/enrichment_lognormal10_1.8/train/cliff-1.8-' +str(i)
                        +' /hpc/group/igvf/A549/GR-AP1/simulated-seq/data/Dex-200/low_act_5000_installed.txt /hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/enrichment_lognormal10_1.8/pred/low_act_5000_installed_pred_'+str(i)+'.txt')

slurm.nice() # turns on "nice" (sets it to 100 by default)
slurm.mem(20000)
# slurm.mem(50000)
# slurm.mem(102400)
slurm.threads(1)
slurm.setQueue("gpu-common,scavenger-gpu,biostat-gpu,majoroslab-gpu,igvf-gpu")
# slurm.setQueue("majoroslab-gpu,igvf-gpu")
# slurm.writeArrayScript('/datacommons/igvf-pm/K562/leave-one-out/slurm', 'leave-one-out',16,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/leave-one-out/slurm', 'leave-one-out',16,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/leave-one-out/Dex-200/slurm-1-1', 'leave-one-out',23,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/slurm-1-1', 'leave-one-out',23,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/slurm', 'DMSO-mse',24,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/leave-one-out/Dex-200/slurm', 'Dex-mse',24,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/K562/leave-one-out/cross-validation/slurm-custom', 'cv-custom',24,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/K562/leave-one-out/cross-validation/slurm-normalized-custom', 'cv-normalized',24,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/K562/leave-one-out/cross-validation/slurm-normalized-mse', 'cv-normalized',24,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/K562/leave-one-out/cross-validation/slurm-mse', 'cv-mse',24,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/slurm-normalized-mse', 'DMSO-normalized',23,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/leave-one-out/Dex-200/slurm-normalized-mse', 'Dex-normalized',23,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/K562/leave-one-out/slurm-normalized-custom', 'k562-normalized',24,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/K562/leave-one-out/slurm-normalized-mse', 'k562-normalized',24,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/ref-score/DMSO-200/slurm','ref-scrore',24,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/ref-score/Dex-200/slurm','ref-scrore',24,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/GR-AP1',"fc",4,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/GR-AP1/slurm',"fc",4,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/GR-AP1/slurm-maxpooling',"fc",4,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/GR-AP1/slurm-attention',"fc",4,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/GR-AP1/slurm-single-based',"fc",4,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/K562/leave-one-out/BlueSTARR/GR-AP1/slurm-attention-pos',"fc",4,"")
# slurm.writeArrayScript('/work/igvf-pm/K562/CRE-preds/mutator-slurm',"MUTATE",300,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/600-bases/slurm-normalized-mse','A549',4,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/leave-one-out/Dex-200/600-bases/slurm-normalized-mse','A549',4,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/ref-score/DMSO-200/600-bases/slurm','ref-scrore',24,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/ref-score/Dex-200/600-bases/slurm','ref-scrore',24,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/fc-full/Dex-DMSO/600-bases/slurm','fc',4,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/fc-full/Dex-DMSO/600-bases/tf+pos/slurm','fc',4,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/enhancer-seq/fc-full/Dex-DMSO/600-bases/default-2/slurm','fc',4,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-biased','pred',5,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-unbiased','pred',5,"")

# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.003/slurm-lognormal10-pred','pred',5,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.003/slurm-unbiased-pred','pred',5,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.003/slurm-lognormal10-train','biased-train',5,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.003/slurm-unbiased-train','unbiased-train',5,"")

# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.01/slurm-lognormal10-train','biased-train',5,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.01/slurm-unbiased-train','unbiased-train',5,"")
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.01/slurm-unbiased-pred','unbiased-pred',5,'')
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.01/slurm-lognormal10-pred','biased-pred',5,'')

# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.001/slurm-lognormal10-train','biased-train',5,'')
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.001/slurm-unbiased-train','unbiased-pred',5,'')
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.001/slurm-lognormal10-pred','biased-pred',5,'')
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-0.001/slurm-unbiased-pred','unbiased-pred',5,'')

# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-1-0.005/slurm-lognormal10-train','fit-1-train',5,'')
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-2-0.005/slurm-lognormal10-train','fit-2-train',5,'')
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-1-0.005/slurm-lognormal10-pred','fit-1-pred',5,'')
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-2-0.005/slurm-lognormal10-pred','fit-2-pred',5,'')
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-1-0.005/slurm-unbiased-train','fit-1-train',5,'')
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-1-0.005/slurm-unbiased-pred','fit-1-pred',5,'')
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-1-0.005/slurm-bluestarr-train','fit-1-train',5,'')
# slurm.writeArrayScript('/datacommons/igvf-pm/A549/GR-AP1/simulated-seq/slurm/slurm-exp-fit-1-0.005/slurm-bluestarr-pred','fit-1-pred',5,'')

# slurm.writeArrayScript('/hpc/group/naderilab/eleanor/Efficient_PLM/slurms/aav/active','aav',10,'source activate /hpc/home/yc583/envs/pt2')
# slurm.writeArrayScript('/hpc/group/naderilab/eleanor/Efficient_PLM/slurms/aav/random','aav',10,'source activate /hpc/home/yc583/envs/pt2')
# slurm.writeArrayScript('/hpc/group/naderilab/eleanor/Efficient_PLM/slurms/ssp/active','ssp',10,'source activate /hpc/home/yc583/envs/pt2')
# slurm.writeArrayScript('/hpc/group/naderilab/eleanor/Efficient_PLM/slurms/ssp/random','ssp',10,'source activate /hpc/home/yc583/envs/pt2')
# slurm.writeArrayScript('/hpc/group/naderilab/eleanor/Efficient_PLM/slurms/scl/active','scl',10,'source activate /hpc/home/yc583/envs/pt2')
# slurm.writeArrayScript('/hpc/group/naderilab/eleanor/Efficient_PLM/slurms/scl/random','scl',10,'source activate /hpc/home/yc583/envs/pt2')
# slurm.writeArrayScript('/hpc/group/naderilab/eleanor/Efficient_PLM/slurms/cmp/active','cmp',10,'source activate /hpc/home/yc583/envs/pt2')
# slurm.writeArrayScript('/hpc/group/naderilab/eleanor/Efficient_PLM/slurms/cmp/random','cmp',10,'source activate /hpc/home/yc583/envs/pt2')

# slurm.writeArrayScript('/work/igvf-pm/A549/extra_GCs/600bp/slurms/biased-downsampling','biased-downsampling',10,'')
# slurm.writeArrayScript('/work/igvf-pm/A549/extra_GCs/600bp/slurms/unbiased-downsampling','unbiased-downsampling',10,'')
# slurm.writeArrayScript('/work/igvf-pm/A549/extra_GCs/600bp/slurms/train-biased','biased-train',10,'')
# slurm.writeArrayScript('/work/igvf-pm/A549/extra_GCs/600bp/slurms/train-unbiased','unbiased-train',10,'')
# slurm.writeArrayScript('/work/igvf-pm/A549/extra_GCs/600bp/slurms/normalized','normalize',10,'')

# slurm.writeArrayScript('/work/igvf-pm/A549/extra_GCs/600bp/slurms/process','process-combined',10,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/full-set/Dex-200/300-bases/slurms/train-unbiased-normalized','Dex',10,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/full-set/DMSO-200/300-bases/slurms/train-unbiased-normalized','DMSO',10,'')
# slurm.writeArrayScript('/hpc/group/igvf/K562/full-set/300bp/slurms/train-unbiased-normalized','K562',10,'')

# slurm.writeArrayScript('/hpc/group/igvf/A549/extra_GCs/IGVF_var_preds/mutator-slurms/K562','MUTATE',300,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/extra_GCs/IGVF_var_preds/mutator-slurms/DMSO','MUTATE',300,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/extra_GCs/IGVF_var_preds/mutator-slurms/Dex','MUTATE',300,'')

# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/mound/train-0.005','mound',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/mound/pred-0.005','mound',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/train-0.005','bowl',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/pred-0.005','bowl',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/train-0.005','cliff',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/pred-0.005','cliff',5,'')

# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/mound/no_enrichment_0.5/train','mound-0.5',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/mound/no_enrichment_0.5/pred','mound-0.5',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/mound/no_enrichment_5/train','mound-5',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/mound/no_enrichment_5/pred','mound-5',5,'')

# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_0.5/train','bowl-0.5',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_0.5/pred','bowl-0.5',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_3/train','bowl-3',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_3/pred','bowl-3',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_10/train','bowl-10',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/bowl/no_enrichment_10/pred','bowl-10',5,'')

# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/no_enrichment_0.5/train','cliff-0.5',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/no_enrichment_0.5/pred','cliff-0.5',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/no_enrichment_5/train','cliff-5',5,'')
# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/no_enrichment_5/pred','cliff-5',5,'')

# slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/enrichment_lognormal10_1.8/train','cliff-1.8',5,'')
slurm.writeArrayScript('/hpc/group/igvf/A549/GR-AP1/simulated-seq/slurm/cliff/enrichment_lognormal10_1.8/pred','cliff-1.8',5,'')


# slurm.writeArrayScript('/hpc/group/igvf/A549/CRE-preds/DMSO/mutator_slurm',"MUTATE",300,"")


# for label in labels:
#     for i in range(0,len(VAR_ls)):
#         slurm.addCommand('hostname && nvidia-smi && '+'\n'+
#                         'source ~/.bashrc'+'\n'+
#                         'module load BigWig'+'\n'+
#                         'source activate /hpc/home/yc583/envs/tf2'+'\n'+
#                         'python /work/igvf-pm/A549/full-set/BlueSTARR/mutator2-parent.py /work/igvf-pm/A549/extra_GCs/'+label+'/train/'+ label+'-normalized /work/igvf-pm/A549/extra_GCs/IGVF_var_preds/chunks/VARs'+VAR_ls[i]+
#                         '.txt 300 3000 /work/igvf-pm/A549/extra_GCs/IGVF_var_preds/preds/'+label+'/pred'+VAR_ls[i]+'.txt')
#     slurm.writeArrayScript('/work/igvf-pm/A549/extra_GCs/IGVF_var_preds/mutator-slurms/'+label,label,200,"")
#     slurm.clearCommands()

# commands=''
# for label in labels:
#     commands+='sbatch /work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label+'-biased.sh'+'\n'+\
#                     'sbatch /work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label+'-normalized.sh'+'\n'+\
#                     'sbatch /work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label+'.sh'+'\n'
# slurm.writeScript('/work/igvf-pm/A549/extra_GCs/all.sh',
#                     '/work/igvf-pm/A549/extra_GCs','',
#                     commands)

    # slurm.writeScript('/work/igvf-pm/A549/extra_GCs/'+label+'/data-biased/biased-downsampling.sh',
    #                     '/work/igvf-pm/A549/extra_GCs/'+label+'/data-biased/biased-downsampling',label+'-biased-downsampling',
    #                     'python /work/igvf-pm/A549/extra_GCs/downsample_unbiased.py /work/igvf-pm/A549/extra_GCs/ /work/igvf-pm/A549/extra_GCs/ '+label+' 1600000 500000 500000'+'\n'+
    #                     'python /work/igvf-pm/K562/leave-one-out/BlueSTARR/leave-one-out/downsampling/theta.py /work/igvf-pm/A549/extra_GCs/'+label+'/data-biased/all-train-counts.txt /work/igvf-pm/A549/extra_GCs/'+label+'/data-biased/all-train-thetas.txt '+'\n'+
    #                     'python /work/igvf-pm/K562/leave-one-out/BlueSTARR/leave-one-out/downsampling/downsample.py /work/igvf-pm/A549/extra_GCs/'+label+'/data-biased/all-train-thetas.txt ' +
    #                     '/work/igvf-pm/A549/extra_GCs/'+label+'/data-biased/all-train.fasta /work/igvf-pm/A549/extra_GCs/'+label+'/data-biased/all-train-counts.txt 100 1600000 /work/igvf-pm/A549/extra_GCs/'+label+'/data-biased/ train'+'\n'+
    #                     'gzip -f /work/igvf-pm/A549/extra_GCs/'+label+'/data-biased/*.txt /work/igvf-pm/A549/extra_GCs/'+label+'/data-biased/*.fasta') 

    # slurm.writeScript('/work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label+'-biased.sh',
    #                     '/work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label+'-biased',label+'-train',
    #                     'python /work/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /work/igvf-pm/A549/full-set/BlueSTARR/A549.config '+
    #                     '/work/igvf-pm/A549/extra_GCs/'+label+'/data-biased /work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label+'-biased')

    # slurm.writeScript('/work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label+'-normalized.sh',
    #                     '/work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label+'-normalized',label+'-train',
    #                     'python /work/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /work/igvf-pm/A549/full-set/BlueSTARR/A549.config '+
    #                     '/work/igvf-pm/A549/extra_GCs/'+label+'/data-normalized /work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label+'-normalized')

    # slurm.writeScript('/work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label+'.sh',
    #                     '/work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label,label+'-train',
    #                     'python /work/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /work/igvf-pm/A549/full-set/BlueSTARR/A549.config '+
    #                     '/work/igvf-pm/A549/extra_GCs/'+label+'/data /work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label)

    # slurm.writeScript('/work/igvf-pm/A549/extra_GCs/'+label+'/train/pred.sh',
    #                     '/work/igvf-pm/A549/extra_GCs/'+label+'/train/pred',label+'-pred',
    #                     'python /work/igvf-pm/A549/full-set/BlueSTARR/predictions.py /work/igvf-pm/A549/full-set/BlueSTARR/A549.config /work/igvf-pm/A549/extra_GCs/'+label+'/data /work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label+'\n'+
    #                     'python /work/igvf-pm/A549/full-set/BlueSTARR/predictions.py /work/igvf-pm/A549/full-set/BlueSTARR/A549.config /work/igvf-pm/A549/extra_GCs/'+label+'/data-normalized /work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label+'-normalized\n'+
    #                     'python /work/igvf-pm/A549/full-set/BlueSTARR/predictions.py /work/igvf-pm/A549/full-set/BlueSTARR/A549.config /work/igvf-pm/A549/extra_GCs/'+label+'/data-biased /work/igvf-pm/A549/extra_GCs/'+label+'/train/'+label+'-biased')

                        
# for label in labels:
    # for i in range(1, 10):
    #     slurm.addCommand('python /work/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /work/igvf-pm/A549/full-set/BlueSTARR/A549-10-layers.config /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+label+
    #                     '/split-unbiased /work/igvf-pm/A549/extra_GCs/600bp/slurms/train-unbiased-normalized/'+label+'/outputs/'+label+'-'+str(i+1))
    # slurm.writeArrayScript('/work/igvf-pm/A549/extra_GCs/600bp/slurms/train-unbiased-normalized/'+label, label, 10,'')
    # slurm.clearCommands()

    # for i in range(1, 10):
    #     slurm.addCommand('python /work/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /work/igvf-pm/A549/full-set/BlueSTARR/A549-10-layers.config /work/igvf-pm/A549/extra_GCs/600bp/data-normalized/'+label+
    #                     '/split-biased /work/igvf-pm/A549/extra_GCs/600bp/slurms/train-biased-normalized/'+label+'/outputs/'+label+'-'+str(i+1))
    # slurm.writeArrayScript('/work/igvf-pm/A549/extra_GCs/600bp/slurms/train-biased-normalized/'+label, label, 10,'')
    # slurm.clearCommands()

    # for i in range(0, 10):
    #     slurm.addCommand('python /work/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /work/igvf-pm/A549/full-set/BlueSTARR/A549-10-layers.config /work/igvf-pm/A549/extra_GCs/600bp/data/'+label+
    #                     '/split-unbiased /work/igvf-pm/A549/extra_GCs/600bp/slurms/train-unbiased/'+label+'/outputs/'+label+'-'+str(i+1))
    # slurm.writeArrayScript('/work/igvf-pm/A549/extra_GCs/600bp/slurms/train-unbiased/'+label, label, 10,'')
    # slurm.clearCommands()

# for i in range(0, 10):
#     slurm.addCommand('python /work/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /work/igvf-pm/K562/full-set/600bp/K562-10-layers.config /work/igvf-pm/K562/full-set/600bp/data-normalized/split-unbiased'+
#                     ' /work/igvf-pm/K562/full-set/600bp/slurms/train-unbiased-normalized/outputs/K562-'+str(i+1))
# slurm.writeArrayScript('/work/igvf-pm/K562/full-set/600bp/slurms/train-unbiased-normalized', 'K562', 10,'')


# for i in range(0, 10):
#     slurm.addCommand('python /work/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /work/igvf-pm/A549/full-set/BlueSTARR/A549-10-layers.config /work/igvf-pm/A549/full-set/Dex-200/600-bases/data-normalized/split-unbiased'+
#                     ' /work/igvf-pm/A549/full-set/Dex-200/600-bases/slurms/train-unbiased-normalized/outputs/Dex-'+str(i+1))
# slurm.writeArrayScript('/work/igvf-pm/A549/full-set/Dex-200/600-bases/slurms/train-unbiased-normalized', 'Dex', 10,'')
# slurm.clearCommands()

# for i in range(0, 10):
#     slurm.addCommand('python /work/igvf-pm/A549/full-set/BlueSTARR/BlueSTARR-multitask-pred.py /work/igvf-pm/A549/full-set/BlueSTARR/A549-10-layers.config /work/igvf-pm/A549/full-set/DMSO-200/600-bases/data-normalized/split-unbiased'+
#                     ' /work/igvf-pm/A549/full-set/DMSO-200/600-bases/slurms/train-unbiased-normalized/outputs/DMSO-'+str(i+1))
# slurm.writeArrayScript('/work/igvf-pm/A549/full-set/DMSO-200/600-bases/slurms/train-unbiased-normalized', 'DMSO', 10,'')
# slurm.clearCommands()