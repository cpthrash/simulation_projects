#!/usr/bin/env bash

"""This shell script calls on a Python script that simulates fluctuating selection in a haploid population, and redirects the output to an Rscript for plotting and printing of a PDF file.  It also directs the printed pdf file to a specific directory"""

# Start the script



# Call on python script for simuPOP simulation
python Fluct_sel_SimuPOP_script.py

# Extract the filename from the python script as a variable, which is printed on the last line of the Python script
# Need to change this to correct filepath after testing, i.e. 'python Fluct_sel_SimuPOP_script.py'
Outfile=`python test.py | tail -n 1`

cat $Outfile  # take out later, print var to screen for testing purposes

# Check to see if Rscript is installed. If not, exit with error
if ! $(command -v Rscript > /dev/null 2> /dev/null); then echo "Please install R and place in your PATH" >&2; exit 1; fi

# Where is plot_MS.R?
plot_PY.R=/Users/colinpierce/Desktop/plot-PY.R

# If no file exists at plot_PY.R, exit with error
if [[ ! -f "${plot_PY.R}" ]]; then echo "Failed to find plot_PY.R" >&2; exit 1; fi

#	Where should we put the PDF files?
PDF_OUTDIR='/Users/colinpierce/Desktop/simulation_projects/SimuPOP/simuPOP-1.1.7/PDFs'

#	Make the PDF output directory and any missing parent directories
mkdir -p "${PDF_OUTDIR}"

# PY outfile location
Outfile=${HOME}/SFSCode/msstats_reps_${reps}_out.txt



# Call on the R script
# Argument 1 from R script
# Argument 2 from R script
Rscript "${plot_PY.R}" "${HOME}/Desktop/simulation_projects/${Outfile}.txt" "${PDF_OUTDIR}/${Outfile}"