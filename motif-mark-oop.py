#!/usr/bin/env python
from __future__ import annotations
import cairo 
import argparse
import re


#set defaults for cairo plotting
width, height = 1000, 1000

surface = cairo.PDFSurface("test.pdf", width, height)

context = cairo.Context(surface)

#set_custom_palette_color(index: int, red: float, green: float, blue: float, alpha: float)→ None

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

    #def draw function
 

class Gene:
    def __init__(self, name, length):
        self.name = name
        self.length = length
    def counter(self, name):
        pass
    #def draw function (self, x, y, name, length)
    def gene_draw(self, x, y, name, length):
        context.set_line_width(2)
        context.set_source_rgba(1, 0.2, 0.2, 1)
        context.move_to(x, y)
        context.line_to(x + gene_length, y)
        context.stroke()
        context.set_source_rgba(0, 0, 0, 1)
        context.move_to(x+10, y+10)
        context.show_text(name)
        context.stroke()


class Exon:
    def __init__(self, start, end, colot, gene):
        self.name = name
        self.length = length

    #def draw function
        
class Intron:
    def __init__(self, start, end, colot, gene):
        self.name = name
        self.length = length

    #def draw function (self, x = int, y = int, exon_len = int)


with open(ol, 'r') as fasta:
    i = 0
    while True:
        header = fasta.readline().split()
        sequence = fasta.readline().split()
        if (header == []):
            break
        gene_name = header[0][1:]
        gene_length = len(sequence[0])
        #add gene to class
        newgene = Gene(header[0][1:], gene_length)
        
        #draw gene action
        newgene.gene_draw(20, 50+i, header[0][1:], gene_length)

        #extract exon by grabbing all capital letters
        #calculate exon length

        #add exon to class


        #compile motif with regex
        #m.span 

        i+=100
