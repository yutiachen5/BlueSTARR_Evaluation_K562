import pandas as pd

# Define the file path
file_path = "/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/data-unbiased/downsampled-counts.txt"
output_file_path = "/datacommons/igvf-pm/A549/leave-one-out/DMSO-200/data-1-1/downsampled-single-rep-counts.txt"

df = pd.read_csv(file_path, sep="\t", skiprows=1,header=None)
print(df.head())

# Extract the first and fourth columns
df_selected = df.iloc[:, [2, 6]]

header = "DNA=1   RNA=1\n"
with open(output_file_path, 'w') as file: 
    file.write(header)  
    df_selected.to_csv(file, sep='\t', index=False, header=None)  
