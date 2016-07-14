#!/usr/bin/env bash

"""This shell script calls on a Python script that simulates fluctuating selection in a haploid population, and redirects the output to an Rscript for plotting and printing of a PDF file.  It also directs the printed pdf file to a specific directory"""

module load molpopgen # load 'molpopgen' in order to use MSstats to produce summary statistics from simulation data outfile

# Run the simulation
python Fluct_sel_SimuPOP_script.py

# Extract the filename from the simulation script as a variable, which is printed on the last line of the Python (simulation) script
var=`python Fluct_sel_SimuPOP_script.py | tail -n 1`

# Where is outfile from simulation? 
'''Need to update'''
simOutfile=`python Fluct_sel_SimuPOP_script.py | tail -n 1`

# Take simOutfile and calculate summary statistics using msstats
simOutfile | msstats >msstats_sel_${selection}_mut_time_${mut_time}_out.txt

# Where is plot_MSstats.R (file containing summary statistics using MSstats)?
'''need to update'''
plot_MSstats.R=/Users/ColinPierce/Desktop/simulation_projects/SimuPOP/simuPOP-1.1.7/working_scripts

# If no file exists at plot_MSstats.R, exit with error
if [[ ! -f "${plot_MSstats.R}" ]]; then echo "Failed to find plot_MSstats.R" >&2; exit 1; fi

#	Where should we put the PDF files that are printed from the Rscript?
PDF_OUTDIR='/Users/ColinPierce/Desktop/simulation_projects/PDFs'

#	Make the PDF output directory and any missing parent directories
mkdir -p "${PDF_OUTDIR}"



#	Check to see if Rscript is installed. If not, exit with error
if ! $(command -v Rscript > /dev/null 2> /dev/null); then echo "Please install R and place in your PATH" >&2; exit 1; fi

# Call on the R script of filename ''
# Pass argument 1 to the Rscript
# Pass argument 2 to the Rscript
Rscript "${plot_MSstats.R}" "${HOME}/SFSCode/msstats_reps_${reps}_out.txt" "${PDF_OUTDIR}/MS_${reps}"