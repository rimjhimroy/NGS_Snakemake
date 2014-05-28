"""
@attention: When the bowtie index is not present, the program needs writing permissions 
in the directory of the reference genome
TODO: implement BWA
TODO: implement Tophat for RNA
"""
################
##  Bowtie 2  ##
################
rule bowtiePaired:
    input: 
        forward: "preprocessing/{sample}_1.fastq",
        reversed: "preprocessing/{sample}_2.fastq",
        reference: CONFIG["mapping"]["referenceGenome"],
        index: CONFIG["mapping"]["referenceGenome"] + ".1.bt2"
    output: "bowtie2.{sample}.sam"
    shell: "bowtie2 -x {input.reference} -1 {input.forward} -2 {input.reversed} -S {output[0]}"

rule bowtieSingle:
    input:
        reads: "preprocessing/{sample}.fastq",
        reference: CONFIG["mapping"]["referenceGenome"],
        index: CONFIG["mapping"]["referenceGenome"] + ".1.bt2"
    output: "{sample}.sam"
    shell: "bowtie2 -x {input.reference} -U {input.raeds} -S {output[0]}"

rule bowtieIndex:
    input: "{prefix}.fasta"
    output: "{prefix}.1.bt2"
    shell: "bowtie2-build {input[0]} {input[0]}"
    
###########
##  BWA  ##
###########


##############
##  Tophat  ##
##############
