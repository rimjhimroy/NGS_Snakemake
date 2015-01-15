The assemblers package
====================
The assemblers package contains all the rules for each implemented assembler and scaffolder.

Wgs
------
> Celera Assembler is a de novo whole-genome shotgun (WGS) DNA sequence assembler. 
It reconstructs long sequences of genomic DNA from fragmentary data produced by whole-genome shotgun sequencing. 
Celera Assembler was developed at Celera Genomics starting in 1999. It was released to SourceForge in 2004 as the 
wgs-assembler under the GNU General Public License. The pipeline revised for 454 data was named CABOG.

Allpaths
--------
ALLPATHS-LG is a short read assembler and it works on both small and large (mammalian size) genomes. 
To use it, you should first generate ~100 base Illumina reads from two libraries: 
one with ~180 bp insert size (fragment data), and one with a ~3000 bp insert size (jumping library), both at about 45x coverage. 
Sequence from longer fragments will enable longer-range continuity.

Scarpa
------
> Scarpa is a stand-alone scaffolding tool for NGS data with paired end reads. It can be used together with virtually any genome assembler and any NGS read mapper 
that supports SAM format. Other features include support for multiple libraries and an option to estimate insert size distributions from data. 
Scarpa is available free of charge for academic and commercial use under the GNU General Public License (GPL).