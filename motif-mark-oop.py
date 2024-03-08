#!/usr/bin/env python

#Author: Sydney Hamilton
#Collaborators: Tam Ho, Anna Grace Welch

from __future__ import annotations
import cairo 
import argparse
import re


def get_args():
    parser= argparse.ArgumentParser()
    parser.add_argument("-f", "--fasta", help="Fasta file", required=True, type = str)
    parser.add_argument("-m", "--motif", help="Motif file", required=True, type = str)

    return parser.parse_args()
 
args = get_args()
f=args.fasta
m=args.motif

def oneline_fasta(f):
    '''this function takes the input fasta file and converts the sequence line to oneline and strips the new line so it can be searched through in regex more easily'''
    with open(f, "r") as rf, open(f'{f}_oneline',"w") as wf:
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
        return seq


oneline_fasta(f)

#open fasta file and scale heights and width values
with open(f'{f}_oneline', 'r') as fasta:
    i = 0
    lengths = []
    scaled_height = 100
    while True:
        header = fasta.readline().split() #grabs the first line of the fasta as a list
        sequence = fasta.readline().strip()
        if (header == []): #breaks when the list is empty
            break
        gene_name = header[0][1:]
        gene_length = len(sequence)
        lengths.append(len(sequence))
        scaled_height +=100
scaled_width = max(lengths)

#making motif regular expresssion dictionary
motif_reg_dict = {}
motif_reg_dict = {
        "A" : "[A]",
        "T" : "[T]",
        "G" : "[G]", 
        "C" : "[C]",
        "U" : "[TU]",
        "W" : "[AT]",
        "S" : "[CG]",
        "M" : "[AC]",
        "K" : "[GT]",
        "R" : "[AG]",
        "Y" : "[CT]",
        "B" : "[CGT]",
        "D" : "[AGT]",
        "H" : "[ACT]",
        "V" : "[ACG]",
        "N" : "[ACGT]",
    }

#making color list and motif dictionary to coincide with the color
color_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 102, 102), (153, 0, 153)]
motif_color_dict = {}

def convert_motif(string): 
    '''this function takes a string and converts it to a regular expression to be used later on to find motifs in the sequence'''
    string = string.upper()
    verted_motif = ""
    for x in string: 
        verted_motif+=motif_reg_dict[x]
    return(verted_motif)
    
#adding length to a motif_dict and creating a motif list
motif_dict = {}
motif_list = []
with open(m, "r") as motifs:
    while True:
        line  = motifs.readline().strip()
        if (line == ""):
            break
        motif_list.append(line.upper())
        motif_dict[line] = len(line)

motif_colors = color_list[0:len(motif_list)]

#assmebling the motif color dictionary
for i in range(0,len(motif_list)):
    if not motif_color_dict.get(motif_list[i]):
        motif_color_dict[motif_list[i]] = motif_colors[i]

motif_color_dict["Exon"] = (0,0,0)


#set defaults for cairo plotting
width, height = scaled_width+50, scaled_height+50

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, gene_length+50, height)

context = cairo.Context(surface)
context.set_source_rgb(1, 1, 1)
context.paint()


# Set up variables for legend
legend_x = 50
legend_y = scaled_height - 50
legend_spacing = 20
legend_font_size = 12

# Save the surface to a PNG file
surface.write_to_png("legend.png")


# Draw legend
for label, color in motif_color_dict.items():
    # Draw colored square
    context.set_source_rgb(*color)
    context.rectangle(legend_x, legend_y, 10, 10)
    context.fill()

    # Draw legend label
    context.set_source_rgb(0, 0, 0)  # Set text color to black
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(legend_font_size)
    context.move_to(legend_x + 15, legend_y + 8)
    context.show_text(label)

    # Move to the next legend item
    legend_spacing = 20
    legend_y += legend_spacing





class Motif:
    '''this class creates motif objects and draws them'''
    def __init__(self, motif_seq, length, color, start_position):
        self.motif_seq = motif_seq
        self.length = length
        self.color = color
        self.start_position = start_position
        self.gene_name = gene_name

    #def draw function
    def motif_draw(self, x, y, name, length, start, end, color):
        context.set_line_width(10)
        context.set_source_rgb(*color)
        context.move_to(x + start, y)
        context.line_to(x + end, y)
        context.stroke()
 

class Gene:
    '''this class creates gene/intron objects and draws them'''
    def __init__(self, name, length):
        self.name = name
        self.length = length
    #def draw function (self, x, y, name, length)
    def gene_draw(self, x, y, name, length):
        context.set_line_width(2)
        context.set_source_rgb(0, 0, 0)
        context.move_to(x, y)
        context.line_to(x + gene_length, y)
        context.stroke()
        context.set_source_rgba(0, 0, 0, 1)
        context.move_to(x+10, y+15)
        context.show_text(name)
        context.stroke()


class Exon:
    '''this class creates exon objects and draws them'''
    def __init__(self, start, end, gene):
        self.start = start
        self.end = end
        self.gene = gene


    def exon_draw(self, x, y, start, end, exon_length):
        context.set_line_width(10)
        context.set_source_rgb(0, 0, 0)
        context.move_to(x + start, y)
        context.line_to(x + end, y)
        context.stroke()

#this is the main open 'function' that assmebles all the above and uses them to draw the final picture in png format
with open(f'{f}_oneline', 'r') as fasta:
    i = 0
    while True:
        header = fasta.readline().split() #grabs the first line of the fasta as a list
        sequence = fasta.readline().strip()
        if (header == []): #breaks when the list is empty
            break
        gene_name = header[0][1:]
        gene_length = len(sequence)
        #add gene to class
        newgene = Gene(header[0][1:], gene_length) 
        #draw gene action
        newgene.gene_draw(20, 46+i, header[0][1:], gene_length)
        #extract exon by grabbing all capital letters
        Exon_pattern = re.compile("[AGCT]")
        exons = Exon_pattern.findall(sequence)
        exons_string = ''.join(exons)
 
        match = re.search('[A-Z]+', sequence)
        if match:
            exon_start = match.start()  # Get the start position of the uppercase section
            exon_end = match.end()
        else:
            pass
            #print("No uppercase section found in the sequence.")     
        if exons:
            exon_length = len(exons)
        else:
            pass
            #print("No exons found in the sequence.")
        #add exon to class
        new_exon = Exon(exon_start, exon_end, newgene)
        new_exon.exon_draw(20, 50+i, exon_start, exon_end, exon_length)

        color_index = 0
        for m in motif_dict:
            converted_motif = convert_motif(m)
            upper_seq = sequence.upper()
            match_motif = re.finditer(converted_motif, upper_seq)
            for match in match_motif:
                new_motif = Motif(m, motif_dict[m], color_list[color_index], match.start())
                new_motif.motif_draw(20, 42+i, m, motif_dict[m], match.start(), match.end(), motif_color_dict[m.upper()])
        i+=100

surface.write_to_png(f'{f}.png')