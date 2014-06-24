import re, sys

class GenblastParser():
    def __init__(self, filename):
        self.currentGene = None
        self.genes = []
        self.queries = {}
        with open(filename) as genblastReader:
            for line in genblastReader:
                if line.startswith("//") or line.startswith("genBlast phase"):
                    if line.startswith("//for query"):
                        line = line.replace("//for query: ","").replace("//","").strip()
                        self.queries[line.split("|")[-1]] = [0,0]
                    continue
                if line.strip():
                    self.parseGenes(line)
        partial = 0
        full = 0
        for entry in self.queries.values():
            if entry[0] > 0:
                full += 1
            if entry[1] > 0 or entry[0] > 0:
                partial += 1
                        
        self.partial = partial / float(len(self.queries)) * 100
        self.full = full/float(len(self.queries))*100
    
    def parseGenes(self, line):
        splittedLine = line.split("|")
        if len(splittedLine) > 5:
            self.currentGene = Gene(splittedLine)
            if float(self.currentGene.score) > 0:
                if self.currentGene.cover > 70:
                    self.queries[splittedLine[-6]][0] += 1
                else:
                    self.queries[splittedLine[-6]][1] += 1
                self.genes.append(self.currentGene)
            else:
                self.currentGene = None
        else:
            if self.currentGene !=None:
                try:
                    Exon(line, self.currentGene)
                except AttributeError:
                    #This line probaby contains None, so this gene has no hits
                    pass
    
    def createGffFile(self, fileName):
        with open(fileName, "w") as gffWriter:
            for gene in self.genes:
                gffWriter.write(gene.toGff())
        
class Gene():
    def __init__(self, geneInfo):
        self.chrom = geneInfo[-5].split(":")[0]
        self.start = geneInfo[-5].split(":")[1].split("..")[0]
        self.end = geneInfo[-5].split(":")[1].split("..")[1]
        self.name = geneInfo[-6] + "_" + geneInfo[-1].split(":")[1].strip()
        self.score = geneInfo[-2].split(":")[1]
        self.rank = int(geneInfo[-1].split(":")[1].strip())
        self.cover = float(re.search("\((\d+\.?\d*)%\)",geneInfo[-3]).group(1))
        self.exons = []
        self.strand = geneInfo[-4]
    
    def toGff(self):
        txt = "\t".join([self.chrom,"genBlastA","gene",self.start,self.end,self.score, self.strand, ".","ID=" + self.name + ";Name="+self.name]) + "\n"
        for exon in self.exons:
            txt += exon.toGff()
        return txt
    
    def __repr__(self):
        return self.__str__()
        
    def __str__(self):
        return "Gene[name="+self.name+ ", chrom=" + self.chrom + ", start=" +self.start + ", end=" + self.end + ", score="+self.score+ ", exons=" + str(len(self.exons))+"]"
        
    
        
class Exon():
    
    def __init__(self, exonInfo, gene):
        matchObj = re.search("HSP_ID\[(\d+)\]:\(([0-9]+).([0-9]+)\);query:\(([0-9]+).([0-9]+)\); pid: (\d+\.?\d*)", exonInfo)
        if matchObj == None:
            raise AttributeError("No match found...")
        self.exonIndex = matchObj.group(1)
        self.start = matchObj.group(2)
        self.end = matchObj.group(3)
        self.identity = matchObj.group(6)
        gene.exons.append(self)
        self.gene = gene
    
    def toGff(self):
        return "\t".join([self.gene.chrom,"genBlastA","exon",self.start,self.end,self.identity, self.gene.strand, ".","Parent="+self.gene.name+";"]) + "\n"
        
    def __repr__(self):
        return self.__str__()
        
    def __str__(self):
        return "Exon[id="+self.exonIndex+ ", start=" +self.start + ", end=" + self.end + ", identity="+self.identity+"]"

