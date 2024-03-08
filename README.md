# Motif Marker

### Introduction
Motifs are recurring nucleotide sequences within a gene's exon or intron. 

This script will take in a fasta formatted file with argparse input and a motif text file with motifs listed per line into an argparse argument and return a picture of the introns, exons, and motifs labeled with colors, as well as a legend and appropriate labaleing. This script only accounts for 1 exon per sequence. 

### Instructions
```conda create -n <your pycairo environment name>```

```conda install pycairo```

```conda activate <your pycairo environment name>```

Running your code:

```./motif-mark-oop.py -f <path to your_fasta_file>.fasta -m <path to your_motifs_file>.txt```

### Output

<your_fasta_file>.png
