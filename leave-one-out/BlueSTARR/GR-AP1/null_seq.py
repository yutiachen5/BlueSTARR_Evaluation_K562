import pandas as pd
import numpy as np
import sys
import os

## generate 3 nulls

forward_ap1 = 'TGAGTCAT'
backward_ap1 = 'ATGACTCA'
forward_gr  = 'GAACATTATGTTC'
backward_gr = 'GAACATAATGTTC'
distance = np.arange(23, 244, 20)
step = 20


def gen_seq(ap1,gr,df,start):
    # 3 nulls
    ls_loc = []
    ls_score = []
    ls_distance = []
    ls_seq = []

    for i in range(len(df)):
        # ap1 only, fixed ap1 at position 10
        seq = df.loc[i,'sequence']
        seq = seq[:start-1]+ap1+seq[start+len(ap1)-1:]
        for j in range(len(distance)):
            ls_loc.append(df.loc[i,'location'])
            ls_score.append(df.loc[i,'refScore'])
            ls_distance.append(distance[j])
            ls_seq.append(seq)
    df_ap1 = pd.DataFrame({'location':ls_loc,
                            'refScore':ls_score,
                            'sequence':ls_seq,
                            'distance':ls_distance})

    ls_loc = []
    ls_score = []
    ls_distance = []
    ls_seq = []

    for i in range(len(df)):
        # gr only, move gr
        seq = df.loc[i,'sequence']
        for j in range(len(distance)):
            ls_loc.append(df.loc[i,'location'])
            ls_score.append(df.loc[i,'refScore'])
            ls_distance.append(distance[j])
            ls_seq.append(seq[:start+distance[j]]+gr+seq[start+distance[j]+len(gr):])
    df_gr = pd.DataFrame({'location':ls_loc,
                            'refScore':ls_score,
                            'sequence':ls_seq,
                            'distance':ls_distance})

    ls_loc = []
    ls_score = []
    ls_distance = []
    ls_seq = []

    for i in range(len(df)):
        # no ap1 and no gr
        seq = df.loc[i,'sequence']
        for j in range(len(distance)):
            ls_loc.append(df.loc[i,'location'])
            ls_score.append(df.loc[i,'refScore'])
            ls_distance.append(distance[j])
            ls_seq.append(seq)
    df_null = pd.DataFrame({'location':ls_loc,
                            'refScore':ls_score,
                            'sequence':ls_seq,
                            'distance':ls_distance})


    return df_ap1, df_gr, df_null



def main(ref_seq_dir,output_dir,num_seq,start):
    ref_seq_files = [f for f in os.listdir(ref_seq_dir) if f.endswith('.txt')]
    for ref_seq in ref_seq_files:
        chromosome = ref_seq.split('.')[0]

        df = pd.read_csv(ref_seq_dir+'/'+ref_seq, sep='\t', header=None)
        df.columns = ['location','refScore','sequence']
        df = df.sort_values(by = 'refScore').head(num_seq).reset_index(drop = True)

        df_ap1, df_gr, df_null = gen_seq(forward_ap1,forward_gr,df,start)
        df_ap1.to_csv(output_dir+'/'+chromosome+'-null-ap1.txt', sep = '\t', header = None, index = False)
        df_gr.to_csv(output_dir+'/'+chromosome+'-null-gr.txt', sep = '\t', header = None, index = False)
        df_null.to_csv(output_dir+'/'+chromosome+'-null.txt', sep = '\t', header = None, index = False)


if(len(sys.argv)!=5):
    exit(ProgramName.get()+" <ref_seq_dir> <output_dir> <num_seq> <start_pos_ap1>\n")
(ref_seq_dir, output_dir, num_seq,start)=sys.argv[1:]
main(ref_seq_dir, output_dir, int(num_seq),int(start))