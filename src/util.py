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
            if line.startswith("#"):
                continue
            fields = line.strip().split()
            seq_id = fields[0]
            index = fields[1]
            snps = (seq_id, index)
            result.append(snps)
        return result

def length_of_feature(items):
    start = int(items[3])
    end = int(items[4]) 
    return end - start + 1 

def get_mrna_id(fields):
    attributes = fields[8]
    split_attr = attributes.split(";")
    for attr in split_attr:
        if "Parent" in attr: 
            return attr.split("=")[1]

def read_genome(gfile):
    result = {} 
    with open(gfile, "r") as gff:
        for line in gff: 
            if line.startswith("#"):
                continue
            fields = line.strip().split()
            if len(fields) != 9:
                continue 
            exoncolumn = fields[2]
            if exoncolumn == "exon":     
                length = length_of_feature(fields)
                mrnaid = get_mrna_id(fields)
                if length >= 400:
                    print(mrnaid, length)

def update_gene_snp_count(gene, snps):
    pass
