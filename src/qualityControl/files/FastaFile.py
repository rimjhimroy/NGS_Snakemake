"""
@version: 0.1
@author: Jetse
"""
from Bio import SeqIO
from collections import Counter
from qualityControl import QualityControlExceptions

class FastaFile:    
    def __init__(self, fastaFile):
        self.fastaFile = fastaFile
        
    def isValid(self, dna=False):
        """
        Quality control:
        * Checked whether biopython can parse the full fasta file
        * Checked whether the reads only contain A,T,C,G or N characters (if DNA)
        * Checked whether the file contains at least a single sequence
        """
        seqs = 0
        try:
            for record in SeqIO.parse(open(self.fastaFile), "fasta"):
                lcs = Counter(record.seq.upper())
                if dna==True and sum([lcs["A"],lcs["T"],lcs["C"],lcs["G"],lcs["N"]])!=len(record.seq):
                    raise QualityControlExceptions.FileFormatException("Illegal character found in " + self.fastaFile + " with sequence id: " + record.id)
                seqs += 1
        except ValueError as e:
            raise QualityControlExceptions.FileFormatException(e)
        if seqs == 0:
            raise QualityControlExceptions.FileFormatException(self.fastaFile + " contains no sequences...")
        
    def getFastaStats(self):
        """
        This method calculates the base statistics which consist of the following statistics:
        * total number of sequences
        * total length
        * GC percentage
        * longest sequence
        * N50
        * N90
        """
        [contigLengths, totalLength] = self.getContigsLengths(self.fastaFile)
        [n50Index, n50] = self.calculateN(50, contigLengths, totalLength)
        [n90Index, n90] = self.calculateN(90, contigLengths, totalLength)
         
        self.totalSeqs = len(contigLengths)
        self.totalLen = totalLength
        self.gcPerc = self.gcNo/float(totalLength)*100
        self.longestSeq = contigLengths[0]
        self.n50 = n50
        self.n50Index = n50Index
        self.n90 = n90
        self.n90Index = n90Index
        
    def getContigsLengths(self, fastaFile):
        """
        The lengths of the contigs are calculated with the biopython library. In the end all contigs are sorted on length.
        """
        contigLengths = []
        totalLength = 0
        self.gcNo = 0
        for contig in SeqIO.parse(open(fastaFile), "fasta"):
            self.gcNo = self.gcNo + sum(map(contig.seq.count, ['G', 'C', 'g', 'c']))
            contigLenght = len(contig.seq)
            totalLength += contigLenght
            contigLengths.append(contigLenght)
        
        contigLengths.sort()
        contigLengths.reverse()
        return [contigLengths, totalLength]
    
    def calculateN(self, n, contigLengths, totalLength):
        """
        The method calculateN calculates the N50, N90 or any other N.
        The N50 is defined as
        "Given a set of sequences of varying lengths, the N50 length is defined as the length N for which 50% of all bases in the sequences are in a sequence of length L < N."
        """
        lengthTillNow = 0
        indexTillNow = 0
        toThisLength = totalLength * n / 100
        for contigLen in contigLengths:
            lengthTillNow += contigLen
            indexTillNow = indexTillNow + 1
            if toThisLength < lengthTillNow:
                return [indexTillNow,contigLen]
    
    def __str__(self):
        if hasattr(self, "totalSeqs") == False:
            try:
                self.getFastaStats()
            except:
                return("An empty fasta file...")
        return ("Total sequences: {}\n"
        "Total length: {} bp\n"
        "GC percentage: {}%\n"
        "Longest sequence: {} bp\n"
        "N50 index: {}, length: {} bp\n"
        "N90 index: {}, length: {} bp").format(
                                        self.totalSeqs,
                                        self.totalLen,
                                        self.gcPerc,
                                        self.longestSeq,
                                        self.n50Index, self.n50,
                                        self.n90Index, self.n90)