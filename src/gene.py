#!/usr/bin/env python

import sys

def read_genome(gfile):
    result = []
    with open(gfile, "r") as gff:
        for line in gff:
            pass 

class Gene:

    def __init__(self, seq_name, exons):
        self.seq_name = seq_name
        self.exons = exons

    def discard_all_but_longest_exon(self):
        pass

