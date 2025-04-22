import re
import pandas as pd
import os
import gzip
from FastaWriter import FastaWriter
from tqdm import tqdm
import sys

## generate input file for test-variants.py
## format: position     ref     seq

def loadFasta(fasta_path, seqlen, as_dict=False,uppercase=False, stop_at=None,
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
    return pd.DataFrame({'location': [e[0].split('=')[-1] for e in fastas],
                         'ref': ['ref='+e[1][int(seqlen/2)] for e in fastas],
                         'alleles':[e[1][int(seqlen/2)] for e in fastas],
                         'sequence': [e[1] for e in fastas]})

def writeFasta(output_dir, fasta_label,df):
    df.to_csv(output_dir+fasta_label+'.txt', header=None, sep='\t', index = False)

def main(fasta_dir, output_dir, seqlen):
    df = loadFasta(fasta_dir, seqlen)
    writeFasta(output_dir, 'test-ref',df)

if(len(sys.argv)!=4):
    exit(ProgramName.get()+" <fasta_dir> <output_dir/> <seqlen>\n")
(fasta_dir, output_dir, seqlen)=sys.argv[1:]
main(fasta_dir, output_dir, int(seqlen))