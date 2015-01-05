#!/usr/bin/env python

class MRNA:

    def __init__(self, mrna_id, seq_id, exon_id, exon_start, exon_stop, exon_length):
        self.mrna_id = mrna_id
        self.seq_id = seq_id
        self.exon_id = exon_id
        self.exon_start = exon_start
        self.exon_stop = exon_stop
        self.exon_length = exon_length
        self.snp_count = 0
