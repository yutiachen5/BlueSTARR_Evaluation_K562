import sys
import re
import pandas as pd
import gzip
import os
from tqdm import tqdm
from FastaReader import FastaReader
from FastaWriter import FastaWriter

# discard bins in training set which are paralogous regions in test/validation set

def loadFasta(fasta_file, as_dict=False,uppercase=False, stop_at=None,
              revcomp=False):
    fastas = []
    seq = None
    header = None
        
    for r in (gzip.open(fasta_file) if fasta_file.endswith(".gz") else open(fasta_file)):
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
                         'id': [e[0].split(' /')[0] for e in fastas],
                         'sequence': [e[1] for e in fastas]})



def main(aligned_file, data_dir, Kircher_dir, out_dir):
    matched = pd.read_table(aligned_file, names=["qseqid", "sseqid"], dtype=str, header=None)

    # train_fasta = loadFasta(data_dir+'/train-presplit.fasta.gz')
    train_fasta = loadFasta(data_dir+'/all-train.fasta')
    val = loadFasta(data_dir+'/validation.fasta.gz')
    test = loadFasta(data_dir+'/test.fasta.gz')

    val_matched = pd.merge(val, matched, how='inner',left_on='id', right_on='qseqid')['sseqid'].tolist()
    test_matched = pd.merge(test, matched, how='inner',left_on='id', right_on='qseqid')['sseqid'].tolist()
    kircher_matched = pd.read_table(Kircher_dir, names=['location', 'id', 'sequence'], header=None)['id'].tolist()
    drop = pd.DataFrame({'id': list(set(val_matched+test_matched+kircher_matched))})
    print('# indices to be discarded:', len(drop))

    train_matched = pd.merge(train_fasta, drop, how='left', on='id', indicator=True)
    train_kept = train_matched.loc[train_matched['_merge'] == 'left_only']
    keep_idxs = train_kept.index
    print('# bins kept:',len(keep_idxs))
    print(round((len(train_fasta) - len(keep_idxs))/len(train_fasta)*100, 2), '% bins in training set were discarded (paralogous region+Kircher''s region).')


    fastaWriter=FastaWriter()
    # train_count = gzip.open(data_dir+'/train-presplit-counts.txt.gz','rt')
    train_count = gzip.open(data_dir+'/all-train-counts.txt.gz','rt')

    # out_fasta = gzip.open(out_dir+'/train.fasta.gz',"wt")
    # out_count = gzip.open(out_dir+'/train-counts.txt.gz','wt')
    out_fasta = gzip.open(out_dir+'/all-train-blacklisted.fasta.gz',"wt")
    out_count = gzip.open(out_dir+'/all-train-blacklisted-counts.txt.gz','wt')
    count_header = train_count.readline()
    print(count_header, end="", file=out_count)

    ls_def = train_fasta['location'].tolist()
    ls_seq = train_fasta['sequence'].tolist()

    for i in tqdm(range(len(train_fasta))):
        count_line = train_count.readline()
        if i in keep_idxs:
            fastaWriter.addToFasta(ls_def[i], ls_seq[i], out_fasta)
            print(count_line, end="", file=out_count)

    train_count.close()
    out_fasta.close()
    out_count.close()


if(len(sys.argv)!=5):
    exit(ProgramName.get()+" <aligned_file> <data_dir> <Kircher_region_dir> <out_dir>\n")
(aligned_file, data_dir, Kircher_dir, out_dir)=sys.argv[1:]

main(aligned_file, data_dir, Kircher_dir, out_dir)
# python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/leave-one-out/remove_paralogs.py /hpc/group/igvf/K562/leave-one-out/BlueSTARR/leave-one-out/BLASTN/all_aligned_300_cleaned.txt /hpc/group/igvf/K562/full-set/300bp/data-normalized /hpc/group/igvf/K562/full-set/300bp/data-normalized/matched_kircher.txt /hpc/group/igvf/K562/full-set/300bp/data-normalized
# python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/leave-one-out/remove_paralogs.py /hpc/group/igvf/A549/full-set/BLASTN/all_aligned_300_dex_cleaned.txt /hpc/group/igvf/A549/full-set/Dex-200/300-bases/data-normalized /hpc/group/igvf/A549/full-set/Dex-200/300-bases/data-normalized/matched_kircher.txt /hpc/group/igvf/A549/full-set/Dex-200/300-bases/data-normalized
# python /hpc/group/igvf/K562/leave-one-out/BlueSTARR/leave-one-out/remove_paralogs.py /hpc/group/igvf/A549/full-set/BLASTN/all_aligned_300_dmso_cleaned.txt /hpc/group/igvf/A549/full-set/DMSO-200/300-bases/data-normalized /hpc/group/igvf/A549/full-set/DMSO-200/300-bases/data-normalized/matched_kircher.txt /hpc/group/igvf/A549/full-set/DMSO-200/300-bases/data-normalized