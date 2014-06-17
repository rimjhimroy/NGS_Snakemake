"""
@version 0
@author: Jetse
"""

class BamFile:
    
    def __init__(self, fileName, sam=True):
        self.fileName = fileName
        self.sam = sam
        
    def isValid(self):
        print("WARNING: bam check not yet implemented, always returning true!")
        return True
    
    def getInsertSizeDistribution(self):
        raise NotImplementedError()
    
    def getStatistics(self):
        raise NotImplementedError()