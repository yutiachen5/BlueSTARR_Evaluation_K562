from tqdm import tqdm
import pandas as pd 

# get id and its corresponding chr
def id_chr(fasta_file):
    id_to_chr = {}
    with open(fasta_file, 'r') as file:
        for line in file:
            if line.startswith('>'):
                parts = line.strip().split()
                seq_id = parts[0][1:]  # Remove the '>'
                chromosome = parts[1].split('=')[1].split(':')[0]  # Get the chrinates part after '/chr='
                id_to_chr[seq_id] = chromosome
    return id_to_chr
id_to_chr = id_chr('/datacommons/igvf-pm/K562/leave-one-out/all-train.fasta')

print('length of all fasta: ', len(id_to_chr))


columns = ["qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", 
           "qstart", "qend", "sstart", "send", "evalue", "bitscore"]
paralog = pd.read_table('/datacommons/igvf-pm/K562/leave-one-out/all_aligned.txt', names=columns)
print('length of original matches: ',len(paralog))

# remove the pair that has bin matched with itself
paralog = paralog.loc[paralog['qseqid'] != paralog['sseqid'], ]
paralog = paralog.reset_index(drop = True)

# discard the pair that has match within the same chr
ls_q = paralog['qseqid']
ls_s = paralog['sseqid']
ls_type = []

for i in tqdm(range(len(ls_q))):
    if id_to_chr[str(ls_q[i])] == id_to_chr[str(ls_s[i])]:
        ls_type.append(0) # paralogs on the same chr
    else:
        ls_type.append(1) # paralogs on different chrs
paralog['type'] = ls_type
paralog = paralog.loc[paralog['type'] == 1, ]

# drop unuseful columns
paralog = paralog[['qseqid','sseqid']]
paralog = paralog.reset_index(drop = True)
print('length of cleaned matches: ', len(paralog))
paralog.to_csv('/datacommons/igvf-pm/K562/leave-one-out/all_aligned_cleaned.csv', index=False)
print(paralog.head())