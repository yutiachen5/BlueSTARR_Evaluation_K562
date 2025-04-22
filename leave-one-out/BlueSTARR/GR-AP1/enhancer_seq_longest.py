import pandas as pd
import numpy as np
import sys
import os

## generate enhancer sequence by chromosome and save as the format of test-variant.py input file

forward_ap1 = 'TGAGTCAT'
backward_ap1 = 'ATGACTCA'
forward_gr  = 'GAACATTATGTTC'
backward_gr = 'GAACATAATGTTC'




def gen_seq(ap1,gr,df,start):
    ls_loc = []
    ls_score = []
    ls_distance = []
    ls_seq = []
    ls_ref = []
    ls_allele = []

    for i in range(len(df)):
        seq = df.loc[i,'sequence']

        ls_loc.append(df.loc[i,'location'])
        ls_score.append(df.loc[i,'refScore'])
        ls_seq.append(ap1+seq[len(ap1):300-len(gr)]+gr)
        ls_ref.append('ref='+seq[150])
        ls_allele.append(seq[150])


    return pd.DataFrame({'location':ls_loc,
                         'ref':ls_ref,
                         'allele':ls_allele,
                         'sequence':ls_seq,
                         })



def main(ref_seq_dir,output_dir,num_seq,start):

    ref_seq_files = [f for f in os.listdir(ref_seq_dir) if f.endswith('.txt')]
    for ref_seq in ref_seq_files:
        chromosome = ref_seq.split('.')[0]

        df = pd.read_csv(ref_seq_dir+'/'+ref_seq, sep='\t', header=None)
        df.columns = ['location','refScore','sequence']
        df = df.sort_values(by = 'refScore')
        df = df.reset_index(drop = True)
        df = df.iloc[:num_seq,:]

        gen_seq(forward_ap1,forward_gr,df,start).to_csv(output_dir+'/'+chromosome+'-f-ap1-f-gr-longest-dis.txt', sep = '\t', header = None, index = False)
        gen_seq(forward_ap1,backward_gr,df,start).to_csv(output_dir+'/'+chromosome+'-f-ap1-b-gr-longest-dis.txt', sep = '\t', header = None, index = False)
        gen_seq(backward_ap1,forward_gr,df,start).to_csv(output_dir+'/'+chromosome+'-b-ap1-f-gr-longest-dis.txt', sep = '\t', header = None, index = False)
        gen_seq(backward_ap1,backward_gr,df,start).to_csv(output_dir+'/'+chromosome+'-b-ap1-b-gr-longest-dis.txt', sep = '\t', header = None, index = False)

if(len(sys.argv)!=5):
    exit(ProgramName.get()+" <ref_seq_score_dir> <output_dir> <num_seq> <start_pos_ap1>\n")
(ref_seq_dir, output_dir, num_seq, start)=sys.argv[1:]
main(ref_seq_dir, output_dir, int(num_seq), int(start))