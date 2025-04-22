# convert txt predictions to bed

import sys
from tqdm import tqdm

def txt_to_bed(input_dir, outfile):

    with open(outfile, 'w') as fout:
        for i in tqdm(range(1, 1065)):
        # for i in tqdm(range(426, 427)):

            infile = input_dir+'pred'+str(i)+'.txt'
            with open(infile, 'r') as fin:
                header = True
                for line in fin:
                    if header:
                        header = False
                        continue

                    line = line.strip()
                    if not line:
                        continue  # skip empty lines if any

                    fields = line.split('\t')

                    if len(fields) == 5:
                        spdi_parts = fields[4].split(':')  # e.g. NC_000001.11:104896:T:G
                        start = spdi_parts[1]
                        end = str(int(start)+1)
                        ref = spdi_parts[2]
                        alt = spdi_parts[3]
                        chrom = fields[0]
                        effect = fields[3]
                        spdi = fields[4]

                        out_line = [
                            chrom,  
                            start,  
                            end,  
                            effect, 
                            ref,        
                            alt,
                            spdi   
                        ]
                    elif len(fields) == 6:
                        spdi_parts = fields[5].split(':')  # e.g. NC_000001.11:104896:T:G
                        start = spdi_parts[1]
                        end = str(int(start)+1)
                        ref = spdi_parts[2]
                        alt = spdi_parts[3]
                        chrom = fields[0]
                        effect = fields[3]
                        spdi = fields[4]

                        out_line = [
                            chrom,  
                            start,  
                            end,  
                            effect, 
                            ref,        
                            alt,
                            spdi   
                        ]
                    else:
                        print(fields)


                    fout.write("\t".join(out_line) + "\n")



if(len(sys.argv)!=3):
    exit(ProgramName.get()+" <input-dir:/.../> <output.bed> \n")
(input_dir,outfile)=sys.argv[1:]
txt_to_bed(input_dir, outfile)

# python /work/igvf-pm/K562/CRE-preds/to_bed.py /work/igvf-pm/K562/CRE-preds/processed-preds/ /work/igvf-pm/K562/CRE-preds/processed-preds/preds.bed