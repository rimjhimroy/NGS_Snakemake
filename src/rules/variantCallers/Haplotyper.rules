"""
@version: 0.1
@author: Jetse
@attention: Haplotyping fails when there is a single chromosome without SNPs!

The minimum JSON for executing the Haplotyping:
{
    "options":{
        "java":{
            "memUsage":"-Xmx30g"
        },
        "beagle":{
            "path":"/path/to/beagle.jar"
        },
        "gatk":{
            "path":"/path/to/gatk.jar"
        },
        "picardTools":{
            "path":"/path/to/pacardTools"
        }
    },
    "mapping":{
        "referenceGenome":"/path/to/referenceGenome.fasta"
    }
}
"""
import csv, os

def getChromosomes(faiIndex):
    """
    The method getChromosomes retrieves the chromosomes of a fai indexed reference file
    """
    chromosomes = []
    with open(faiIndex) as indexFile:
        indexReader = csv.reader(indexFile, delimiter="\t")
        for line in indexReader:
            chromosomes.append(line[0])
    return chromosomes

rule extractChrom:
    input: 
        vcf="variantCalling/{prefix}.vcf.bgz",
        index="variantCalling/{prefix}.vcf.bgz.tbi"
    output: "variantCalling/snps.{chrom}_{prefix}.vcf"
    shell: "tabix -h -p vcf {input.vcf} {wildcards.chrom} > {output[0]}"
    
rule bgzipCompress:
    input: "variantCalling/{prefix}.vcf"
    output: "variantCalling/{prefix}.vcf.bgz"
    shell: "bgzip -c {input[0]} > {output[0]}"

rule tabixIndex:
    input: "variantCalling/{prefix}.vcf.bgz"
    output: "variantCalling/{prefix}.vcf.bgz.tbi"
    shell: "tabix -h -p vcf {input[0]}"

rule prepareBeagle:
    input: 
        vcf = "variantCalling/snps.{chrom}_{prefix}.vcf"
    output: "variantCalling/{chrom}_{prefix}.BEAGLE.PL"
    shell: "vcftools --vcf {input.vcf} --chr {wildcards.chrom} --out variantCalling/{wildcards.chrom}_{wildcards.prefix} --BEAGLE-PL"
 
rule beagle:
    input: "variantCalling/{chrom}_{prefix}.BEAGLE.PL"
    output:
        dose = "variantCalling/beagle.{chrom}_{prefix}.BEAGLE.PL.dose.gz",
        gprobs = "variantCalling/beagle.{chrom}_{prefix}.BEAGLE.PL.gprobs.gz",
        phased = "variantCalling/beagle.{chrom}_{prefix}.BEAGLE.PL.phased.gz",
        rTwo = "variantCalling/beagle.{chrom}_{prefix}.BEAGLE.PL.r2"
    params: 
        maxMem = CONFIG["options"]["java"]["memUsage"],
        path = CONFIG["options"]["beagle"]["path"]
    shell: "java -jar {params.maxMem} {params.path} like={input[0]} out=variantCalling/beagle"

rule beagleExtractDose:
    input: "variantCalling/beagle.{chrom}_{prefix}.BEAGLE.PL.dose.gz"
    output: "variantCalling/beagle.{chrom}_{prefix}.BEAGLE.PL.dose"
    shell: "gunzip {input[0]}"
 
rule beagleExtractGprobs:
    input: "variantCalling/beagle.{chrom}_{prefix}.BEAGLE.PL.gprobs.gz"
    output: "variantCalling/beagle.{chrom}_{prefix}.BEAGLE.PL.gprobs"
    shell: "gunzip {input[0]}"
    
rule beagleExtractPhased:
    input: "variantCalling/beagle.{chrom}_{prefix}.BEAGLE.PL.phased.gz"
    output: "variantCalling/beagle.{chrom}_{prefix}.BEAGLE.PL.phased"
    shell: "gunzip {input[0]}" 
    
rule beagleOutputToVcf:
    input: 
        vcf="variantCalling/snps.{chrom}_{prefix}.vcf",
        dose = "variantCalling/beagle.{chrom}_{prefix}.BEAGLE.PL.dose",
        gprobs = "variantCalling/beagle.{chrom}_{prefix}.BEAGLE.PL.gprobs",
        phased = "variantCalling/beagle.{chrom}_{prefix}.BEAGLE.PL.phased",
        rTwo = "variantCalling/beagle.{chrom}_{prefix}.BEAGLE.PL.r2",
        refGenome = CONFIG["mapping"]["referenceGenome"],
        refGenomeIndex = os.path.splitext(CONFIG["mapping"]["referenceGenome"])[0] + ".dict"
    output: "variantCalling/phased.{chrom}_{prefix}.vcf"
    params:
        maxMem = CONFIG["options"]["java"]["memUsage"],
        path = CONFIG["options"]["gatk"]["path"]
    shell: "java -jar {params.maxMem} {params.path} -R {input.refGenome} -T BeagleOutputToVCF -V {input.vcf} "
        "-beagleR2:BEAGLE {input.rTwo} "
        " -beaglePhased:BEAGLE {input.phased}"
        " -beagleProbs:BEAGLE {input.gprobs}"
        " -o {output[0]}"
        " --unsafe LENIENT_VCF_PROCESSING"

rule genomeDictIndex:
    input: "{prefix}.fasta"
    output: "{prefix}.dict"
    params:
        path = CONFIG["options"]["picardTools"]["path"]
    shell: "java -jar {params.path}/CreateSequenceDictionary.jar R={input[0]} O={output[0]}"
     
rule mergePhasedVcf:
    input: 
        index = CONFIG["mapping"]["referenceGenome"] + ".fai",
        chroms = expand("variantCalling/phased.{chrom}_{{prefix}}.vcf",chrom=getChromosomes(CONFIG["mapping"]["referenceGenome"] + ".fai"))
    output: "variantCalling/phased.snps.{prefix}.vcf"
    shell: "vcf-concat {input.chroms} > {output[0]}"
#             
#     
