#!/usr/bin/env Rscript

# Enable command-line arguments
args <- commandArgs(trailingOnly = TRUE)


filelist = list.files(pattern = "MSStats*.txt")

datalist = lapply(filelist, function(x)read.table(x, header=T)) 

datafr = do.call("rbind", datalist) 

# Start the PDF printer
pdf(file = paste0(outfile.name, ".pdf"), width = 6, height = 6)

# Make a barplot of Pi values
barplot(height = MSstats.data$theta, xlab = "theta Values", ylab = "Counts", main = "theta Values", col = "cyan")

# Make a barplot of Segregating sites(S)
barplot(height = MSstats.data$S, xlab = "# Segregating Sites", ylab = "Counts", main = "Segregating Sites", col = "red")

# Make a barplot of Segregating sites(S)
barplot(height = MSstats.data$pi, xlab = "Pi", ylab = "Counts", main = "Pi values", col = "red")

# Make a barplot of Tajima's D values
barplot(height = MSstats.data$tajd, xlab = "Tajima's D", ylab = "Counts", main = "Tajima's D", col = "springgreen")

# Make a barplot of Theta H values
barplot(height = MSstats.data$thetaH, xlab = "ThetaH", ylab = "Counts", main = "ThetaH Values", col = "violetred")



# Turn the PDF printer off
dev.off()
