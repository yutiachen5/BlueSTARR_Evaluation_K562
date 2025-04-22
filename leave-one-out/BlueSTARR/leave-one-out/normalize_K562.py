import pandas as pd
import sys

input_rep1 = 123384250
input_rep2 = 130680200
input_rep3 = 134539576
output_rep1 = 116270841
output_rep2 = 217503220
output_rep3 = 219086330

def main(raw_data, output_dir, output_label):
    df_count = pd.read_csv(raw_data, sep='\t', header=None, skiprows=1)
    IN_COUNTS=open(raw_data,"rt")
    header=IN_COUNTS.readline()
    df_count.columns = ['input_rep1','input_rep2','input_rep3','output_rep1','output_rep2','output_rep3']

    c = 1000000
    df_count['input_rep1'] = df_count['input_rep1']/input_rep1*c
    df_count['input_rep2'] = df_count['input_rep2']/input_rep2*c
    df_count['input_rep3'] = df_count['input_rep3']/input_rep3*c
    df_count['output_rep1'] = df_count['output_rep1']/output_rep1*c
    df_count['output_rep2'] = df_count['output_rep2']/output_rep2*c
    df_count['output_rep3'] = df_count['output_rep3']/output_rep3*c

    output_file = output_dir+output_label+'-counts.txt'
    with open(output_file, 'w') as file:
        file.write(header)  
        df_count.to_csv(file, sep='\t', index=False, header=None) 

if(len(sys.argv)!=4):
    exit(ProgramName.get()+" <raw-data-path> <output-dir> <output-label>\n")
(raw_data,output_dir,output_label)=sys.argv[1:]
main(raw_data,output_dir,output_label)