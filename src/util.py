#!/usr/bin/env python

import sys

def process_args(args):
    if len(args) != 4:
        sys.stderr.write("usage: filter_genome.py <genome.gff> <orthologs.out> "
                         "<snps.vcf>\n")
        sys.exit()
    else:
        return args[1], args[2], args[3]

def read_orthologs(ofile):
    result = []
    with open(ofile, "r") as ortho:
        for line in ortho:
            fields = line.strip().split("|")
            ortho_id = fields[3] 
            result.append(ortho_id)
        return result

def read_vcf(vfile):
    result = []
    with open(vfile, "r") as vcf:
        for line in vcf:
            fields = line.strip().split()
            seq_id = fields[0]
            index = fields[1]
            snps = (seq_id, index)
            result.append(snps)
        return result

def update_gene_snp_count(gene, snps):
    pass
