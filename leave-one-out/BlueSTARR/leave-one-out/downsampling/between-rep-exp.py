import gzip
import pandas as pd
from scipy.stats import spearmanr
import sys


def corr(file, task):
    with gzip.open(file) if file.endswith(".gz") else open(file) as f:
        if task == 'K562':
            NUM_DNA = 3
            header = ['DNA1','DNA2','DNA3','RNA1','RNA2','RNA3']
            df = pd.read_csv(f, sep='\t', header=None, skiprows=1,names=header)
        
            df['DNA_sum'] = df['DNA1']+df['DNA2']+df['DNA3']
            df['rep1'] = (df['RNA1']+1)/(df['DNA_sum']+NUM_DNA)
            df['rep2'] = (df['RNA2']+1)/(df['DNA_sum']+NUM_DNA)
            df['rep3'] = (df['RNA3']+1)/(df['DNA_sum']+NUM_DNA)

            print('rep1 and rep2: ', spearmanr(df['rep1'], df['rep2']))
            print('rep1 and rep3: ', spearmanr(df['rep1'], df['rep3']))
            print('rep2 and rep3: ', spearmanr(df['rep2'], df['rep3']))
        elif task == 'A549':
            NUM_DNA = 5
            header = ['DNA1','DNA2','DNA3','DNA4','DNA5','RNA2','RNA3','RNA4','RNA5']
            df = pd.read_csv(f, sep='\t', header=None, skiprows=1,names=header)
        
            df['DNA_sum'] = df['DNA1']+df['DNA2']+df['DNA3']+df['DNA4']+df['DNA5']
            df['rep2'] = (df['RNA2'])/(df['DNA_sum']/NUM_DNA)
            df['rep3'] = (df['RNA3'])/(df['DNA_sum']/NUM_DNA)
            df['rep4'] = (df['RNA4'])/(df['DNA_sum']/NUM_DNA)
            df['rep5'] = (df['RNA5'])/(df['DNA_sum']/NUM_DNA)

            print('rep2 and rep3: ', spearmanr(df['rep2'], df['rep3']))
            print('rep2 and rep4: ', spearmanr(df['rep2'], df['rep4']))
            print('rep2 and rep5: ', spearmanr(df['rep2'], df['rep5']))
            print('rep3 and rep4: ', spearmanr(df['rep3'], df['rep4']))
            print('rep3 and rep5: ', spearmanr(df['rep3'], df['rep5']))
            print('rep4 and rep5: ', spearmanr(df['rep4'], df['rep5']))           

if(len(sys.argv)!=3):
    exit(ProgramName.get()+" <counts_file_path> <task>\n")
(file, task)=sys.argv[1:]
corr(file, task)