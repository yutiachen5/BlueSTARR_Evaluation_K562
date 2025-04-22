# process the cCRE predictions to have fold-change on log2 scale and spdi

import sys
import pandas as pd
import re
import os
import math
from tqdm import tqdm

headers = ['cCRE_interval','actual_interval','pos','ref','alt','log_pred']


spdi = {'chr1':'NC_000001.11', 'chr2':'NC_000002.12', 'chr3':'NC_000003.12', 'chr4':'NC_000004.12', 'chr5':'NC_000005.10', 'chr6':'NC_000006.12',
        'chr7':'NC_000007.14', 'chr8':'NC_000008.11', 'chr9':'NC_000009.12', 'chr10':'NC_000010.11', 'chr11':'NC_000011.10', 'chr12':'NC_000012.12',
        'chr13':'NC_000013.11', 'chr14':'NC_000014.9', 'chr15':'NC_000015.10', 'chr16':'NC_000016.10', 'chr17':'NC_000017.11', 'chr18':'NC_000018.10',
        'chr19':'NC_000019.10', 'chr20':'NC_000020.11', 'chr21':'NC_000021.9', 'chr22':'NC_000022.11', 'chrX':'NC_000023.11', 'chrY':'NC_000024.10'}

def process(df):
    df['log2_pred'] = df['log_pred']*math.log2(math.e)  # convert prediction to log2 scale
    df = df.drop(columns=['log_pred'])
    df['ref'] = df['ref'].apply(lambda x: x.split('=')[-1])

    ref = df.loc[df['ref'] == df['alt'], ]
    ref = ref.drop(columns=['alt'])
    ref = ref.rename(columns={'log2_pred':'log2_ref_pred'})
    merged = pd.merge(df, ref, on=['cCRE_interval','actual_interval','pos','ref'], how='left')
    merged['effect'] = merged['log2_pred'] - merged['log2_ref_pred']
    merged = merged.loc[merged['ref'] != merged['alt'], ]
    merged['cre_chrom'] = merged['cCRE_interval'].apply(lambda x: x.split(':')[0])
    merged['cre_start'] = merged['cCRE_interval'].apply(lambda x: (x.split(':')[-1]).split('-')[0])
    merged['cre_end'] = merged['cCRE_interval'].apply(lambda x: (x.split(':')[-1]).split('-')[-1])
    merged['pos'] = merged['pos'].apply(lambda x: x.split('=')[-1])
    merged['SPDI'] = merged['cre_chrom'].map(spdi)+':'+merged['pos']+':'+merged['ref']+':'+merged['alt']
    merged = merged[['cre_chrom','cre_start','cre_end','effect','SPDI']]
    
    return merged

def main(pred_dir, out_dir):
    all_preds = os.listdir(pred_dir)
    for i in tqdm(range(1,1065)):
        df = pd.read_csv(pred_dir+'pred'+str(i)+'.txt', sep="\t", header = None)
        if df.shape[1] == 7: 
            df.columns = ['cCRE_interval','actual_interval','pos','ref','alt','log_pred','log2fc']
        elif df.shape[1] == 6: 
            df.columns = ['cCRE_interval','actual_interval','pos','ref','alt','log_pred']
        df = process(df)        
        df.to_csv(out_dir+'pred'+str(i)+'.txt', sep="\t", index = False)

main('/work/igvf-pm/K562/CRE-preds/preds/', '/work/igvf-pm/K562/CRE-preds/processed-preds/')