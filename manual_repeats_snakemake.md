# Manual for the _de novo_ repeat finder pipeline

The pipeline for finding repeats is part of the larger VLPB Snakemake pipeline. The code and example data sets are found on the github repository: [https://github.com/VLPB/SnakeMakeVlpb](https://github.com/VLPB/SnakeMakeVlpb)

To get access to this repository, please sign up for github and contact the VLPB for access.

## Installation process

To run the VLPB pipeline, you need python version 3 and snakemake. The 'readme' in the root of the repository contains the most up to date installation process.

## Workflow set-up

Each workflow has the same structure for configuration and running. In the `paths.json` file, important paths need to be set. These paths are then used in `config.json`. This file contains the configuration for running the workflow, including download URLs, build options and locations of sample data files.

**Note:** although is it possible to run the workflows from the source directory, it is best to copy all files except the Snakemake file to a project folder. This way you can keep track of the particular settings you used for the project. And, also important, updating the repository from git is easier and fail-safe. You can run the workflow from the project directory through `snakemake -s [workflow snakemake]`

## Tool 1: TEDNA

TEDNA is a transposable element `de novo` assembler.

Paper: [http://bioinformatics.oxfordjournals.org/content/30/18/2656](http://bioinformatics.oxfordjournals.org/content/30/18/2656).

Tool website: [https://urgi.versailles.inra.fr/Tools/Tedna](https://urgi.versailles.inra.fr/Tools/Tedna)

Focus on: Transposable Elements

Type of repeats: all sorts of TEs

Description:

>Tedna is a lightweight _de novo_ transposable element assembler. It assembles the transposable elements directly from the raw reads.

TEDNA requires a **paired-end Illumina** data set. The files should end in **\_1.fastq** and **\_2.fastq**.

The workflow is located at: `./src/workflows/repeats/tedna`

To run, please edit `paths.json` and `config.json` first. In `config.json`, the samples are described in the _samples_ field. Additional tedna command line options are _tedna\_opts -&gt; cl\_options_. 

@TODO: fully describe all tedna command line options.

The important fields in config.json which you can edit are shown in green:

    "samples": {
            "Pleurotus_ostreatus": {
                "EP57": {
                    "readsets": {
                            "1": [
                                    "/media/sven/extData/sven/VLPB/raw_reads/ST_sample001_1.fastq",
                                    "/media/sven/extData/sven/VLPB/raw_reads/ST_sample001_2.fastq"
                                    ]    
                            },
                    "type": "pe",
                    "insertSize": "300",
                    "insertSizeStDev": "",
                    "platform": "illumina"
                }
            }
    },
    "tedna_opts": {
            "cl_options": " -k 61 -i 300 -t 10 "
    }


TEDNA can now be started by running `snakemake` in the workflow directory.

## Tool 2: DNAPipeTE

The DNAPipeTE tool is incorporated in the pipeline. However, a bug in the software makes it impossible to use it at this point. An issue has been opened on the DNAPipeTE repository.

Paper: [https://academic.oup.com/gbe/article/7/4/1192/533768](https://academic.oup.com/gbe/article/7/4/1192/533768)

Tool website: [https://lbbe.univ-lyon1.fr/-dnaPipeTE-?lang=en](https://lbbe.univ-lyon1.fr/-dnaPipeTE-?lang=en)

Focus on: Transposable elements

Types of repeats: all

Description:

> dnaPipeTE (for **d**e-**n**ovo **a**ssembly &amp; annotation **Pipe** line for **T**ransposable **E**lements), is a pipeline designed to find, annotate and quantify Transposable Elements in small samples of NGS datasets. It is very useful to quantify the proportion of TEs in newly sequenced genomes since it **does not require genome assembly** and works on **small datasets (< 1X per run)**.

## Tool 3: RepeatModeler

RepeatModeler scans DNA sequences for repeat motifs. It works only on (genome) assemblies, not on NGS read files.

Paper: NA

Tool website: [http://www.repeatmasker.org/RepeatModeler/](http://www.repeatmasker.org/RepeatModeler/)

Focus on: Repeats in genome assembly

Types of repeats: all

Description:

>RepeatModeler is a de-novo repeat family identification and modeling package. At the heart of RepeatModeler are two de-novo repeat finding programs ( RECON and RepeatScout ) which employ complementary computational methods for identifying repeat element boundaries and family relationships from sequence data. RepeatModeler assists in automating the runs of RECON and RepeatScout given a genomic database and uses the output to build, refine and classify consensus models of putative interspersed repeats.

The workflow is located in: `./src/workflows/repeats/modeler`

The workflow also installs blast+, rmblast, repeatmasker, repeatscout, trf and recon.

To run, please edit `paths.json` and `config.json` first. In `config.json`, these fields are important:


    "base":
        {
            "bashrc": "{base_dir}{executables}bashrc",
            "download_dir":"{download_dir}",
            "genome": "{base_dir}e.coli.fna",
            "rmlib" : "{base_dir}{databases}repeat_db.fasta",
            "cpus": "8"
        },


| **Field** | **Description**                                   |
| ---       | ---                                               |
| genome    | Location of the genome fasta file to be processed |
| rmlib     | Location of the output file                       |
| cpus      | Number of CPUs to use                             |

RepeatModeler can now be started by running `snakemake` in the workflow directory.

## Tool 4: ReAS

Paper: [https://academic.oup.com/bioinformatics/article/31/11/1827/2365472](https://academic.oup.com/bioinformatics/article/31/11/1827/2365472)

Tool website: ftp:// [ftp.genomics.org.cn/pub/ReAS/software/ReAS\_2.02.tar.gz](http://ftp.genomics.org.cn/pub/ReAS/software/ReAS_2.02.tar.gz)

Focus on: Transposable elements

Type of repeats: only TEs?

Description:

>We describe an algorithm, ReAS, to recover ancestral sequences for transposable elements (TEs) from the unassembled reads of a whole genome shotgun.

## Tool 5: Transposome

Transposome is a command line application to annotate transposable elements from paired-end whole genome shotgun data.

Paper: [https://academic.oup.com/bioinformatics/article/31/11/1827/2365472](https://academic.oup.com/bioinformatics/article/31/11/1827/2365472)

Tool website: [https://github.com/sestaton/Transposome](https://github.com/sestaton/Transposome)

Focus on: Transposable elements

Type of repeats: only TEs?

Description:

>Transposome is a command line application to annotate [transposable elements](http://en.wikipedia.org/wiki/Transposable_element) from paired-end whole genome shotgun data.

The workflow is located in: `./src/workflows/repeats/transposome`

To run, please edit `paths.json` and `config.json` first. In `config.json`, these fields are important:

    "base":
        {
         "seq_file": "/tmp/test.fa",
         "format": "fasta",
         "output": "{working_dir}transposome_output",
         "cpus":"8"
    }


| **Field** | **Description**                         |
| ---       | ---                                     |
| seq_file | Read file                                |
| format    | Format of the read file (fasta, fastq)  |
| output    | Output directory of transposome         |
| cpus      | Number of CPUs to use                   |

Transposome can now be started by running `snakemake` in the workflow directory. The complete list of options is described here: [https://github.com/sestaton/Transposome/wiki/Specifications-and-example-usage](https://github.com/sestaton/Transposome/wiki/Specifications-and-example-usage)

## Tool 6: RepeatMasker

RepeatMasker uses a repeat database to scan a genome for repeats. It requires two files: a repeat database fasta file and a genome fasta file. When you have several repeat files, you can use the command line tool `cat` to create one large fasta file: `cat myFile1.fa myFile2.fa > complete.fa`

Paper: NA

Tool website: [http://www.repeatmasker.org](http://www.repeatmasker.org)

Focus on: all repeats in genome assembly

Type of repeats: all

Description:

>RepeatMasker is a program that screens DNA sequences for interspersed repeats and low complexity DNA sequences. The output of the program is a detailed annotation of the repeats that are present in the query sequence as well as a modified version of the query sequence in which all the annotated repeats have been masked (default: replaced by Ns).

The workflow is located in: `./src/workflows/repeats/masker`

To run, please edit `paths.json` and `config.json` first. In `config.json`, these fields are important:

    "base":
        {
         "bashrc": "{base_dir}{executables}bashrc",
         "download_dir":"{download_dir}",
         "genome": "{base_dir}e.coli.fna",
         "rmlib" : "{base_dir}{databases}repeat_db.fasta",
         "cpus": "8",
         "output": "{base_dir}repeatmasker_out",
         "cl_options": " -gff -html "
        },


| **Field**   | **Description**                                         |
| ---         | ---                                                     |
| genome      | Genome fasta file to be masked                          |
| rmlib       | Repeat database                                         |
| cpus        | Number of CPUs to use                                   |
| output      | Output _directory_                                      |
| cl\_options | Addition command line options (see manual RepeatMasker) |

RepeatMasker can now be started by running `snakemake` in the workflow directory. The workflow will add a `snakemake.done` file in the RepeatMasker output directory after completion. When configuration has changed, for instance the command line options are different, please remove this file to make sure the analysis will start over.

## Tool 7: USearch

The usearch tool ( [http://www.drive5.com/usearch/](http://www.drive5.com/usearch/)) is used for identifying similar sequences and creating a consensus sequence for each of the clusters. This tool is useful after running several repeat finder tools and you would like to combine the predicted repeat sequences into a single file.

Paper: [https://academic.oup.com/bioinformatics/article/26/19/2460/230188](https://academic.oup.com/bioinformatics/article/26/19/2460/230188)

Tool website: [http://www.drive5.com/usearch/](http://www.drive5.com/usearch/)

Focus on: clustering sequences

Type repeats: none

Description:

>UBLAST and USEARCH are new algorithms enabling sensitive local and global search of large sequence databases at exceptionally high speeds. They are often orders of magnitude faster than BLAST in practical applications, though sensitivity to distant protein relationships is lower. UCLUST is a new clustering method that exploits USEARCH to assign sequences to clusters.

**Note:** for this application you need a license, which can be found at:

[http://www.drive5.com/usearch/download.html](http://www.drive5.com/usearch/download.html)

You will receive a download link in your e-mail. **Please add this link to the config.json!**

First, create a single fasta file with all the repeat sequences. The common way is by running `cat`:`cat file1.fa file2.fa … > /tmp/fasta.fa`

Input and output are given in the `config.json`:

| **Field** | **Description**               |
| ---       | ---                           |
| fasta     | Name of the fasta input file  |
| output    | Name of the consensus file    |
