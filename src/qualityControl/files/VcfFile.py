"""
@version 0
@author: Jetse

Quality control:
* Checked whether each column contains at least 8 columns
* Checked whether file contains at least a single SNP
"""

from qualityControl import QualityControlExceptions

class VcfFile:
    
    def __init__(self, fileName, bcf=False):
        self.fileName = fileName
        self.bcf = bcf
        
    def isValid(self):
        print("Checking: " + self.fileName)
        lineNo = 0
        snps = 0
        with open(self.fileName) as vcfReader:
            lineNo += 1
            for line in vcfReader:
                if line.startswith("#"):
                    continue
                elif line.isspace():
                    continue
                snps += 1
                columns = line.split()
                if len(columns) < 8:
                    raise QualityControlExceptions.FileFormatException("Too less columns in line {}, at least 8 expected, {} found".format(lineNo, len(columns)))
        if snps == 0:
            raise QualityControlExceptions.FileFormatException("No SNPs found in vcf file!")
        print("{} SNPs found in {}".format(snps,self.fileName))