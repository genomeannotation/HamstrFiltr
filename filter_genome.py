#!/usr/bin/env python

import sys
from src.util import process_args, read_orthologs, read_vcf, update_gene_snp_count, read_genome 

def main():
    genomefile, orthofile, snpfile = process_args(sys.argv)  

    # Read ortho file, return a list of single-copy orthologous mrna ids
    sys.stderr.write("Reading ortholog info in file " + orthofile + "...\n")
    orthologs = read_orthologs(orthofile)

    # Read vcf, return dict of seq_id: [snp_indices]
    sys.stderr.write("Reading SNPs in file " + snpfile + "...\n")
    snps = read_vcf(snpfile)

    # Read gff
    sys.stderr.write("Reading gff file " + genomefile + "...\n")
    mrnas = read_genome(genomefile)
    sys.stderr.write("found " + str(len(mrnas)) + " exons\n") 

    # Keep genes that are single copy orthologs
    sys.stderr.write("Total mRNAs in genome: " + str(len(mrnas)) + "\n")
    mrnas = [m for m in mrnas if m.mrna_id in orthologs]
    sys.stderr.write("Single copy orthologs: " + str(len(mrnas)) + "\n")

    # Calculate number of SNPs on each mrna/exon
    sys.stderr.write("Counting number of SNPs on each exon; this could take a minute...\n")
    for mrna in mrnas:
        if mrna.seq_id not in snps:
            sys.stderr.write("No snps on " + mrna.seq_id + "...\n")
            continue
        for snp_index in snps[mrna.seq_id]:
            if mrna.contains_index(snp_index):
                mrna.snp_count += 1

    # Rank exons in descending order based on SNP count
    mrnas = sorted(mrnas, key=lambda x: x.snp_count, reverse=True)

    # Print summary of results
    for mrna in mrnas:
        print("\t".join([mrna.seq_id, mrna.exon_start, mrna.exon_stop, mrna.mrna_id, str(mrna.snp_count)]))

    # For the SNPpiest 200 exons, write output:
    # seq_id \t exon_start \t exon_end \t 'name'
    # TODO idk what 'name' is supposed to be, maybe gene_name, or exon_id? ## hi brian 'name' = gene_name 
	

###########################################

if __name__ == '__main__':
    main()
