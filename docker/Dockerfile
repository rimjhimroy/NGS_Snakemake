FROM ubuntu:latest

MAINTAINER Sven Warris (sven.warris@wur.nl)

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-dev python3-pip python3-setuptools git wget build-essential

RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh; bash Miniconda3-latest-Linux-x86_64.sh -b; rm Miniconda3-latest-Linux-x86_64.sh

RUN pip3 install setuptools wheel
RUN pip3 install snakemake

