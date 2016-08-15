#!/bin/sh 

#PBS -l walltime=12:00:00,nodes=1:ppn=8,pmem=20gb
#PBS -m abe
#PBS -M pier0273@umn.edu
#PBS -q lab
#PBS -e /panfs/roc/groups/9/morrellp/pier0273/simulation_projects_MSI/scripts/e_o_files
#PBS -o pipefail /panfs/roc/groups/9/morrellp/pier0273/simulation_projects_MSI/scripts/e_o_files
#PBS -u pier0273

# echo $(pwd -P)
# exit -8

#This shell script calls on a Python script that simulates fluctuating selection in a haploid population, and redirects the output to an Rscript for plotting and printing of a PDF file.  It also directs the printed pdf file to a specific directory

module load molpopgen # load 'molpopgen' in order to use MSstats to produce summary statistics from simulation data outfile

module load R # load R

module load python2 # load python2

# Run the simulation
#python /panfs/roc/groups/9/morrellp/pier0273/simulation_projects_MSI/scripts/Fluct_sel_SimuPOP_script.py

# Extract the filename from the simulation script as a variable, which is printed on the last line of the Python (simulation) script
#:qvar=`python Fluct_sel_SimuPOP_script.py | tail -n 1`

# Run the simulation and extract the filename from the last line
simOutfile=`python /panfs/roc/groups/9/morrellp/pier0273/simulation_projects_MSI/scripts/Fluct_sel_SimuPOP_script.py | tail -n 1`

base=$(basename "${simOutfile}" .txt) # Strip the path information from the filename

popSize=$(echo "${base}" | cut -f 2 -d '-')  # Extract the population size from the filename

generations=$(echo "${base}" | cut -f 3 -d '-')  # Extract the generations from the filename

stablePeriod=$(echo "${base}" | cut -f 4 -d '-')  # Extract the stablePeriod from the filename

lowerSelValue=$(echo "${base}" | cut -f 5 -d '-') # Extract the lower selection value from the filename

upperSelValue=$(echo "${base}" | cut -f 6 -d '-')  # Extract the upper selection value from the filename


# Where is MSstats_outfile? (file containing summary statistics from MSstats)?
MSstats_outfile=/panfs/roc/groups/9/morrellp/pier0273/simulation_projects_MSI/scripts/output_files/MSstats_${popSize}_${generations}_${stablePeriod}_${lowerSelValue}_${upperSelValue}.txt

# Take simOutfile and calculate summary statistics using msstats
cat "/panfs/roc/groups/9/morrellp/pier0273/simulation_projects_MSI/scripts/output_files/${simOutfile}" | msstats > "${MSstats_outfile}"



# If no file exists at MSstats, exit with error
if [[ ! -f "${MSstats_outfile}" ]]; then echo "Failed to find MSstats_outfile" >&2; exit 1; fi

#	Where should we put the PDF files that are printed from the Rscript?
PDF_OUTDIR='/panfs/roc/groups/9/morrellp/pier0273/simulation_projects_MSI/scripts/PDFs'


#	Make the PDF output directory and any missing parent directories
mkdir -p "${PDF_OUTDIR}"


graph_summary_statistics=/panfs/roc/groups/9/morrellp/pier0273/simulation_projects_MSI/scripts/plot_MSstats.R  # Where is the R script that plots the summary statistics?

#	Check to see if Rscript is installed. If not, exit with error
if ! $(command -v Rscript > /dev/null 2> /dev/null); then echo "Please install R and place in your PATH" >&2; exit 1; fi

# Call on the R script of filename 'plot_MSstats.R'
# Pass argument 1 to the Rscript, which is the location of the MSstats_outfile
# Pass argument 2 to the Rscript, which is the name of the PDF outfile
Rscript "${graph_summary_statistics}" "${MSstats_outfile}" "${PDF_OUTDIR}/PDF_${popSize}_${generations}_${stablePeriod}_${lowerSelValue}_${upperSelValue}"