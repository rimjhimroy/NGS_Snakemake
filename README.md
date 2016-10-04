# Workflows in Snakemake for VLPB #


In this project, a couple of workflows have been made, the main ones are:

* Genome assembly
* Variant calling
* Genome annotation

To run a workflow, you will need:

* Python 3
* Snakemake
* Biopython

## Example ##

The repository was extracted in `/tmp/SnakeMakeVlpb` , with ```git clone https://git.wur.nl/warri004/SnakemakeVLPB.git /tmp/SnakeMakeVlpb```.

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
