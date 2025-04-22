import re
import pandas as pd
import os
from FastaWriter import FastaWriter
from tqdm import tqdm
from Rex import Rex
import gzip
rex=Rex()


def loadFasta(fasta_path, as_dict=False,uppercase=False, stop_at=None,
              revcomp=False):
    fastas = []
    seq = None
    header = None
    for r in (gzip.open(fasta_path) if fasta_path.endswith(".gz") else open(fasta_path)):
        if type(r) is bytes: r = r.decode("utf-8")
        r = r.strip()
        if r.startswith(">"):
            if seq != None and header != None:
                fastas.append([header, seq])
                if stop_at != None and len(fastas) >= stop_at:
                    break
            seq = ""
            header = r[1:]
        else:
            if seq != None:
                seq += r.upper() if uppercase else r
            else:
                seq = r.upper() if uppercase else r
    if stop_at != None and len(fastas) < stop_at:
        fastas.append([header, seq])
    elif stop_at == None:
        fastas.append([header, seq])
    if as_dict:
        return {h: s for h, s in fastas}
    if(revcomp):
        for rec in fastas:
            rc=generate_complementary_sequence(rec[1])
            rec[1]=rec[1]+"NNNNNNNNNNNNNNNNNNNN"+rc
    return pd.DataFrame({'location': [e[0] for e in fastas],
                         'chromosome': [e[0].split('chr')[1].split(':')[0] for e in fastas],
                         'sequence': [e[1] for e in fastas]})

def split_by_chr(input_fasta, input_counts, output_dir, set_name):
    # Dictionary to hold bins and indexes by chromosome
    chr_bin = {}
    chr_idx = {}
    fastaWriter=FastaWriter()
    len_seq = []
    len_count = []

    
    i = 1
    df_fasta = loadFasta(input_fasta)
    all_chr = list(df_fasta['chromosome'].unique())

    for c in all_chr:
        df_chr = df_fasta.loc[df_fasta['chromosome'] == c, ]
        chr_idx[c] = list(df_chr.index)
        df_chr.reset_index(inplace = True)

        output_file = open(output_dir+"/" +'chr'+c + set_name +".fasta","wt")

        ls_loc = list(df_chr['location'])
        ls_seq = list(df_chr['sequence'])

        for i in range(len(df_chr)):
            defline = ls_loc[i]
            seq = ls_seq[i]
            fastaWriter.addToFasta(defline,seq,output_file)
        len_seq.append(len(df_chr))


    # write counts into txt files by chr

    df_count = pd.read_csv(input_counts, sep='\t', header=None, skiprows=1)
    IN_COUNTS=open(input_counts,"rt")
    header=IN_COUNTS.readline()

    for c in all_chr:
        dftmp = df_count.loc[df_count.index.isin(chr_idx[c])]
        output_file = output_dir+'/'+'chr'+c+set_name+'-counts.txt'

        with open(output_file, 'w') as file: 
            file.write(header)  
            dftmp.to_csv(file, sep='\t', index=False, header=None)  
        len_count.append(len(dftmp)+1)
    
        print(f"Written {len(dftmp)} counts and header to {output_file}")

    print(len_seq)
    print(len_count)
        

# split_by_chr('/datacommons/igvf-pm/K562/leave-one-out/data-biased/downsampled-test.fasta',
#             '/datacommons/igvf-pm/K562/leave-one-out/data-biased/downsampled-test-counts.txt',
#             '/datacommons/igvf-pm/K562/leave-one-out/data-biased',
#             '-test')

# split_by_chr('/datacommons/igvf-pm/K562/leave-one-out/data-biased/downsampled-train.fasta',
#             '/datacommons/igvf-pm/K562/leave-one-out/data-biased/downsampled-train-counts.txt',
#             '/datacommons/igvf-pm/K562/leave-one-out/data-biased',
#             '-train')

