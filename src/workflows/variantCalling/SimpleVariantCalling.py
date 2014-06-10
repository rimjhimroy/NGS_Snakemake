"""
@author: Jetse

"""
import json, os, sys
 
with open("config.json") as f:
    CONFIG = json.load(f)

# Variant calling:
include: os.path.dirname(sys.argv[2])+"/../../rules/mappers/Bowtie.py"
include: os.path.dirname(sys.argv[2])+"/../../rules/mappers/BamProcessing.py"
 
include: os.path.dirname(sys.argv[2])+"/../../rules/variantCalling/SnpCallers.py"


rule all:
    input: "variantCalling/samtoolsMpileupSnps.vcf"