############
##  Code  ##
############
def getLaTeXReport(fastaFile,
                   outputFile,
                   totalSeqs,
                   totalLen,
                   gcPerc,
                   longestSeq,
                   n50Index, n50,
                   n90Index, n90,
                   a50Plot,
                   cegmaScore=None,
                   otherCegmaScores={},
                   dnaMappingStats=None,
                   errorRate=None,
                   snpDensity=None,
                   rnaMappingStats=None):
    """
    Convert all previously calculated statistics into LaTeX with this method.
    """
    print("creating report")
    txt = "\\documentclass{report}\n"
    txt += "\\usepackage[margin=2cm]{geometry}\n"
    txt += "\\usepackage{graphicx}\n"
    txt += "\\begin{document}\n"
    txt += "\\section*{Report of "+os.path.basename(fastaFile)+", generated on \\today}"

    txt += "\\subsection*{Statistics}\n"
    table = LaTeX.ltxTable(2)
    table.addRow(["Total sequences: ",str(totalSeqs)])
    table.addRow(["Total length: ","{:,}".format(totalLen)])
    table.addRow(["GC perc: ","{:.2f}".format(gcPerc) + "\%"])
    table.addRow(["Longest sequence: ","{:,}".format(longestSeq)])
    table.addRow(["N50 index: ","{:,}".format(n50Index)])
    table.addRow(["N50: ","{:,}".format(n50)])
    table.addRow(["",""])
    table.addRow(["N90 index: ","{:,}".format(n90Index)])
    table.addRow(["N90: ","{:,}".format(n90)])
    if cegmaScore != None:
        table.addRow(["",""])
        table.addRow(["Cegma complete: ",cegmaScore[0] + "\%"])
        table.addRow(["Cegma partial: ",cegmaScore[1] + "\%"])
    for name, value in otherCegmaScores.items():
        table.addRow(["",""])
        table.addRow([name + " complete: ","{:.2f}".format(value[0]) + "\%"])
        table.addRow([name + " partial: ","{:.2f}".format(value[1]) + "\%"])

    if dnaMappingStats != None:
        table.addRow(["",""])
        table.addRow(["DNA reads: ","{:,}".format(int(dnaMappingStats["total"]))])
        table.addRow(["Mapped: ",dnaMappingStats["mapped"] + "\%"])
        if "propPair" in dnaMappingStats:
            table.addRow(["Properly paired",dnaMappingStats["propPair"] + "\%"])
    if errorRate != None:
        table.addRow(["Error rate: ","{:.2f}".format(errorRate) + " SNPs per 10kb"])
        table.addRow(["SNP density: ","{:.2f}".format(snpDensity) + " SNPs per 10kb"])
    if rnaMappingStats != None:
        table.addRow(["",""])
        table.addRow(["RNA reads: ","{:,}".format(int(rnaMappingStats["total"]))])
        table.addRow(["Mapped: ",rnaMappingStats["mapped"] + "\%"])
        if "propPair" in rnaMappingStats:
            table.addRow(["Properly paired: ",rnaMappingStats["propPair"] + "\%"])

    txt += table.getText()
    txt += "\\begin{figure}[h]\n"
    txt += "\\includegraphics[scale=0.7]{" + a50Plot + "}\n"
    txt += "\\end{figure}\n"

    txt += "\\end{document}\n"
    with open(outputFile, "w") as outWriter:
        outWriter.write(txt)

def getContigStats(fastaFile):
    """
    The lengths of the contigs are calculated with the biopython library. In the end all contigs are sorted on length.
    The return value is a list with the following information:
    - The sorted list (on length) with all contigs
    - The total number of basepairs
    - The gc percentage
    - The percentage of unkown bases (other chars than ATCG or atcg)
    """
    contigLengths = []
    totalLength = 0
    gcNo = 0
    taNo = 0
    for contig in SeqIO.parse(open(fastaFile), "fasta"):
        gcNo = gcNo + sum(map(contig.seq.count, ['G', 'C', 'g', 'c']))
        taNo = taNo + sum(map(contig.seq.count, ['T', 't', 'A', 'a']))
        contigLenght = len(contig.seq)
        totalLength += contigLenght
        contigLengths.append(contigLenght)

    contigLengths.sort()
    contigLengths.reverse()
    return [contigLengths, totalLength, gcNo/(gcNo+taNo)*100, 100-((gcNo+taNo)/totalLength*100)]

def calculateN(n, contigLengths, totalLength):
    """
    The method calculateN calculates the N50, N90 or any other N.
    The N50 is defined as
    "Given a set of sequences of varying lengths, the N50 length is defined as the length N for which 50% of all bases in the sequences are in a sequence of length L < N."
    """
    lengthTillNow = 0
    indexTillNow = 0
    toThisLength = totalLength * n / 100
    for contigLen in contigLengths:
        lengthTillNow += contigLen
        indexTillNow = indexTillNow + 1
        if toThisLength < lengthTillNow:
            return [indexTillNow,contigLen]

def getSnpDensity(vcfFile, totalLen):
    """
    The SNP density is calculated by reading all lines of a vcf files which are not comments and are not empty, divided
    by the total length multiplied by 10.000. This way the snps per 10kb are calculated.
    """
    print("calculating snp ratio from vcf file")
    errors = 0
    heterozygotes = 0
    with open(vcfFile) as vcfReader:
        for line in vcfReader:
            if line.startswith("#") or line.strip() == False:
                continue
            splitted = line.split("\t")
            if len(splitted) !=10:
                continue
            if splitted[9].startswith("1/1"):
                errors += 1
            else:
                heterozygotes += 1

    return [errors/float(totalLen)*10000, heterozygotes/float(totalLen)*10000]

def getMappingPerc(bamFile):
    """
    The mapping percentage is calculated by samtools flagstat, the output of samtools flagstat is parsed and put into a dictionary
    """
    print("calculating mapping percentage from bam file")
    results = {}
    p = subprocess.Popen("samtools flagstat " + bamFile, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(p.stdout.readline, ''):
        line = line.decode("utf-8")
        if len(line) > 0:
            print(line.strip())
        if("mapped (" in line):
            results["mapped"] = re.findall("\d+.\d+", line)[1]
        elif "properly paired" in line:
            results["propPair"] = re.findall("\d+.\d+", line)[1]
            return results
        elif "in total" in line:
            results["total"] = re.findall("\d+.\d+", line)[0]
    return results

def getCegmaStatistics(cegmaFile):
       """
       This method executes the cegma command and parses the output file to retrieve the percentage of core eukaryotic genes which are found complete or partial.
       """
       complete = "-"
       partial = "-"
       with open(cegmaFile) as fileReader:
           for line in fileReader:
               if not line.strip() or line.startswith("#"):
                   continue
               info = line.split()
               if info[0] == "Complete":
                   complete = info[2]
               elif info[0] == "Partial":
                   partial = info[2]
       return [complete,partial]