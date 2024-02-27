#!/usr/bin/env python
import cairo 
import argparse
import re

def get_args():
    parser= argparse.ArgumentParser()
    parser.add_argument("-f", "--fasta", help="Fasta file", required=True, type = str)
    parser.add_argument("-m", "--motif", help="Motif file", required=True, type = str)
    parser.add_argument("-w", "--write", help="Output file", required=True, type = str)
    parser.add_argument("-ol", "--oneline", help="Oneline fasta intermediate file", required=False, type = str)

    return parser.parse_args()
 
args = get_args()
f=args.fasta
m=args.motif
w=args.write
ol=args.oneline

motif_dict = {}
with open(m, "r") as motifs:
    while True:
        line  = motifs.readline().strip()
        if (line == ""):
            break
        motif_dict[line] = len(line)
        

        match_motif = re.findall(r'([c|t]gc[c|t])', line)
        match_gene_name = re.findall(r'>([A-Za-z0-9]+)', line)

def oneline_fasta(f):
    with open(f, "r") as rf, open(w,"w") as wf:
        seq = ''
        while True:
            line = rf.readline().strip()
            if not line:
                break
            if line.startswith(">"):
                if seq != "":
                    wf.write(seq + "\n") 
                seq = ''
                wf.write(line + "\n") 
            else:
                seq += line 
        wf.write(seq)

oneline_fasta(f)


class Motif:
    def __init__(self, motif_seq, length, color, start_position, gene_name):
        self.motif_seq = motif_seq
        self.length = length
        self.color = color
        self.start_position = start_position
        self.gene_name = gene_name

class Gene:
    def __init__(self, name, length):
        pass
    def counter(self, name):
        pass


with open(ol, 'r') as fasta:
    while True: 
        line = fasta.readline().strip()
        if (line == ""):
            break
        match_gene_length = re.search(r'[AGC]', line)
        print(match_gene_length.groups(1))