"""
@version: 0
@author: Jetse

Quality control:
* Checked whether biopython can parse the full fastq file
* Checked whether the reads only contain A,T,C,G or N characters
* Checked whether the file contains at least a single read
* If paired end, the number of reads will be compared, 
the forward file has to contain the same numer of reads as the reversed.
"""
from qualityControl import QualityControlExceptions
from collections import Counter
from Bio import SeqIO
import os

class FastqFile:
    
    def __init__(self, forwardReads, reversedReads=None):
        self.forwardReads = forwardReads
        self.reversedReads = reversedReads
    
    def isValid(self, dna=False):
        print("Checking: " + self.forwardReads)
        forwardRecords = self._contentControl(self.forwardReads, dna)
        print("Correct! File contains {} reads".format(forwardRecords))
        if self.reversedReads != None:
            print("Checking: " + self.reversedReads)
            reversedRecords = self._contentControl(self.reversedReads, dna)
            print("Correct! File contains {} reads".format(reversedRecords))
            if forwardRecords != reversedRecords:
                raise QualityControlExceptions.FileFormatException("Forward file has not the same number of sequences as the reversed file when comparing " + self.forwardReads + " with " + self.reversedReads)
            print("Paired end is correct!")
        
    def _contentControl(self, fastqFile, dna=False):
        noOfRecords = 0
        try:
            for record in SeqIO.parse(open(fastqFile), "fastq"):
                lcs = Counter(record.seq.upper())
                if dna == True and sum([lcs["A"],lcs["T"],lcs["C"],lcs["G"],lcs["N"]])!=len(record.seq):
                    raise QualityControlExceptions.FileFormatException("Illegal character found in " + fastqFile + " with sequence id: " + record.id)
                if max(record.letter_annotations["phred_quality"]) > 72 or min(record.letter_annotations["phred_quality"]) < 0:
                    raise QualityControlExceptions.FileFormatException("Invalid quality score in " + fastqFile + " with sequence id: " + record.id)
                noOfRecords += 1
        except ValueError as e:
            raise QualityControlExceptions.FileFormatException(e)
        if noOfRecords == 0:
            raise QualityControlExceptions.FileFormatException(fastqFile + " contains no sequences...")
        return noOfRecords
    
    def calculateStatistics(self):
        self.fastqInfo = {}
        self.forwardInfo = self.getFastqInfo(self.forwardReads)
        if self.reversedReads != None:
            self.reversedInfo = self.getFastqInfo(self.reversedReads)
            
    def getFastqInfo(self, fastqFile):
        """
        The method getFastqInfo counts the number of reads, bases and high quality reads and writes these to a summary file.
        If this summary file already exists, this file is used instead of counting the reads/bases again.
        """
        summaryFile = fastqFile + ".summary"
        if os.path.exists(summaryFile):
            self.info = self.getFastqInfoFromSummary(summaryFile)
            return self.info
        totalLength = 0
        totalReads = 0
        totalHighq = 0
        for record in SeqIO.parse(open(fastqFile), "fastq"):
            seqLength = len(record.seq)
            totalReads += 1
            totalLength += seqLength
            for qual in record.letter_annotations["phred_quality"]:
                if qual > 30:
                    totalHighq +=1
        self.info = ["{:,}".format(totalLength), "{:,}".format(totalReads), str(totalLength/totalReads),str(int(round(totalHighq/float(totalLength)*100)))]
        with open(summaryFile, "w") as summaryWriter:
            summaryWriter.write("\t".join(self.info))
        return self.info
    
    def getFastqInfoFromSummary(self, summaryFile):
        """
        This method reads the summary file and returns the content
        """
        with open(summaryFile) as summaryReader:
            for line in summaryReader:
                return line.split("\t")
            
    def __str__(self):
        if hasattr(self, "info") == False:
            try:
                self.info = self.getFastqInfo(self.forwardReads)
            except ZeroDivisionError:
                return "An empty fastq file..."
        return ("Total basepairs: {}\n"
                "Total reads: {}\n"
                "Avg read length: {}\n"
                "Percentage good quality {}%").format(self.info[0],self.info[1],self.info[2],self.info[3])