#!/usr/bin/env bash

"""This shell script calls on a Python script that simulates fluctuating selection in a haploid population, and redirects the output to an Rscript for plotting and printing of a PDF file.  It also directs the printed pdf file to a specific directory"""

# Start the script

#	Check to see if Rscript is installed. If not, exit with error
if ! $(command -v Rscript > /dev/null 2> /dev/null); then echo "Please install R and place in your PATH" >&2; exit 1; fi

# Call on python script and run simulation
python Fluct_sel_SimuPOP_script.py

# Extract the filename (which is a variable), which is printed on the last line of the Python script
var=`python Fluct_sel_SimuPOP_script.py | tail -n 1`

# Define filename for Outfile - Don't think this is correct, likely will need to read about and change
Outfile=`python Fluct_sel_SimuPOP_script.py | tail -n 1`

# Where is plot_MS.R? 
'''need to update'''
plot_PY.R=/Users/colinpierce/Desktop/plot-PY.R

# If no file exists at plot_PY.R, exit with error
if [[ ! -f "${plot_PY.R}" ]]; then echo "Failed to find plot_PY.R" >&2; exit 1; fi

#	Where should we put the PDF files?
PDF_OUTDIR='/Users/colinpierce/Desktop/simulation_projects/SimuPOP/simuPOP-1.1.7/PDFs'

#	Make the PDF output directory and any missing parent directories
mkdir -p "${PDF_OUTDIR}"

# PY outfile location
Outfile=${HOME}/SFSCode/msstats_reps_${reps}_out.txt



# Call on the R script of filename ''
# Pass argument 1 to the Rscript
# Pass argument 2 to the Rscript
Rscript "${plot_PY.R}" "${HOME}/SFSCode/msstats_reps_${reps}_out.txt" "${PDF_OUTDIR}/MS_${reps}"