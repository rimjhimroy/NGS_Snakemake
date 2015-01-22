###############
##  Classes  ##
###############
class LociFinder(object):
    """
    The class LociFinder combines the gff file with the vcf file and the phenotype file. All differen t haplotypes
    per gene are reconstructed (only on positions where at least one sample has a SNP). In the end for each gene
    a p-value is calculated with the t-test to indicate the chance of being involved in a phenotype. If multiple
    phenotypes are described in the phenotype file, the chance of each phenotype will be calculated independent.
    """
    def findLoci(self, vcfFile, chrom, phenotypeFile, gffFile, outputFile):
        """
        findLoci is the main method of the calculation of which genes are involved in a phenotype. First the phenotype
        file is read, then for each phenotype the gff file is read and haplotypes are constructed from the vcf files.
        After this a method is called to calculate the chance of being involved in a phenotype. In the end each chance is
        written to a csv file with one p-value for each gene.
        """
        phenReader = Readers.PhenotypeReader()
        phenReader.readFile(phenotypeFile)
        for phenotype in  phenReader.phenotypes:
            gffReader = Readers.GffReader(chrom=chrom)
            gffReader.readFile(gffFile)
            phenotype.contigs = gffReader.contigs

            vcfReader = Readers.VcfReader(phenotype.contigs.values())
            vcfReader.readFile(vcfFile)

            pVals = self.findLociInPheno(phenotype)
            self.writePvaluesToFile(pVals, outputFile)

    def writePvaluesToFile(self, pVals, outFile):
        """
        This method writes a dictionary of p-values to a given file
        """
        with open(outFile, "w") as outWriter:
            for (contig, pVal) in pVals.items():
                outWriter.write(contig + "\t" + str(pVal[1]) + "\n")

    def findLociInPheno(self, phenotype):
        """
        This method creates the output needed for the f_oneway test of the scipy module, and executes this method.
        """
        numpy.seterr(all="raise")
        pValues = {}
        for contig in phenotype.contigs:
            if len(phenotype.contigs[contig].haplotypes) == 0:
                pValues[contig] = ["",1.0]
                continue
            accessions = {}
            for accession in phenotype.alleles.keys():
                for (haplotype,contigAccessions) in phenotype.contigs[contig].haplotypes.items():
                    for contigAccession in contigAccessions:
                        if haplotype in accessions:
                                accessions[haplotype].append(float(phenotype.alleles[accession]))
                        else:
                                accessions[haplotype] = [float(phenotype.alleles[accession])]
            try:
                pValues[contig] = stats.f_oneway(*[item for sublist in accessions.values() for item in sublist])
            except Exception as err:
                pValues[contig] = ["",1.0]
        return pValues