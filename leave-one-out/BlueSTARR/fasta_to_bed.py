from Bio import SeqIO

fasta_file = "/datacommons/igvf-pm/A549/leave-one-out/Dex-200/data/chr1.fasta"
bed_file = "/datacommons/igvf-pm/A549/leave-one-out/Dex-200/data/chr1.bed"

with open(bed_file, 'w') as bed:
    # Parse the input FASTA file
    for record in SeqIO.parse(fasta_file, "fasta"):
        # Extract the description (e.g., "/coord=chr1:778400-778700")
        description = record.description
        
        # Extract the coordinate string after "/coord="
        coord_str = description.split("/coord=")[-1]
        
        # Split the coordinate string into chromosome, start, and end
        chrom, positions = coord_str.split(":")
        start, end = positions.split("-")
        
        # BED format requires 0-based start, so subtract 1 from start position
        bed.write(f"{chrom}\t{int(start)-1}\t{end}\t{record.id}\n")
