# check pre-empted job by file size

import os

def get_small_file_numbers(directory_path, size_limit_mb=9):

    file_numbers = []
    
    # Iterate through files in the directory
    for file in os.listdir(directory_path):
        if file.startswith("pred"): 
            file_path = os.path.join(directory_path, file)
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Convert bytes to MB
            
            if file_size_mb < size_limit_mb:
                file_numbers.append(file.split('.txt')[0][4:])  # Extract the number part
    print(len(file_numbers))

    return ",".join(file_numbers), file_numbers

result, ls = get_small_file_numbers("/hpc/group/igvf/A549/extra_GCs/IGVF_var_preds/preds/DMSO")
print(result)