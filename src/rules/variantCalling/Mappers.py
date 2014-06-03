"""
@version: 0.1
@author: Jetse
@attention: When the bowtie index is not present, the program needs writing permissions 
in the directory of the reference genome
TODO: implement BWA
TODO: implement Tophat for RNA
TODO test bowtieSingle

{
    "mapping":{
        "reads":{
            "sampleName":[/path/to/forward.fastq,/path/to/reversed.fastq]
            "anotherSample":[/path/to/singleEndReads.fastq]
        },
        "referenceGenome":"/path/to/reference"
    }
}
"""
################
##  Bowtie 2  ##
################
ruleorder: bowtiePaired > bowtieSingle

rule bowtiePaired:
    input: 
        forward = lambda wildcards: CONFIG["mapping"]["reads"][wildcards.sample][0],
        reversed = lambda wildcards: CONFIG["mapping"]["reads"][wildcards.sample][1],
        reference = CONFIG["mapping"]["referenceGenome"],
        index = CONFIG["mapping"]["referenceGenome"] + ".1.bt2"
    threads: 999
    output: "mapped/bowtie2.{sample}.sam"
    shell: "bowtie2 -p {threads} -x {input.reference} -1 {input.forward} -2 {input.reversed} -S {output[0]}"

rule bowtieSingle:
    input:
        reads = lambda wildcards: CONFIG["mapping"]["reads"][wildcards.sample][0],
        reference = CONFIG["mapping"]["referenceGenome"],
        index = CONFIG["mapping"]["referenceGenome"] + ".1.bt2"
    output: "mapped/{sample}.sam"
    threads: 999
    shell: "bowtie2 -p {threads} -x {input.reference} -U {input.reads} -S {output[0]}"
    
###########
##  BWA  ##
###########


##############
##  Tophat  ##
##############
