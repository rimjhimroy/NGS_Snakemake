FROM ubuntu:18.04

MAINTAINER Sven Warris (sven.warris@wur.nl)

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-dev python3-pip python3-setuptools git wget build-essential ssh less emacs libidn2-0 sra-toolkit bc

RUN pip3 install setuptools wheel
RUN pip3 install snakemake

#
# SYSTEM REQS
#

RUN apt-get update && apt-get install -y git python python-setuptools sudo wget curl bzip2 && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN cpan App::cpanminus

RUN /usr/bin/wget https://ftp.gnu.org/gnu/libidn/libidn-1.9.tar.gz && \
	tar zxvf libidn-1.9.tar.gz && \
	cd libidn-1.9 && \
	./configure --prefix=/usr/ && \
	make install && \
	cd .. && \
	rm -rf libidn-1.9* 

#
# CREATE USER
#
ARG USER_UID=1001

RUN echo USER_UID $USER_UID; \
    useradd --uid $USER_UID --create-home --shell /bin/bash snakemake && \
    echo `echo "snakemake\nsnakemake\n" | passwd snakemake` && \
    adduser snakemake sudo && \
    ln -snf /bin/bash /bin/sh




#
# CHANGE USER
#

USER snakemake

WORKDIR /home/snakemake



#
# INSTALL CONDA
#

#RUN wget https://repo.continuum.io/archive/$CONDA_VER -O /tmp/$CONDA_VER && \
#    chmod +x /tmp/$CONDA_VER && \
#    /tmp/$CONDA_VER -b && \
#    rm /tmp/$CONDA_VER
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
	bash Miniconda3-latest-Linux-x86_64.sh -b 
	#&& \
	#rm Miniconda3-latest-Linux-x86_64.sh

ENV PATH="/home/snakemake/bin:/home/snakemake/.local/bin:/home/snakemake/miniconda3/bin:$PATH"

RUN conda config --add channels conda-forge && \
    conda config --add channels defaults    && \
    conda config --add channels r           && \
    conda config --add channels bioconda    && \
    conda create --name snakemake -y python=3 snakemake biopython

RUN conda install --yes seqtk

RUN cpanm --local-lib=~/perl5 local::lib && eval $(perl -I ~/perl5/lib/perl5/ -Mlocal::lib)
 
RUN git clone https://git.wur.nl/warri004/SnakemakeVLPB.git  && \
    ln -s SnakemakeVLPB SnakeMakeVlpb

    
RUN mkdir /home/snakemake/data && \
    mkdir /home/snakemake/bin

ENV PYTHONPATH=$PYTHONPATH:/home/snakemake/SnakeMakeVlpb

ADD runSnakemake /home/snakemake/bin/

RUN echo 'export PERL_MB_OPT="--install_base \"/home/snakemake/perl5\""' >> /home/snakemake/.bashrc
RUN echo 'export PERL_MM_OPT=INSTALL_BASE=/home/snakemake/perl5' >> /home/snakemake/.bashrc
RUN echo 'export PERL_LOCAL_LIB_ROOT=/home/snakemake/perl5' >> /home/snakemake/.bashrc
RUN echo 'export PERL5LIB=/home/snakemake/perl5/lib/perl5' >> /home/snakemake/.bashrc
#
# RUN
#

# Download test data
RUN cd /home/snakemake/data && \
	/usr/bin/wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_genomic.fna.gz && \
	gunzip GCF_000001735.4_TAIR10.1_genomic.fna.gz
	
RUN mkdir /home/snakemake/data/databases && \
	cd /home/snakemake/data/databases && \
	/usr/bin/wget ftp://ftpmips.helmholtz-muenchen.de/plants/REdat/mipsREdat_9.3p_ALL.fasta.gz && \
	gunzip mipsREdat_9.3p_ALL.fasta.gz
	
RUN mkdir /home/snakemake/data/Pleurotus_ostreatus && \
	cd  /home/snakemake/data/Pleurotus_ostreatus && \
	wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR638/008/SRR6384728/SRR6384728_1.fastq.gz && \
	wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR638/008/SRR6384728/SRR6384728_2.fastq.gz && \
	gunzip SRR6384728_1.fastq.gz && \
	gunzip SRR6384728_2.fastq.gz
	

WORKDIR /home/snakemake/data
ENV USEARCH=2019010405583625040 
RUN bash /home/snakemake/bin/runSnakemake repeats/masker repeatmasker_installation	
RUN bash /home/snakemake/bin/runSnakemake repeats/modeler repeatmodeler_installation	
RUN bash /home/snakemake/bin/runSnakemake repeats/reas reas_installation	
RUN bash /home/snakemake/bin/runSnakemake repeats/tedna tedna_installation	
RUN bash /home/snakemake/bin/runSnakemake repeats/transposome install_transposome	
RUN bash /home/snakemake/bin/runSnakemake repeats/usearch usearch_installation	


	

