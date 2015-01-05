#!/usr/bin/env python

import sys
from src.mrna import MRNA

def process_args(args):
    if len(args) != 4:
        sys.stderr.write("usage: filter_genome.py <genome.gff> <orthologs.out> "
                         "<snps.vcf>\n")
        sys.exit()
    else:
        return args[1], args[2], args[3]

def read_orthologs(ofile):
    """Returns a list of mrna_ids for single-copy orthologous mRNAs"""
    result = []
    with open(ofile, "r") as ortho:
        for line in ortho:
            fields = line.strip().split("|")
            ortho_id = fields[3] 
            result.append(ortho_id)
        return result

def read_vcf(vfile):
    """Return dict of seq_id: [snp_indices]"""
    result = {}
    with open(vfile, "r") as vcf:
        for line in vcf:
            if line.startswith("#"):
                continue
            fields = line.strip().split()
            seq_id = fields[0]
            index = fields[1]
            if seq_id in result:
                result[seq_id].append(index)
            else:
                result[seq_id] = [index]
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

def get_exon_id(fields):
    attributes = fields[8]
    split_attr = attributes.split(";")
    for attr in split_attr:
        if "ID" in attr: 
            return attr.split("=")[1]

def read_genome(gfile):
    mrna_dict = {} 
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
                mrna_id = get_mrna_id(fields)
                seq_id = fields[0]
                start = fields[3]
                stop = fields[4]
                exon_id = get_exon_id(fields)
                if length < 400:
                    continue 
                if mrna_id in mrna_dict:
                    length_from_dict = mrna_dict[mrna_id][4]
                    if length > length_from_dict:
                        mrna_dict[mrna_id] = (seq_id, exon_id, start, stop, length)
                else:
                    mrna_dict[mrna_id] = (seq_id, exon_id, start, stop, length)
    # Pack dictionary entries into a list of MRNA objects
    result = []
    for mrna_id, attr in mrna_dict.items():
        mrna = MRNA(mrna_id, attr[0], attr[1], attr[2], attr[3], attr[4])
        result.append(mrna)
    return result

def update_gene_snp_count(gene, snps):
    pass
