"""

"""
import json, os, sys
 
with open("config.json") as f:
    CONFIG = json.load(f)

#Fastq preprocessing:
include: os.path.dirname(sys.argv[2])+"/../../rules/fastqProcessing/Trimming.py"
 
include: os.path.dirname(sys.argv[2])+"/../../rules/fastqProcessing/ContaminationFiltering.py"

include: os.path.dirname(sys.argv[2])+"/../../rules/fastqProcessing/Merging.py"

include: os.path.dirname(sys.argv[2])+"/../../rules/fastqProcessing/KmerCorrection.py"

#Variant calling:
include: os.path.dirname(sys.argv[2])+"/../../rules/variantCalling/Mappers.py"

include: os.path.dirname(sys.argv[2])+"/../../rules/variantCalling/BamProcessing.py"

# include: os.path.dirname(sys.argv[2])+"/../../rules/variantCalling/SnpCallers.py"

include: os.path.dirname(sys.argv[2])+"/../../rules/variantCalling/Haplotyper.py"

#Indexing:
include: os.path.dirname(sys.argv[2])+"/../../rules/functions/Indexing.py"

rule all:
    input: "variantCalling/phased.snps.samtoolsMpileupSnps.vcf"