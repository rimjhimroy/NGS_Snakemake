"""

"""
import json, os, sys
 
with open("config.json") as f:
    CONFIG = json.load(f)

#Fastq preprocessing:
# include: os.path.dirname(sys.argv[2])+"/../../rules/fastqProcessing/Trimmomatic.py"
# include: os.path.dirname(sys.argv[2])+"/../../rules/fastqProcessing/SeqPrep.py"
# include: os.path.dirname(sys.argv[2])+"/../../rules/fastqProcessing/Quake.py"
# include: os.path.dirname(sys.argv[2])+"/../../rules/fastqProcessing/FastqMcf.py"
# include: os.path.dirname(sys.argv[2])+"/../../rules/fastqProcessing/ContaminationFiltering.py"

#Variant calling:
# include: os.path.dirname(sys.argv[2])+"/../../rules/mappers/Bowtie.py"
# include: os.path.dirname(sys.argv[2])+"/../../rules/mappers/BamProcessing.py"
# 
# include: os.path.dirname(sys.argv[2])+"/../../rules/variantCalling/SnpCallers.py"
# 
include: os.path.dirname(sys.argv[2])+"/../../rules/variantCalling/Haplotyper.py"

#Indexing:
include: os.path.dirname(sys.argv[2])+"/../../rules/functions/Indexing.py"

#Analysis
include: os.path.dirname(sys.argv[2])+"/../../rules/variantCalling/analysis/AllelicDiversity.py"

rule all:
#     input: "variantCalling/phased.snps.samtoolsMpileupSnps.vcf"
    input: "variantCalling/all.phased.samtoolsMpileupSnps.allelicDiversity.csv"