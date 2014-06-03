"""
@author: jetse
@version: 0.1
"""
rule samtoolsMpileup:
    input: 
        reads=CONFIG["options"]["mpileup"]["input"],
        reference=CONFIG["mapping"]["referenceGenome"]
    output: "variantCalling/samtoolsMpileupSnps.mpileup"
    shell: "samtools mpileup -g -f {input.reference} {input.reads} > {output[0]}"
    
rule bcftoolsView:
    input: "variantCalling/{prefix}.mpileup"
    output: "variantCalling/{prefix}.vcf"
    shell: "bcftools view -vcg {input[0]} > {output[0]}"

rule filterVcf:
    input: "{prefix}.vcf"
    output: "variantCalling/filtered.{prefix}.vcf"
    params: 
        path=CONFIG["options"]["vcfUtils"]["path"],
        optionalOpts=CONFIG["options"]["vcfUtils"]["optionalOpts"]
    shell: "perl {params.path} varFilter {params.optionalOpts} {input[0]} > {output[0]}"