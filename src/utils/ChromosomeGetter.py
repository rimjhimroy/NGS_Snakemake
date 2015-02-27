"""
@author: Jetse

The module ChromosomeGetter retrieves all different chromosomes from a file. At the moment only chromosomes can be
retrieved from a fasta file with an fai index.
"""
import csv


def getChromosomes(faiIndex):
    """
    The method getChromosomes retrieves the chromosomes of a fai indexed reference file
    """
    chromosomes = []
    with open(faiIndex) as indexFile:
        indexReader = csv.reader(indexFile, delimiter="\t")
        for line in indexReader:
            chromosomes.append(line[0])
    return chromosomes