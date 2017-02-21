#!/bin/bash

set -xeu

source domain

for snakefile1 in `cd ../src/workflows/ && find -name 'Snakefile'`; do
    echo snakefile1 $snakefile1
    snakefile2=${snakefile1//\.\//}
    snakename1=${snakefile2//\//_}
    snakename=${snakename1,,}
    echo snakefile2 $snakefile2
    echo snakename1 $snakename1
    echo snakename  $snakename

    mkdir -p sub
    cd sub
    mkdir -p $snakename
    cd $snakename
    echo "FROM sauloal/snakemake" > Dockerfile
    echo "CMD source activate snakemake && snakemake --directory /home/snakemake/data --snakefile /home/snakemake/SnakemakeVLPB/src/workflows/$snakefile2" >> Dockerfile
    docker build --rm -t ${DOMAIN}/snakemake_${snakename} .
    cd ../..
done
