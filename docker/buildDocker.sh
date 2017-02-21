#!/bin/bash

set -xeu

source domain

if [[ -f "ok" ]]; then
exit 0
fi

docker build --rm -t ${DOMAIN}/snakemake .

touch ok
