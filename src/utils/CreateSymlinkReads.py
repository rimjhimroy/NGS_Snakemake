#!/usr/bin/python
#################
# INFO		#
#################

#"""
#renames the readfiles indicated in the JSON file to symlinks in the read_dir folder
#These renamed filenames are the basis of the pipeline
#
#Sample definition in JSON file (example):
#{
#    "samples": {
#        "Staphylococcus aureus (SRS004751,SRS004751)": {
#            "SRR022868": {
#                "readsets": {
#                        "1": [
#                                "/home/haars001/scratch/projects/VLPB/test_data/Staphylococcus_aureus/Data.original/frag_1.fastq.gz",
#                                "/home/haars001/scratch/projects/VLPB/test_data/Staphylococcus_aureus/Data.original/frag_2.fastq.gz"
#                                ]
#                        },
#                "type": "pe",
#                "insertSize": "180",
#                "insertSizeStDev": "",
#                "platform": "illumina"
#            },
#            "SRR022865": {
#                "readsets": {
#                        "1": [
#                                "/home/haars001/scratch/projects/VLPB/test_data/Staphylococcus_aureus/Data.original/shortjump_1.fastq.gz",
#                                "/home/haars001/scratch/projects/VLPB/test_data/Staphylococcus_aureus/Data.original/shortjump_2.fastq.gz"
#                                ]
#                        },
#                "type": "mp",
#                "insertSize": "3500",
#                "insertSizeStDev": "",
#                "platform": "illumina"
#            }
#        }
#    }
#}
#
#
#"""
import sys
import json
import os

def createSymlinks(CONFIG):
    for sample in CONFIG["samples"]:
        for lib in CONFIG["samples"][sample]:
           for readset in CONFIG["samples"][sample][lib]["readsets"]:
                for path in CONFIG["samples"][sample][lib]["readsets"][readset]:
                    splitpath=path.split("/")
                    dir="./reads/" + sample + "/" + lib + "/" + readset
                    try:
                        os.stat(dir)
                    except:
                        print("Creating " + dir, file=sys.stderr)
                        os.makedirs(dir)
                    newpath=dir + "/" + splitpath[-1]
                    oldpath=path
                    try:
                        os.stat(newpath)
                        print(newpath,"already exists, skipping", file=sys.stderr)
                    except:
                        print(oldpath," -> ",newpath)
                        os.symlink(oldpath, newpath)

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        config = json.load(f)
        createSymlinks(config)

