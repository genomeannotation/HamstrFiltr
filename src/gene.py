#!/usr/bin/env python

import sys

def read_genome(gfile):
    result = []
    with open(gfile, "r") as gff:
        for line in gff:
            pass 

class Gene:

    def __init__(self, gene_id, exons):
        self.gene_id = gene_id 
        self.exons = exons

    def discard_all_but_longest_exon(self):
        pass

