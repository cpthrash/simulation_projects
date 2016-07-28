#!/usr/bin/env Rscript

# Enable command-line arguments
args <- commandArgs(trailingOnly = TRUE)

MSstats.file <- args[1] # Get the name of the MSstats file
outfile.name <- args[2] # Get the name of the R output file, i.e. the name of the PDF to be printed

# Read in file
MSstats.data <- read.table(file = MSstats.file,
                      sep = "\t", # Separate columns by tab 
                      header = TRUE, # Don't include header
                      as.is = TRUE,) # No factors!

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
