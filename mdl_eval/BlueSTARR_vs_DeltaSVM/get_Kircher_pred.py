import sys
import ProgramName
from Pipe import Pipe

def main(model,Kircher_chunk,seqLen,outputFile):
    cmd = 'module load BigWig'
    Pipe.run(cmd)
    cmd = 'python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/mutator2-parent.py '+model+' '+Kircher_chunk+' '+seqLen+' 3000 '+outputFile
    Pipe.run(cmd)

if(len(sys.argv)!=5):
    exit(ProgramName.get()+" <model> <Kircher_chunk.txt> <seq-len> <out-file>\n")
(model,Kircher_chunk,seqLen,outputFile)=sys.argv[1:]

main(model,Kircher_chunk,seqLen,outputFile)

# python /hpc/group/igvf/K562/mdl_eval/BlueSTARR_vs_DeltaSVM/get_Kircher_pred.py /hpc/group/igvf/K562/full-set/300bp/slurms/train-unbiased-normalized/outputs/K562-7 /hpc/group/igvf/K562/mdl_eval/BlueSTARR_vs_DeltaSVM/Kircher_entire_regions/Kircher_region_chunk.txt 300 /hpc/group/igvf/K562/mdl_eval/BlueSTARR_vs_DeltaSVM/Kircher_entire_regions/Kircher_region_pred.txt