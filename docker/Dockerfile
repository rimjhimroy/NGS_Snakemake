FROM ubuntu:latest

MAINTAINER Sven Warris (sven.warris@wur.nl)

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-dev python3-pip python3-setuptools git wget build-essential ssh less emacs

RUN pip3 install setuptools wheel
RUN pip3 install snakemake

#
# SYSTEM REQS
#

RUN apt-get update && apt-get install -y git python python-setuptools sudo wget curl bzip2 && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*



#
# CREATE USER
#
ARG USER_UID=1001

RUN echo USER_UID $USER_UID; \
    useradd --uid $USER_UID --create-home --shell /bin/bash snakemake && \
    echo `echo "snakemake\nsnakemake\n" | passwd snakemake` && \
    adduser snakemake sudo && \
    ln -snf /bin/bash /bin/sh

ADD id_rsa     /home/snakemake/.ssh/
ADD id_rsa.pub /home/snakemake/.ssh/

RUN chmod 750 /home/snakemake/.ssh && \
    chown -R snakemake:snakemake /home/snakemake/.ssh/ 
#&& \
#    echo "    IdentityFile ~/.ssh/id_rsa" >> /etc/ssh/ssh_config



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


RUN echo -e "Host git.wur.nl\n\tStrictHostKeyChecking no\n" >> /home/snakemake/.ssh/config && \
    ssh-keyscan -t rsa -H github.com >> /home/snakemake/.ssh/known_hosts && \
    ssh-keyscan -t rsa -H git.wur.nl >> /home/snakemake/.ssh/known_hosts && \
    git clone git@git.wur.nl:warri004/SnakemakeVLPB.git && \
    ln -s SnakemakeVLPB SnakeMakeVlpb
    
RUN mkdir /home/snakemake/data && \
    mkdir /home/snakemake/bin

ENV PYTHONPATH=$PYTHONPATH:/home/snakemake/SnakeMakeVlpb

ADD runSnakemake /home/snakemake/bin/

#
# RUN
#

WORKDIR /home/snakemake/data

#CMD source activate snakemake && snakemake --directory /home/snakemake/data --snakefile /home/snakemake/SnakemakeVLPB/src/workflows/variantCalling/freebayes/Snakefile

#ENTRYPOINT ["/home/snakemake/bin/runSnakemake"]

