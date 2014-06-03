"""
@attention: untested

"""
rule faidX:
    input: "{prefix}.fasta"
    output: "{prefix}.fasta.fai"
    shell: "samtools faidx {input[0]}"
    
rule bowtieIndex:
    input: inFile = "{ref}.fasta"
    output: outFile = "{ref}.fasta.1.bt2"
    shell: "bowtie2-build {input.inFile} {input.inFile}"