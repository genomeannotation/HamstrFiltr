#!/usr/bin/env python

import sys

def process_args(args):
    if len(args) != 4:
        sys.stderr.write("usage: filter_genome.py <genome.gff> <orthologs.out> "
                         "<snps.vcf>\n")
        sys.exit()
    else:
        return args[1], args[2], args[3]

def read_genome(gfile):
    pass

def read_orthologs(ofile):
    pass

def read_vcf(vfile):
    pass

