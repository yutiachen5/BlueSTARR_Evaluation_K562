# process K562 data

import pandas as pd
import sys
import os
import gzip
from FastaWriter import FastaWriter


input_rep1 = 123384250
input_rep2 = 130680200
input_rep3 = 134539576
output_rep1 = 116270841
output_rep2 = 217503220
output_rep3 = 219086330

def normalize(df_count):
    c = 10**6
    df_count['input_rep1'] = df_count['input_rep1']/input_rep1*c
    df_count['input_rep2'] = df_count['input_rep2']/input_rep2*c
    df_count['input_rep3'] = df_count['input_rep3']/input_rep3*c
    df_count['output_rep1'] = df_count['output_rep1']/output_rep1*c
    df_count['output_rep2'] = df_count['output_rep2']/output_rep2*c
    df_count['output_rep3'] = df_count['output_rep3']/output_rep3*c

    return df_count

def main(input_path, output_path, output_label):
    df_combined = pd.read_csv(input_path, sep = '\t', compression="gzip")

    os.makedirs(output_path, exist_ok=True)

    # process lines to fhave the format of >17698785 /coord=chr1:138900-139200
    # CCTGTAGACGCTGACAGGAGGCAGGAGCTGGGCCTGGACAGGTCAACTTGAGGAGATTTT

    ls_chr = df_combined['chrom']
    ls_start = df_combined['start']
    ls_end = df_combined['end']
    ls_seq = df_combined['sequence']

    fastaWriter=FastaWriter()
    # output_fasta = gzip.open(output_path+label+"-all.fasta.gz","wt") # slow
    output_fasta = open(output_path+output_label+".fasta","wt") 

    for i in range(len(df_combined)):
        defline = '>'+str(i)+' /coord='+str(ls_chr[i])+':'+str(ls_start[i])+'-'+str(ls_end[i])
        assert len(ls_seq[i]) == 600
        fastaWriter.addToFasta(defline,ls_seq[i],output_fasta)

    # process counts to have the format
    # DNA=3    RNA=3
    # 1   2   3   4   5   6  

    count_cols = ['input_rep1','input_rep2','input_rep3','output_rep1','output_rep2','output_rep3']
    df_count = df_combined[count_cols].astype(float)
    df_count = normalize(df_count)

    output_count = gzip.open(output_path+output_label+'-counts.txt.gz',"wt")
    header = "DNA=3\tRNA=3\n"
    print(header,end="",file=output_count)
    df_count.to_csv(output_count, sep='\t', index=False, header=None) 

if(len(sys.argv)!=4):
    exit(ProgramName.get()+" <input-path> <output-path> <output-label>\n")
(input_path,output_path,output_label)=sys.argv[1:]
main(input_path,output_path,output_label)

# python /work/igvf-pm/K562/leave-one-out/BlueSTARR/leave-one-out/process_combined.py /work/igvf-pm/K562/full-set/600bp/K562.combined.input_and_output.w600s50.gt_200.thres_dna_only.log2FC.sequenc.na_removed.txt.gz /work/igvf-pm/K562/full-set/600bp/thres_dna_only/data-normalized/ all
# python /work/igvf-pm/K562/leave-one-out/BlueSTARR/leave-one-out/process_combined.py /work/igvf-pm/K562/full-set/600bp/K562.combined.input_and_output.w600s50.gt_200.log2FC.sequenc.na_removed.txt.gz /work/igvf-pm/K562/full-set/600bp/thres_rna_dna/data-normalized/ all