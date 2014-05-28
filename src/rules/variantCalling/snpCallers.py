'''
Created on May 28, 2014

@author: jetse
'''
rule samtoolsMpileup:
    input: CONFIG["options"]["mpileup"]["input"]
    output: "variantCalling/allSnps.vcf"
    shell: "echo \"not implemented yet...\""