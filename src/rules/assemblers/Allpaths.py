#################
##  Functions  ##
#################
import csv

def createInLibsCsv(libraries, outputFile):
    """
    The method createInLibsCsv creates a csv file with all libraries as allpaths wants its input.
    """
    csvfile =  open(outputFile, "w")
    try:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(("library_name", "project_name", "organism_name", "type", "paired", "frag_size", "frag_stddev", "insert_size", "insert_stddev", "read_orientation", "genomic_start", "genomic_end"))
        for lib in libraries:
            row = []
            row.append(lib)
            row.append("assembly")
            row.append("assembly")
            if libraries[lib]["type"] == "mp":
                row.append("jumping")
                row.append(1)
                row.append("")
                row.append("")
                row.append(libraries[lib]["insertSize"])
                if "insertSizeStDev" in libraries[lib]:
                    if libraries[lib]["insertSizeStDev"] != "":
                        row.append(int(libraries[lib]["insertSizeStDev"]))
                    else:
                        row.append(int(int(libraries[lib]["insertSize"])*0.2))
                else:
                    row.append(int(int(libraries[lib]["insertSize"])*0.2))
                row.append("outward")
                row.append(0)
                row.append(0)
            elif libraries[lib]["type"] == "pe":
                row.append("fragment")
                row.append(1)
                row.append(int(libraries[lib]["insertSize"]))
                if "insertSizeStDev" in libraries[lib]:
                    if libraries[lib]["insertSizeStDev"] != "":
                        row.append(int(libraries[lib]["insertSizeStDev"]))
                    else:
                        row.append(int(int(libraries[lib]["insertSize"])*0.2))
                else:
                    row.append(int(int(libraries[lib]["insertSize"])*0.2))
                row.append("")
                row.append("")
                row.append("inward")
                row.append(0)
                row.append(0)
            elif libraries[lib]["type"] == "u":
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

def createInGroupsCsv(libraries, outputFile):
    """
    The method createInGroupsCsv creates a csv file with all paths to the libraries in it. When the reads are mated, the last "1" is replaced by a ? for the allpaths regex input.
    """
    csvfile =  open(outputFile, "w")
    try:
        csvWriter = csv.writer(csvfile)
        i = 0
        csvWriter.writerow(("group_name", "library_name", "file_name"))
        for lib in libraries:
            row = []
            row.append(i)
            row.append(lib)
            if len(libraries[lib]["reads"]) == 2:
                row.append(rreplace(libraries[lib]["reads"][0], "1", "?",1))
            else:
                row.append(libraries[lib]["reads"][0])
            i += 1
            csvWriter.writerow(row)
    finally:
        csvfile.close()

def rreplace(s, old, new, occurrence):
    """
    The method rreplace replaces the last occurence(s) of a given string with a new value.
    :param s: The string to replace the last value with
    :param old: The substring to replace
    :param new: The new value for the substring
    :param occurence: The number of times to replace the substring, beginning from the end.
    """
    li = s.rsplit(old, occurrence)
    return new.join(li)
