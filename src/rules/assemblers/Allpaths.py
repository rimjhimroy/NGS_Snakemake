#################
##  Functions  ##
#################
import csv

def createInLibsCsv(samples, outputFile):
    """
    The method createInLibsCsv creates a csv file with all libraries as allpaths wants its input.
    """
    csvfile =  open(outputFile, "w")
    try:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(("library_name", "project_name", "organism_name", "type", "paired", "frag_size", "frag_stddev", "insert_size", "insert_stddev", "read_orientation", "genomic_start", "genomic_end"))
        for sample, libraries in samples.items():
            for library, info in libraries.items():
                row = []
                row.append(library)
                row.append("assembly")
                row.append("assembly")
                if info["type"] == "mp":
                    row.append("jumping")
                    row.append(1)
                    row.append("")
                    row.append("")
                    row.append(info["insertSize"])
                    if "insertSizeStDev" in info:
                        if info["insertSizeStDev"] != "":
                            row.append(int(info["insertSizeStDev"]))
                        else:
                            row.append(int(int(info["insertSize"])*0.2))
                    else:
                        row.append(int(int(info["insertSize"])*0.2))
                    row.append("outward")
                    row.append(0)
                    row.append(0)
                elif info["type"] == "pe":
                    row.append("fragment")
                    row.append(1)
                    row.append(int(info["insertSize"]))
                    if "insertSizeStDev" in info:
                        if info["insertSizeStDev"] != "":
                            row.append(int(info["insertSizeStDev"]))
                        else:
                            row.append(int(int(info["insertSize"])*0.2))
                    else:
                        row.append(int(int(info["insertSize"])*0.2))
                    row.append("")
                    row.append("")
                    row.append("inward")
                    row.append(0)
                    row.append(0)
                elif info["type"] == "u":
                    row.append("long")
                    row.append("0")
                    row.append("")
                    row.append("")
                    row.append("")
                    row.append("")
                    row.append("")
                    row.append(0)
                    row.append(0)
                csvWriter.writerow(row)
    finally:
        csvfile.close()

def createInGroupsCsv(samples, outputFile):
    """
    The method createInGroupsCsv creates a csv file with all paths to the libraries in it.
    When the reads are mated, the last "1" is replaced by a ? for the allpaths regex input.
    """
    csvfile =  open(outputFile, "w")
    try:
        csvWriter = csv.writer(csvfile)
        i = 0
        csvWriter.writerow(("group_name", "library_name", "file_name"))
        for sample, libraries in samples.items():
            for library, info in libraries.items():
                #print(library)
                #print(info["type"])
                #print(info["insertSize"])
                #print(info["insertSizeStDev"])
                #print(info["platform"])
                for name,reads in info["readsets"].items():
                    row = []
                    row.append(i)
                    row.append(library)
                    #print(name, reads)
                    if len(reads) == 2:
                        row.append(rreplace(reads[0], "1", "?",1))
                    else:
                        row.append(reads[0])
                    i += 1
                    csvWriter.writerow(row)
    finally:
        csvfile.close()

def rreplace(substitute, old_value, new_value, occurrence):
    """
    The method rreplace replaces the last occurence of a given string with a new value.
    :param substitute: The string to replace the last value with
    :param old_value: The substring to replace
    :param new_value: The new value for the substring
    :param occurence: The number of times to replace the substring from the end.
    See https://docs.python.org/3.4/library/stdtypes.html#str.rsplit
    """
    li = substitute.rsplit(old_value, occurrence)
    return new_value.join(li)
