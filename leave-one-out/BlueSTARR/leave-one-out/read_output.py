import glob
import os
import re

# Step 1: Define the folder containing the .out files
folder_path = '/datacommons/igvf-pm/A549/leave-one-out/Dex-200/slurm/outputs'

# Step 2: Use glob to find all .out files in the folder
out_files = [f for f in os.listdir(folder_path) if f.endswith('.out')]

# Step 3: Initialize a list to store the extracted information
rho_values = {}

# Step 4: Loop through each .out file and extract the information
for file_path in out_files:
    chromosome = int(file_path.split('.')[0])
    with open(folder_path+'/'+file_path, 'r') as file:
        content = file.read()
        # Use regex to find the information starting with "A549 rho="
        matches = re.findall(r"A549 rho= ([0-9.]+)", content)
        if matches:
            rho_values[chromosome] = round(float(matches[0]), 4)
        else:
            rho_values[chromosome] = chromosome
rho_values = {key: rho_values[key] for key in sorted(rho_values.keys())}

print(rho_values.values())
print(len(rho_values))
