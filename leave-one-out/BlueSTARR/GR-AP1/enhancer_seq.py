import pandas as pd
import numpy as np
import sys
import os

## generate enhancer sequence by chromosome and save as the format of test-variant.py input file

forward_ap1 = 'TGAGTCAT'
backward_ap1 = 'ATGACTCA'
forward_gr  = 'GAACATTATGTTC'
backward_gr = 'GAACATAATGTTC'
# step = 1
# distance = np.arange(8, 278, step)





def gen_seq(ap1,gr,df,start,seqlen):
    ls_loc = []
    ls_score = []
    ls_distance = []
    ls_seq = []
    ls_ref = []
    ls_allele = []
    if seqlen == 300: distance = np.arange(23, 244, 20)
    elif seqlen == 600: distance = np.arange(23, 564, 20)
    else: raise Exception('length error')

    for i in range(len(df)):
        seq = df.loc[i,'sequence']

        for j in range(len(distance)):
            ls_loc.append(df.loc[i,'location'])
            ls_score.append(df.loc[i,'refScore'])
            ls_distance.append(distance[j])
            # fix ap1, move gr
            seq_tmp = seq[:start-1]+ap1+seq[start+len(ap1)-1:start+distance[j]-1]+gr+seq[start+distance[j]-1+len(gr):]
            if len(seq_tmp)!=seqlen: raise Exception('length error')
            ls_seq.append(seq_tmp)
            # fix gr, move ap1
            # ls_seq.append(seq[:start-1]+gr+seq[start+len(gr)-1:start+distance[j]-1]+ap1+seq[start+distance[j]-1+len(ap1):])
            ls_ref.append('ref='+seq_tmp[150])
            ls_allele.append(seq_tmp[150])


    return pd.DataFrame({'location':ls_loc,
                         'ref':ls_ref,
                         'allele':ls_allele,
                         'sequence':ls_seq,
                        #  'distance':ls_distance
                         })



def main(ref_seq_dir,output_dir,num_seq,start,seqlen):

    ref_seq_files = [f for f in os.listdir(ref_seq_dir) if f.endswith('.txt')]
    for ref_seq in ref_seq_files:
        chromosome = ref_seq.split('.')[0]

        df = pd.read_csv(ref_seq_dir+'/'+ref_seq, sep='\t', header=None)
        df.columns = ['location','refScore','sequence']
        df = df.sort_values(by = 'refScore')
        df = df.reset_index(drop = True)
        df = df.iloc[:num_seq,:]

        gen_seq(forward_ap1,forward_gr,df,start,seqlen).to_csv(output_dir+'/'+chromosome+'-f-ap1-f-gr.txt', sep = '\t', header = None, index = False)
        gen_seq(forward_ap1,backward_gr,df,start,seqlen).to_csv(output_dir+'/'+chromosome+'-f-ap1-b-gr.txt', sep = '\t', header = None, index = False)
        gen_seq(backward_ap1,forward_gr,df,start,seqlen).to_csv(output_dir+'/'+chromosome+'-b-ap1-f-gr.txt', sep = '\t', header = None, index = False)
        gen_seq(backward_ap1,backward_gr,df,start,seqlen).to_csv(output_dir+'/'+chromosome+'-b-ap1-b-gr.txt', sep = '\t', header = None, index = False)

if(len(sys.argv)!=6):
    exit(ProgramName.get()+" <ref_seq_score_dir> <output_dir> <num_seq> <start_pos_ap1> <seqlen>\n")
(ref_seq_dir, output_dir, num_seq, start,seqlen)=sys.argv[1:]
main(ref_seq_dir, output_dir, int(num_seq), int(start),int(seqlen))