"""
@author: Jetse
@version: 0.1
"""

###############
##  Imports  ##
###############

##############
##  Tophat  ##
##############
rule TophatPaired:
    input: 
        forward = lambda wildcards: CONFIG["mapping"]["reads"][wildcards.sample][0],
        reversed = lambda wildcards: CONFIG["mapping"]["reads"][wildcards.sample][1],
        reference = CONFIG["mapping"]["referenceGenome"],
        index = CONFIG["mapping"]["referenceGenome"] + ".1.bt2"
    output:
        mapped = ""
        unmapped = "variantCalling/"
