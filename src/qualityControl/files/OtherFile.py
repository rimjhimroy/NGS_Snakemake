import os

class OtherFile:
    
    def __init__(self, fileName):
        self.fileName = fileName
        
    def __str__(self):
        fileSize = os.path.getsize(self.fileName)
        suffix = os.path.splitext(self.fileName)[1]
        if fileSize == 0:
            return "An empty {} file".format(suffix[1:])
        return "an {} file of size {} bytes".format(suffix[1:],fileSize)