Variant calling
===============
The variant calling pipeline involves mapping against a reference genome, a multisampled vcf calling and phasing with BEAGLE.

Suffixes
--------
The most important prefixes and suffixes are listed below, more suffixes are used but these are especially for local
conversions...
* Mapping:
	* mapped/bowtie2.{sample}.sam - a mapped sample against a reference genome with bowtie2.
	* mapped/bwa.{sample}.sam - a mapped sample against a reference genome with bwa 
	(not implemented yet).
	* mapped/tophat.{sample}.sam - a mapped sample against a reference genome with tophat.
	(not implemented yet).
* BamProcessing:
	* {sample}.bam - a sam file converted to bam format
	* sorted.{sample}.bam - a sorted bam file
	* {sample}.bam.idx - an indexed bam file
	* headered.{sample}.bam - a bam file with an extra headerline
	* noDup.{sample}.bam - a bam file without duplicates
	* md.{sample}.bam - a bam file with an md tag in each record
* SnpCaller:
	* variantCalling/samtoolsMpileupSnps.vcf - vcf file with SNPs called with samtools mpileup
* Haplotyper:
	* phased.{prefix}.vcf - A phased vcf file, phased with BEAGLE
	
Configuration
-------------
The configuration file is a JSON file which is parsed in a workflow to the variabel CONFIG. The required configuration file has the following structure:
**Mapping**

	