# split_by_chr('/datacommons/igvf-pm/A549/leave-one-out/DMSO-100/data-unbiased/downsampled.fasta',
#             '/datacommons/igvf-pm/A549/leave-one-out/DMSO-100/data-unbiased/downsampled-counts.txt',
#             '/datacommons/igvf-pm/A549/leave-one-out/DMSO-100/data-unbiased',
#             '')

# split_by_chr('/datacommons/igvf-pm/K562/leave-one-out/data-unbiased/downsampled-test.fasta',
#             '/datacommons/igvf-pm/K562/leave-one-out/data-unbiased/downsampled-test-counts.txt',
#             '/datacommons/igvf-pm/K562/leave-one-out/data-unbiased/single-replicate',
#             '-test')

# split_by_chr('/datacommons/igvf-pm/K562/leave-one-out/data-unbiased/downsampled-train.fasta',
#             '/datacommons/igvf-pm/K562/leave-one-out/data-unbiased/single-replicate/downsampled-single-rep-train-counts.txt',
#             '/datacommons/igvf-pm/K562/leave-one-out/data-unbiased/single-replicate',
#             '-train')

# split_by_chr('/datacommons/igvf-pm/A549/leave-one-out/DMSO-150/data-unbiased/downsampled.fasta',
#             '/datacommons/igvf-pm/A549/leave-one-out/DMSO-150/data-unbiased/downsampled-counts.txt',
#             '/datacommons/igvf-pm/A549/leave-one-out/DMSO-150/data-unbiased',
#             '')


# split_by_chr('/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/data-1-1/downsampled.fasta',
#             '/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/data-1-1/downsampled-counts.txt',
#             '/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/data-1-1',
#             '')

# split_by_chr('/datacommons/igvf-pm/A549/leave-one-out/Dex-200/data-1-1/downsampled.fasta',
#             '/datacommons/igvf-pm/A549/leave-one-out/Dex-200/data-1-1/downsampled-counts.txt',
#             '/datacommons/igvf-pm/A549/leave-one-out/Dex-200/data-1-1',
#             '')

# split_by_chr('/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/data-normalized/downsampled.fasta',
#             '/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/data-normalized/downsampled-counts.txt',
#             '/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/data-normalized',
#             '')

# split_by_chr('/datacommons/igvf-pm/A549/leave-one-out/Dex-200/data-normalized/downsampled.fasta',
#             '/datacommons/igvf-pm/A549/leave-one-out/Dex-200/data-normalized/downsampled-counts.txt',
#             '/datacommons/igvf-pm/A549/leave-one-out/Dex-200/data-normalized',
#             '')

# split_by_chr('/datacommons/igvf-pm/K562/leave-one-out/data-normalized/downsampled-test.fasta',
#             '/datacommons/igvf-pm/K562/leave-one-out/data-normalized/downsampled-test-normalized-counts.txt',
#             '/datacommons/igvf-pm/K562/leave-one-out/data-normalized',
#             '-test')

# split_by_chr('/datacommons/igvf-pm/K562/leave-one-out/data-normalized/downsampled-train.fasta',
#             '/datacommons/igvf-pm/K562/leave-one-out/data-normalized/downsampled-train-normalized-counts.txt',
#             '/datacommons/igvf-pm/K562/leave-one-out/data-normalized',
#             '-train')


split_by_chr('/datacommons/igvf-pm/A549/leave-one-out/Dex-200/600-bases/data-normalized/downsampled.fasta.gz',
            '/datacommons/igvf-pm/A549/leave-one-out/Dex-200/600-bases/data-normalized/downsampled-counts.txt',
            '/datacommons/igvf-pm/A549/leave-one-out/Dex-200/600-bases/data-normalized',
            '')

# split_by_chr('/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/600-bases/data-normalized/downsampled.fasta.gz',
#             '/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/600-bases/data-normalized/downsampled-counts.txt',
#             '/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/600-bases/data-normalized',
#             '')