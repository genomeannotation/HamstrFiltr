#!/usr/bin/env python

import sys
from src.util import process_args, read_orthologs, read_vcf, update_gene_snp_count
from src.gene import Gene, read_genome

def main():
    genomefile, orthofile, snpfile = process_args(sys.argv)  
   
    # Read in single copy ortholog info
    # TODO decide what exactly we need to store about orthologs;
    #  I'm thinking just the gene_id or gene_name? In a list?
    print("Reading ortholog info in file " + orthofile + "...")
    orthologs = read_orthologs(orthofile)
    print(orthologs)

    # Read in SNP info
    # TODO decide what exactly we need to store about SNPs;
    #  I'm thinking just sequence and index
    print("Reading SNPs in file " + snpfile + "...")
    snps = read_vcf(snpfile)

    # Read gff
    # TODO decide what exactly we need to store about genes;
    #  I'm thinking just sequence, id/name, and a list of exon start/stops
    #  Maybe also the exons' ids/names -- will ask boss
    print("Reading gff file " + genomefile + "...")
    genes = read_genome(genomefile)

    # Keep genes that are single copy orthologs
    # Will probably look like 
    #    genes = [g for g in genes if g.name in orthologs]

    # For each single copy ortholog gene, choose longest exon
    # Could look like
    #    for gene in genes:
    #        gene.discard_all_but_longest_exon()
    
    # Keep genes whose longest exon (now their only exon) is >= 400bp
    # Could look like
    #    genes = [g for g in genes if g.exon_length() >= 400]

    # For each exon, find out how many SNPs it contains
    # Could look like
    #    for gene in genes:
    #        update_gene_snp_count(gene, snps)

    # Rank exons in descending order based on SNP count
    # There's some clever one-liner way to do this; ask me and I'll look it up

    # For the SNPpiest 200 exons, write output:
    # seq_id \t exon_start \t exon_end \t 'name'
    # TODO idk what 'name' is supposed to be, maybe gene_name, or exon_id? ## hi brian 'name' = gene_name 
	

###########################################

if __name__ == '__main__':
    main()
