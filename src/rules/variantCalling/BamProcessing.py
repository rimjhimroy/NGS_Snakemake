"""
@version:0.1
@author: Jetse

The BamProcessing module contains all rules for manipulating bam files.

A configuration file like the following is expected in a global CONFIG variable:
{
    "mapping":{
        "referenceGenome":"/path/to/referenceGenome.fasta
    }
    "options":{
        "picardTools":{
            "path":"/path/to/picardtools"
        }
    }
}
"""

rule samToBam:
    input: "mapped/{sample}.sam"
    output: "mapped/{sample}.bam"
    shell: "samtools view -bS {input[0]} > {output[0]}"
     
rule indexBam:
    input: "mapped/sorted.{sample}.bam"
    output: "mapped/{sample}.bam.idx"
    shell: "samtools index {input[0]}"
     
rule sortBam:
    input: "mapped/{sample}.bam"
    output: "mapped/sorted.{sample}.bam"
    shell: "samtools sort -o {input[0]} {output[0]} > {output[0]}"
    
rule addHeaderline:
    input: "mapped/{sample}.bam"
    params: 
        path=CONFIG["options"]["picardTools"]["path"]
    output: "mapped/headered.{sample}.bam"
    shell: "java -jar {params.path}/AddOrReplaceReadGroups.jar I={input[0]} VALIDATION_STRINGENCY=SILENT O={output[0]} LB={wildcards.sample} PL=illumina PU=lane SM={wildcards.sample}"
    
rule removeDuplicates:
    input: "mapped/{sample}.bam"
    output: "mapped/noDup.{sample}.bam"  
    params: 
        path=CONFIG["options"]["picardTools"]["path"]
    shell: "java -jar {params.path}/MarkDuplicates.jar INPUT={input[0]} VALIDATION_STRINGENCY=SILENT OUTPUT={output[0]} REMOVE_DUPLICATES=true METRICS_FILE=/dev/null"
     
rule addMdTag:
    input: 
        bam="mapped/{sample}.bam",
        reference=CONFIG["mapping"]["referenceGenome"]
    output: "mapped/md.{sample}.bam"
    shell: "samtools calmd {input.bam} {input.reference} > {output[0]}"