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
        
class ygcy:
    def __init__(self, start, end, gene):
        self.start = start
        self.end = end
        self.gene = gene


    def ygcy_draw(self, x, y, start, end):
        context.set_line_width(10)
        context.set_source_rgba(0.2, 0.5, 0.7, 1)
        context.move_to(x + start, y)
        context.line_to(start + 4, y)
        context.stroke()
        context.set_source_rgba(0, 0, 0, 1)
 

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
    def __init__(self, start, end, gene):
        self.start = start
        self.end = end
        self.gene = gene


    def exon_draw(self, x, y, start, end, exon_length):
        context.set_line_width(10)
        context.set_source_rgba(0.5, 0.5, 0.5, 1)
        context.move_to(x + start, y)
        context.line_to(end + exon_length, y)
        context.stroke()
        context.set_source_rgba(0, 0, 0, 1)
        
class Intron:
    def __init__(self, start, end, gene):
        self.start = start
        self.end = end
        self.gene = gene
    def intron_draw(self, x, y, intron_length):
        context.set_line_width(10)
        context.set_source_rgba(0.7, 0.7, 0.7, 1)
        context.move_to(x, y)
        context.line_to(x + intron_length, y)
        context.stroke()
        context.set_source_rgba(0, 0, 0, 1)


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

        print(f'the gene length is: {gene_length}')
        
        #draw gene action
        newgene.gene_draw(20, 50+i, header[0][1:], gene_length)

        #extract exon by grabbing all capital letters
        Exon_pattern = re.compile("[AGCT]")
        exons = Exon_pattern.findall(sequence[0])


        # Find the exon using a regular expression
        exons_string = ''.join(exons)
        sequence = ''.join(sequence)
        match = re.search('[A-Z]+', sequence)

        if match:
            uppercase_section = match.group()  # Get the uppercase section
            exon_start = match.start()  # Get the start position of the uppercase section
            exon_end = match.end()

        else:
            pass
            #print("No uppercase section found in the sequence.")
        
        if exons:
            exon_length = len(exons)
            print("Exon length:", exon_length)
        else:
            pass
            #print("No exons found in the sequence.")

        #add exon to class
        new_exon = Exon(exon_start, exon_end, newgene)

        new_exon.exon_draw(20, 50+i, exon_start, exon_end, exon_length)

        #compile motif with regex
        #ygcy_pattern = re.compile("(t|c)g(c|t|c)")
        ygcy_pattern = re.compile("[t|cgct|c]")
        ygcys = ygcy_pattern.findall(sequence[0])


        # Find the exon using a regular expression
        ygcys_string = ''.join(ygcys)
        #ygcy_match = re.search('(t|c)g(c|t|c)', sequence)
        ygcy_match = re.search('[t|c]gc[t|c]', sequence)


        if ygcy_match:
            ygcy_section = ygcy_match.group()  # Get the uppercase section
            ygcy_start = ygcy_match.start()  # Get the start position of the uppercase section
            ygcy_end = ygcy_match.end()
            print(ygcy_start)
            print(ygcy_end)
        else:
            print("No uppercase section found in the sequence.")
        
        if ygcys:
            ygcy_length = len(ygcys_string)
            print("ygcy length:", ygcy_length)
            new_ygcy = ygcy(ygcy_start, ygcy_end, newgene)

            new_ygcy.ygcy_draw(20, 50+i, ygcy_start, ygcy_end)
        else:
            print("No ygcys found in the sequence.")

        #add ygcy to class
        #new_ygcy = ygcy(ygcy_start, ygcy_end, newgene)

        #new_ygcy.ygcy_draw(20, 50+i, ygcy_end, ygcy_end, ygcy_length)

        #m.span 

        i+=100
