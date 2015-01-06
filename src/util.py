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
    """Returns a list of bdor, dmel mrna_id tuples for single-copy orthologous mRNAs"""
    result = {}
    with open(ofile, "r") as ortho:
        for line in ortho:
            fields = line.strip().split("|")
            dmel_id = fields[0]
            bdor_id = fields[3] 
            result[bdor_id] = dmel_id
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

def get_parent_id(fields):
    attributes = fields[8]
    split_attr = attributes.split(";")
    for attr in split_attr:
        if "Parent" in attr: 
            return attr.split("=")[1]

def get_id(fields):
    attributes = fields[8]
    split_attr = attributes.split(";")
    for attr in split_attr:
        if "ID" in attr: 
            return attr.split("=")[1]

def first_or_last_exon(mrna_dict, mrna_id, start, stop):
    mrna_start_stop = mrna_dict[mrna_id]
    mrna_start = mrna_start_stop[0]
    mrna_stop = mrna_start_stop[1]
    if start == mrna_start or stop == mrna_stop:
        return True
    else:
        return False

def read_genome(gfile):
    # Count genes so we know how many we lose to the "must contain exon
    #  longer than 400bp" constraint
    total_genes = 0
    # Store a dict that maps mrna_ids to tuples containing 
    #  seq id, exon id, exon start, exon stop and exon length
    mrna_to_exon_tuple = {} 
    # Also store a dict to track mrna starts and stops so we can
    #  determine if exons are the first/last exon on the gene
    mrna_to_start_stop = {}
    with open(gfile, "r") as gff:
        for line in gff: 
            if line.startswith("#"):
                continue
            fields = line.strip().split()
            if len(fields) != 9:
                continue 
            feature_type = fields[2]
            if feature_type == "gene":
                total_genes += 1
            elif feature_type == "mRNA":
                mrna_id = get_id(fields)
                start = fields[3]
                stop = fields[4]
                mrna_to_start_stop[mrna_id] = (start, stop)
            elif feature_type == "exon":     
                length = length_of_feature(fields)
                mrna_id = get_parent_id(fields)
                seq_id = fields[0]
                start = fields[3]
                stop = fields[4]
                exon_id = get_id(fields)
                if length < 400:
                    continue 
                elif first_or_last_exon(mrna_to_start_stop, mrna_id, start, stop):
                    continue
                if mrna_id in mrna_to_exon_tuple:
                    length_from_dict = mrna_to_exon_tuple[mrna_id][4]
                    if length > length_from_dict:
                        mrna_to_exon_tuple[mrna_id] =\
                                (seq_id, exon_id, start, stop, length)
                else:
                    mrna_to_exon_tuple[mrna_id] =\
                            (seq_id, exon_id, start, stop, length)
    # Pack dictionary entries into a list of MRNA objects
    result = []
    for mrna_id, attr in mrna_to_exon_tuple.items():
        mrna = MRNA(mrna_id, attr[0], attr[1], attr[2], attr[3], attr[4])
        result.append(mrna)
    sys.stderr.write("Total genes in genome: " + str(total_genes) + "\n")
    sys.stderr.write("Genes with at least one internal exon > 400bp long: " + 
            str(len(result)) + "\n")
    return result

def update_gene_snp_count(gene, snps):
    pass
