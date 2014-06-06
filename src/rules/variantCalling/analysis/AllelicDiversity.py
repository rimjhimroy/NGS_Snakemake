"""

"""

###############
##  Imports  ##
###############
from rules.variantCalling.analysis import Readers 
from rules.variantCalling.analysis.model import Contig
import csv

#################
##  Functions  ##
#################
#TODO: used more often create generic function in functions...
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

#############
##  Rules  ##
#############
rule allelicDiversityPerChrom:
    input: "variantCalling/snps.{chrom}_phased.snps.{prefix}.vcf"
    output: "variantCalling/phased.{chrom}_{prefix}.allelicDiversity.csv"
    params:
        gffFile = CONFIG["gffFile"]
    run:
        AllelicDiversity().getAllelicDiversity(input[0], wildcards.chrom, output[0], params.gffFile)

rule mergeCsv:
    input: 
        index = CONFIG["mapping"]["referenceGenome"] + ".fai",
        chroms = expand("variantCalling/phased.{chrom}_{{prefix}}.allelicDiversity.csv",chrom=getChromosomes(CONFIG["mapping"]["referenceGenome"] + ".fai"))
    output: "variantCalling/all.phased.{prefix}.allelicDiversity.csv"
    shell: "cat {input.chroms} > {output[0]}"



###############
##  Classes  ##
###############
class AllelicDiversity():
    """
    The class AllelicDiversity calculates the allelic diversity of a given vcf file with a single chromosome.
    """
    def _getAllHaplotypesByAccession(self, contigs):
        """The method getAllHaplotypesByAccession retrieves creates a dictionary with the accession as key and the haplotype as value
        
        :param contigs: The contigs to get the haplotypes from
        :type contigs: an list of :py:class:`Contig.Contig` instances
        
        """
        allHaplotypes = {}
        for key in contigs:
            haplotypes = {}
            if len(contigs[key].snps) > 0:
                for haplotype,accessions in contigs[key].haplotypes.items():
                    for accession in accessions:
                        if accession in haplotypes:
                            haplotypes[accession].append(haplotype)   
                        else:
                            haplotypes[accession] = [haplotype]
                allHaplotypes[key] = haplotypes
                
        return allHaplotypes
    
    def _parseFiles(self, chrom, gffFile, vcfFile):
        """
        The method parseFiles creates the reader objects to parse all files.
        
        :param chrom: The chromosome to parse
        :type chrom: str
        """
        gffReader = Readers.GffReader(chrom=chrom)
        gffReader.readFile(gffFile)
        allContigs = gffReader.contigs
        if len(allContigs) == 0:
            raise IndexError()
        vcfReader = Readers.VcfReader(allContigs.values())
        vcfReader.readFile(vcfFile)
        return allContigs
        
    def getAllelicDiversity(self, vcfFile, chrom, outputFile, gffFile):
        """
        The method getAllelicDiversity calculates the allelic diversity and writes the output to a file.
        
        """
        print("calculating allelic diversity of " + vcfFile)
        try:
            allContigs = self._parseFiles(chrom, gffFile, vcfFile)
            haplotypes = self._getAllHaplotypesByAccession(allContigs)
            accessions = list(list(haplotypes.values())[0].keys())
            with open(outputFile, "w") as outWriter:
                outWriter.write("contig\toriginal\t")
                for accession in accessions: outWriter.write( accession + "_1\t" + accession + "_2\t")
                outWriter.write("\n")
                for contigId in allContigs:
                    outWriter.write(contigId + "\t")
                    try:
                        outWriter.write(allContigs[contigId].refHaplotype + "\t")
                    except AttributeError: outWriter.write("-\t")
                    for accession in accessions:
                        for i in range(2):
                            if contigId in haplotypes:
                                outWriter.write(haplotypes[contigId][accession][i] + "\t")
                            else:
                                outWriter.write("-\t")
                    outWriter.write("\n")
        except IndexError:
            open(outputFile, "w").close()
            print("WARNING: No SNPs within contigs found in " + vcfFile)
