#!/usr/bin/env bash

#This shell script calls on a Python script that simulates fluctuating selection in a haploid population, and redirects the output to an Rscript for plotting and printing of a PDF file.  It also directs the printed pdf file to a specific directory

module load molpopgen # load 'molpopgen' in order to use MSstats to produce summary statistics from simulation data outfile

module load R # load R

# Run the simulation
python Fluct_sel_SimuPOP_script.py

# Extract the filename from the simulation script as a variable, which is printed on the last line of the Python (simulation) script
var=`python Fluct_sel_SimuPOP_script.py | tail -n 1`

# Where is outfile from simulation? 
# Need to update
simOutfile=`python Fluct_sel_SimuPOP_script.py | tail -n 1`

base=$(basename "${simOutfile}" .txt) # Strip the path information from the filename, printing only the file name

popSize=$(echo "${base}" | cut -f 2 -d '-')

generations=$(echo "${base}" | cut -f 3 -d '-')

lowerSelValue=$(echo "${base}" | cut -f 4 -d '-')

upperSelValue=$(echo "${base}" | cut -f 5 -d '-')

# Take simOutfile and calculate summary statistics using msstats
cat "${simOutfile}" | msstats > MSstats_popSize_${popSize}_generations_${generations}_lowerSelValue_${lowerSelValue}_upperSelValue__${upperSelValue}_out.txt

# Where is MSstats_outfile? (file containing summary statistics from MSstats)?
MSstats_outfile=/home/morrellp/pier0273/simulation_projects_MSI/scripts/MSstats_popSize_${popSize}_generations_${generations}_lowerSelValue_${lowerSelValue}_upperSelValue__${upperSelValue}_out.txt


# If no file exists at MSstats, exit with error
if [[ ! -f "${MSstats_outfile}" ]]; then echo "Failed to find MSstats_outfile" >&2; exit 1; fi

#	Where should we put the PDF files that are printed from the Rscript?
PDF_OUTDIR='/home/morrellp/pier0273/simulation_projects_MSI/PDFs/PDFs'


#	Make the PDF output directory and any missing parent directories
#mkdir -p "${PDF_OUTDIR}"


plot_MSstats.R=/home/morrellp/pier0273/simulation_projects_MSI/scripts/  # Where is the R script that plots the summary statistics?

#	Check to see if Rscript is installed. If not, exit with error
if ! $(command -v Rscript > /dev/null 2> /dev/null); then echo "Please install R and place in your PATH" >&2; exit 1; fi

# Call on the R script of filename 'plot_MSstats.R'
# Pass argument 1 to the Rscript, which is the location of the MSstats_outfile
# Pass argument 2 to the Rscript
Rscript "${plot_MSstats.R}" "${MSstats_outfile}" "${PDF_OUTDIR}/PDF_${popSize_${popSize}_generations_${generations}_lowerSelValue_${lowerSelValue}_upperSelValue__${upperSelValue}}"