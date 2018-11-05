# Workflows in Snakemake for VLPB #

In this project, a couple of workflows have been made, the main ones are:

* Genome assembly
* Variant calling
* Genome annotation
* Repeat detection and masking


## Docker ##
The preferable method to run these pipelines is through Docker (https://www.docker.com/).

To run with docker:

- Follow the installation instructions for docker in https://www.docker.com/products/overview.
- run `buildDocker.sh` from the docker folder in the root
- Start an interactive shell: `docker run -i -t vlpb/snakemake /bin/bash`

This will bring you to the data folder of the snakemake user. You can add your own data here, but the docker already contains test data.
In the `/home/snakemake/bin` folder there is a `runSnakemake` script, which will start a selected part of the pipeline:

`./runSnakemake repeats/modeler`



## Local installation ##

To run a workflow, you will need:

* Python 3
* Snakemake
* Biopython

### Example ###

The repository was extracted in `/tmp/SnakeMakeVlpb` , with ```git clone https://git.wur.nl/warri004/SnakemakeVLPB.git /tmp/SnakeMakeVlpb```.
Please note the capitol "M" in the target directory.

To let Snakemake find our code, we need to add that directory to the `PYTHONPATH`:

    export PYTHONPATH=$PYTHONPATH:/tmp/SnakeMakeVlpb/

Now we can set everything up:

    cd /tmp/SnakeMakeVlpb/src/workflows/assembly/allpaths/noPreprocess

    # Install necessary modules in a virtual environment using virtualenv and pip
    virtualenv --python=python3 venv
    source venv/bin/activate
    pip3 install snakemake biopython

Or

    # Install necessary modules in a virtual environment using conda and bioconda
    conda create --name snakemake python=3 snakemake biopython
    source activate snakemake

And then we can simply start the assembly, using the default dataset, as described in `config.json`:

    snakemake

If you want to run a workflow somewhere else, you can tell `snakemake` to load the workflow from there, but make sure that the `PYTHONPATH` is set correctly.

    cd ~/data ; snakemake --snakefile /tmp/SnakeMakeVlpb/src/workflows/variantCalling/freebayes/Snakefile
