'''
Created on Jun 5, 2014

@author: VLPB
'''
from Bio import SeqIO
import subprocess, os
 
class FastaFile:    
    def __init__(self, fastaFile):
        self.fastaFile = fastaFile
        
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

proc = subprocess.Popen("snakemake --snakefile ~/pythonCodebase/snakemakeLocal/src/workflows/bestPractice/preprocessing.py --summary",shell=True, stdout=subprocess.PIPE)
out = proc.communicate()[0]
lines = out.decode("utf-8").split("\n")
for line in lines:
    info = line.split("\t")
    if info[0] == "file" or not line.strip():
        continue
    print("File *{}* after rule *{}*".format(info[0],"unknown" if info[2]=="-" else info[2]))
    print("-"*20)
    suffix = os.path.splitext(info[0])[1]
    if info[4] == "missing":
        print("Removed, statistics can not be calculated anymore")
    elif suffix == ".fasta":
        faFile = FastaFile(info[0])
        faFile.getFastaStats()
        print(faFile)
    elif suffix == ".fastq":
        print("reads!")
    else:
        print("an {} file of size {} bytes".format(suffix[1:],os.path.getsize(info[0])))
    print("\n")