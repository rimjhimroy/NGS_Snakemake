"""
@attention: untested

"""
rule faidX:
    input: "{prefix}.fasta"
    output: "{prefix}.fasta.fai"
    shell: "samtools faidx {input[0]}"