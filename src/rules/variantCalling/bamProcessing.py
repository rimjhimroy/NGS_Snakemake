"""
@attention: untested

"""

rule samToBam:
    input: "{sample}.sam"
    output: "{sample}.bam"
    shell: "samtools view -bS {input[0]} > {output[0]}"
    
rule indexBam:
    input: "sorted.{sample}.bam"
    output: "{sample}.bam.idx"
    shell: "samtools index {input[0]}"
    
rule sortBam:
    input: "{sample}.bam"
    output: "sorted.{sample}.bam"
    shell: "samtools sort -o {input[0]} {output[0]} > {output[0]}"
    
rule addHeaderline:
    input: "{sample}.bam"
    params: 
        path=CONFIG["picardTools"]["path"]
        sequencer=CONFIG["libraries"][wildcards.sample]["sequencingPlatform"]
    output: "headered.{sample}.bam"
    shell: "java -jar {params.path}/AddOrReplaceReadGroups.jar I={input[0] VALIDATION_STRINGENCY=SILENT O={output[0]} LB={wildcards.sample} PL={params.sequencer} PU=lane SM={wildcards.sample}"
    
rule removeDuplicates:
    input: "{sample}.bam"
    output: "noDup.{sample}.bam"  
    params: 
        path=CONFIG["picardTools"]["path"]
    shell: "java -jar {params.path}/MarkDuplicates.jar INPUT={input[0]} VALIDATION_STRINGENCY=SILENT OUTPUT={output[0]} REMOVE_DUPLICATES=true METRICS_FILE=/dev/null"
    
rule addMdTag:
    input: 
        bam="{sample}.bam"
        reference=CONFIG["mapping"]["referenceGenome"]
    output: "md.{sample}.bam"
    shell: "samtools calmd {input.bam} {input.reference} > {output]0]}"