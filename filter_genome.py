#!/usr/bin/env python

import sys
from src.util import process_args, read_orthologs, read_vcf, update_gene_snp_count, read_genome 

def main():
    genomefile, orthofile, snpfile, prefix = process_args(sys.argv)  

    # Read ortho file, return a dictionary mapping bdor mrna_ids 
    #  to dmel mrna_ids
    sys.stderr.write("Reading ortholog info in file " + orthofile + "...\n")
    orthologs = read_orthologs(orthofile)

    # Read vcf, return dict of seq_id: [snp_indices]
    sys.stderr.write("Reading SNPs in file " + snpfile + "...\n")
    snps = read_vcf(snpfile)

    # Read gff
    sys.stderr.write("Reading gff file " + genomefile + "...\n\n")
    mrnas, stats = read_genome(genomefile)
    statfile = open(prefix + ".stats", "w")
    statfile.write(stats)

    # Keep genes that are single copy orthologs
    mrnas = [m for m in mrnas if m.mrna_id in orthologs]
    statfile.write("Single copy orthologs: " + str(len(mrnas)) + "\n")
    statfile.close()

    # Calculate number of SNPs on each mrna/exon
    sys.stderr.write("\nCounting number of SNPs on each exon; this could take a minute...\n\n")
    with open(prefix + ".snps.bed", "w") as snpout:
        snpout.write("exon_id\tseq_id\tsnp_number\tsnp_index\n")
        for mrna in mrnas:
            if mrna.seq_id not in snps:
                sys.stderr.write("No snps on " + mrna.seq_id + "...\n")
                continue
            snp_number = 1
            for snp_index in snps[mrna.seq_id]:
                if mrna.contains_index(snp_index):
                    fields = [mrna.exon_id, mrna.seq_id, 
                            "snp_" + str(snp_number), str(snp_index)]
                    snpout.write("\t".join(fields) + "\n")
                    mrna.snp_count += 1
                    snp_number += 1

    # Rank exons in descending order based on SNP count
    mrnas = sorted(mrnas, key=lambda x: x.snp_count, reverse=True)

    # Print summary of results
    with open(prefix + ".out", "w") as outfile:
        outfile.write("\t".join(["seq_id", "exon_start", "exon_end", "exon_id",
                         "snp_count", "snp_density", "dmel_ortholog_id"]) + "\n")
        for mrna in mrnas:
            dmel_id = orthologs[mrna.mrna_id]
            snp_density = float(mrna.snp_count) / mrna.exon_length
            outfile.write("\t".join([mrna.seq_id, mrna.exon_start, 
                mrna.exon_stop, mrna.exon_id, str(mrna.snp_count), 
                str(snp_density), dmel_id]) + "\n")


###########################################

if __name__ == '__main__':
    main()
