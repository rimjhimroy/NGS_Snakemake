"""
@version: 0.1
@author: Jetse

The FileControl module contains functions to check whether a fileformat is exactly as expected. When a
File is not as expected, a FileFormatException is thrown.

Supported files:
* fastq
    * Checked whether biopython can parse the full fastq file
    * Checked whether the reads only contain A,T,C,G or N characters
    * Checked whether the file contains at least a single read
    * If paired end, the number of reads will be compared, 
    the forward file has to contain the sam numer of reads as the reversed.
* vcf: 
    * Checked whether each column contains at least 8 columns
    * Checked whether file contains at least a single SNP
* fasta: 
    * Checked whether biopython can parse the full fasta file
    * Checked whether the reads only contain A,T,C,G or N characters (if DNA)
    * Checked whether the file contains at least a single sequence
    
"""
from Bio import SeqIO
from collections import Counter

class FileFormatException(Exception):
    pass

def fastqControl(forwardFastq, reversedFastq=None, dna=True):
    print("Checking: " + forwardFastq)
    forwardRecords = _fastqContentControl(forwardFastq, dna)
    print("Correct! File contains {} reads".format(forwardRecords))
    if reversedFastq != None:
        print("Checking: " + reversedFastq)
        reversedRecords = _fastqContentControl(reversedFastq, dna)
        print("Correct! File contains {} reads".format(reversedRecords))
        if forwardRecords != reversedRecords:
            raise FileFormatException("Forward file has not the same number of sequences as the reversed file when comparing " + forwardFastq + " with " + reversedFastq)
        print("Paired end is correct!")
        
def _fastqContentControl(fastqFile, dna=True):
    noOfRecords = 0
    try:
        for record in SeqIO.parse(open(fastqFile), "fastq"):
            lcs = Counter(record.seq.upper())
            if dna==True and sum([lcs["A"],lcs["T"],lcs["C"],lcs["G"],lcs["N"]])!=len(record.seq):
                raise FileFormatException("Illegal character found in " + fastqFile + " with sequence id: " + record.id)
            if max(record.letter_annotations["phred_quality"]) > 72 or min(record.letter_annotations["phred_quality"]) < 0:
                raise FileFormatException("Invalid quality score in " + fastqFile + " with sequence id: " + record.id)
            noOfRecords += 1
    except ValueError as e:
        raise FileFormatException(e)
    if noOfRecords == 0:
        raise FileFormatException(fastqFile + " contains no sequences...")
    return noOfRecords

def vcfControl(vcfFile):
    print("Checking: " + vcfFile)
    lineNo = 0
    snps = 0
    with open(vcfFile) as vcfReader:
        lineNo += 1
        for line in vcfReader:
            if line.startswith("#"):
                continue
            elif line.isspace():
                continue
            snps += 1
            columns = line.split()
            if len(columns) < 8:
                raise FileFormatException("Too less columns in line {}, at least 8 expected, {} found".format(lineNo, len(columns)))
    if snps == 0:
        raise FileFormatException("No SNPs found in vcf file!")
    print("{} SNPs found in {}".format(snps,vcfFile))
    
def fastaControl(fastaFile, dna=False):
    seqs = 0
    try:
        for record in SeqIO.parse(open(fastaFile), "fasta"):
            lcs = Counter(record.seq.upper())
            if dna==True and sum([lcs["A"],lcs["T"],lcs["C"],lcs["G"],lcs["N"]])!=len(record.seq):
                raise FileFormatException("Illegal character found in " + fastaFile + " with sequence id: " + record.id)
            seqs += 1
    except ValueError as e:
        raise FileFormatException(e)
    if seqs == 0:
        raise FileFormatException(fastaFile + " contains no sequences...")