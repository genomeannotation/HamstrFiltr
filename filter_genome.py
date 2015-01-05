#!/usr/bin/env python

import sys
from src.util import process_args, read_orthologs, read_vcf, update_gene_snp_count, read_genome 

def main():
    genomefile, orthofile, snpfile = process_args(sys.argv)  

    # Read ortho file, return a list of single-copy orthologous mrna ids
    print("Reading ortholog info in file " + orthofile + "...")
    orthologs = read_orthologs(orthofile)

    # Read vcf, return dict of seq_id: [snp_indices]
    print("Reading SNPs in file " + snpfile + "...")
    snps = read_vcf(snpfile)

    # Read gff
    print("Reading gff file " + genomefile + "...")
    mrnas = read_genome(genomefile)
    print("found " + str(len(mrnas)) + " exons") 

    # Keep genes that are single copy orthologs
    print("Total mRNAs in genome: " + str(len(mrnas)))
    mrnas = [m for m in mrnas if m.mrna_id in orthologs]
    print("Single copy orthologs: " + str(len(mrnas)))

    # Calculate number of SNPs on each mrna/exon
    for mrna in mrnas:
        if mrna.seq_id not in snps:
            sys.stderr.write("No snps on " + mrna.seq_id + "...\n")
            continue
        for snp_index in snps[mrna.seq_id]:
            if mrna.contains_index(snp_index):
                mrna.snp_count += 1

    # Print summary of results
    for mrna in mrnas:
        print("mrna " + mrna.mrna_id + " has " + str(mrna.snp_count) + " snps.")

    # Rank exons in descending order based on SNP count
    # There's some clever one-liner way to do this; ask me and I'll look it up

    # For the SNPpiest 200 exons, write output:
    # seq_id \t exon_start \t exon_end \t 'name'
    # TODO idk what 'name' is supposed to be, maybe gene_name, or exon_id? ## hi brian 'name' = gene_name 
	

###########################################

if __name__ == '__main__':
    main()
