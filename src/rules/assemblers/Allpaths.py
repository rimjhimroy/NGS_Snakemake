#################
##  Functions  ##
#################
def createInLibsCsv(libraries, outputFile):
    """
    The method createInLibsCsv creates a csv file with all libraries as allpaths wants its input.
    """
    with open(outputFile, "w") as csvWriter:
        csvWriter.write("library_name, project_name, organism_name, type, paired, frag_size, frag_stddev, insert_size, insert_stddev, read_orientation, genomic_start, genomic_end\n")
        for lib in libraries:
            csvWriter.write(lib + ", ")
            csvWriter.write("assembly, ")
            csvWriter.write("assembly, ")
            if CONFIG["libraries"][lib]["type"] == "mp":
                csvWriter.write("jumping, ")
                csvWriter.write("1, ")
                csvWriter.write(", , ")
                csvWriter.write(str(int(CONFIG["libraries"][lib]["insertSize"])) + ", ")
                csvWriter.write(str(int(int(CONFIG["libraries"][lib]["insertSize"])*0.2)) + ", ")
                csvWriter.write("outward, ")
            elif CONFIG["libraries"][lib]["type"] == "pe":
                csvWriter.write("fragment, ")
                csvWriter.write("1, ")
                csvWriter.write(str(int(CONFIG["libraries"][lib]["insertSize"])) + ", ")
                csvWriter.write(str(int(int(CONFIG["libraries"][lib]["insertSize"])*0.2)) + ", ")
                csvWriter.write(", , ")
                csvWriter.write("inward, ")
            elif CONFIG["libraries"][lib]["type"] == "u":
                csvWriter.write("long, ")
                csvWriter.write("0, ")
                csvWriter.write(", , , , , ")
            csvWriter.write("0, 0\n")

def createInGroupsCsv(libraries, outputFile):
    """
    The method createInGroupsCsv creates a csv file with all paths to the libraries in it. When the reads are mated, the last "1" is replaced by a ? for the allpaths regex input.
    """
    with open(outputFile, "w") as csvWriter:
        i = 0
        csvWriter.write("group_name, library_name, file_name\n")
        for lib in libraries:
            if len(CONFIG["libraries"][lib]["reads"])==2:
                csvWriter.write(str(i) + ", " + lib + ", " + rreplace(CONFIG["allpaths"]["input"][lib][0], "1", "?",1) + "\n")
            else:
                csvWriter.write(str(i) + ", " + lib + ", " + CONFIG["allpaths"]["input"][lib][0] + "\n")
            i += 1

def rreplace(s, old, new, occurrence):
    """
    The method rreplace replaces the last occurence(s) of a given string with a new value.
    :param s: The string to replace the last value in
    :param old: The substring to replace
    :param new: The new value for the substring
    :param occurence: The numer of times to replace the substring, beginning from the end.
    """
    li = s.rsplit(old, occurrence)
    return new.join(li)
