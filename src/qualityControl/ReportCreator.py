"""

"""

import subprocess, os
from qualityControl.files import FastaFile, FastqFile, VcfFile, BamFile, OtherFile

def printFileInfo(fileName):
    suffix = os.path.splitext(fileName)[1]
    if suffix == ".fasta":
        file = FastaFile.FastaFile(fileName)
    elif suffix == ".fastq":
        file = FastqFile.FastqFile(fileName)
    elif suffix == ".vcf":
        file = VcfFile.VcfFile(fileName)
    elif suffix == ".bam":
        file = BamFile.BamFile(fileName)
    else:
        file = OtherFile.OtherFile(fileName)
    print(file)

proc = subprocess.Popen("snakemake --snakefile ~/pythonCodebase/snakemakeLocal/src/workflows/bestPractice/preprocessing.py --summary",shell=True, stdout=subprocess.PIPE)
out = proc.communicate()[0]
lines = out.decode("utf-8").split("\n")
for line in lines:
    info = line.split("\t")
    if info[0] == "file" or not line.strip():
        continue
    print("File *{}* after rule *{}*".format(info[0],"unknown" if info[2]=="-" else info[2]))
    print("-"*20)
    if info[4] == "missing":
        print("Removed, statistics can not be calculated anymore")
    else:
        printFileInfo(info[0])
        
    print("\n")