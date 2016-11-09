library(cummeRbund)
cuff<-readCufflinks()
cuff

width<-1900
height<-1200

png(filename="dispersionPlot.png", width=width ,height=height )
dispersionPlot(genes(cuff))
dev.off()

png(filename="MDSplot.png", width=width ,height=height )
MDSplot(genes(cuff))
dev.off()

png(filename="MDSplot_with_replicates.png", width=width ,height=height )
MDSplot(genes(cuff),replicates=T)
dev.off()

png(filename="csDistHeat.png", width=width ,height=height )
csDistHeat(genes(cuff))
dev.off()

png(filename="csDistHeat_with_replicates.png", width=width ,height=height )
csDistHeat(genes(cuff),replicates=T)
dev.off()

png(filename="sigMatrix.png", width=width ,height=height )
sigMatrix(cuff,level='genes',alpha=0.05)
dev.off()