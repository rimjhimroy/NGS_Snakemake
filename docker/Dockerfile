FROM ubuntu:16.04

#
# ARGUMENTS
#

ARG USER_UID=1001

ARG CONDA_VER=Anaconda3-4.3.0-Linux-x86_64.sh


#
# SYSTEM REQS
#

RUN apt-get update && apt-get install -y git python python-setuptools sudo wget curl bzip2 && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*



#
# CREATE USER
#

RUN echo USER_UID $USER_UID; \
    useradd --uid $USER_UID --create-home --shell /bin/bash snakemake && \
    echo `echo "snakemake\nsnakemake\n" | passwd snakemake` && \
    adduser snakemake sudo && \
    ln -snf /bin/bash /bin/sh

ADD id_rsa     /home/snakemake/.ssh/
ADD id_rsa.pub /home/snakemake/.ssh/

RUN chmod 750 /home/snakemake/.ssh && \
    chown -R snakemake:snakemake /home/snakemake/.ssh/ && \
    echo "    IdentityFile ~/.ssh/id_rsa" >> /etc/ssh/ssh_config



#
# CHANGE USER
#

USER snakemake

WORKDIR /home/snakemake



#
# INSTALL CONDA
#

RUN wget https://repo.continuum.io/archive/$CONDA_VER -O /tmp/$CONDA_VER && \
    chmod +x /tmp/$CONDA_VER && \
    /tmp/$CONDA_VER -b && \
    rm /tmp/$CONDA_VER

ENV PATH="/home/snakemake/bin:/home/snakemake/.local/bin:/home/snakemake/anaconda3/bin:$PATH"

RUN conda config --add channels conda-forge && \
    conda config --add channels defaults    && \
    conda config --add channels r           && \
    conda config --add channels bioconda    && \
    conda create --name snakemake -y python=3 snakemake biopython



#
# INSTALL SNAKEMAKE
#

RUN mkdir -p  /home/snakemake/.ssh                     && \
    chmod 750 /home/snakemake/.ssh                     && \
    touch     /home/snakemake/.ssh/known_hosts         && \
    chmod 600 /home/snakemake/.ssh/*                   && \
    chown -R snakemake:snakemake /home/snakemake/.ssh/

RUN echo -e "Host git.wur.nl\n\tStrictHostKeyChecking no\n" >> /home/snakemake/.ssh/config && \
    ssh-keyscan -t rsa -H github.com >> /home/snakemake/.ssh/known_hosts && \
    ssh-keyscan -t rsa -H git.wur.nl >> /home/snakemake/.ssh/known_hosts && \
    git clone git@git.wur.nl:warri004/SnakemakeVLPB.git
    
RUN mkdir /home/snakemake/data && \
    mkdir /home/snakemake/bin

ENV PYTHONPATH=$PYTHONPATH:/home/snakemake/SnakemakeVLPB

ADD runSnakemake /home/snakemake/bin/



#
# RUN
#

WORKDIR /home/snakemake/data

#CMD source activate snakemake && snakemake --directory /home/snakemake/data --snakefile /home/snakemake/SnakemakeVLPB/src/workflows/variantCalling/freebayes/Snakefile

ENTRYPOINT ["/home/snakemake/bin/runSnakemake"]
