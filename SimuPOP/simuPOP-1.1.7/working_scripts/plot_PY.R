#!/usr/bin/env Rscript

# Enable command-line arguments
args <- commandArgs(trailingOnly = TRUE)

simuPOP.file <- args[1] # Get the name of the simuPOP output file
outfile.name <- args[2] # Get the name of the R output file, i.e. the name of the PDF to be printed

# Read in file
simuPOP.data <- read.table(file = simuPOP.file,
                      sep = "\t", # Separate columns by tab 
                      header = FALSE, # Don't include header
                      as.is = TRUE,) # No factors!

# Set the names of our dataframe
names(x = simuPOP.data) <- c("Pi", "Pi.values", "SS", "SS.values", "TajD", "TajD.values", "thetaH", "thetaH.values", "H", "Het?")

# Start the PDF printer
pdf(file = paste0(outfile.name, ".pdf"), width = 6, height = 6)

# Make a barplot of Pi values
barplot(height = ms.data$Pi.values, xlab = "Pi Values", ylab = "Counts", main = "Counts of Pi Values", col = "cyan")

# Make a barplot of Tajima's D values
barplot(height = ms.data$TajD.values, xlab = "Tajima's D", ylab = "Counts", main = "Counts of Tajima's D", col = "springgreen")

# Make a barplot of Theta H values
barplot(height = ms.data$thetaH.values, xlab = "Theta H", ylab = "Counts", main = "Counts of Theta H", col = "violetred")

# Turn the PDF printer off
dev.off()
