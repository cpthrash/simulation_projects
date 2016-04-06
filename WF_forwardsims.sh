#!/usr/bin/env bash

set -e
set -u
set -o pipefail

#PBS -l mem=8000mb,nodes=1:ppn=1,walltime=72:00:00
#PBS -m abe
#PBS -M pier0273@umn.edu
#PBS -q lab

# shell script for forward simulations of fluctuating selection in a haploid population with no recombination
# exploring the dynamics of drift, mutation, and fecundity selection

# requires ms-stats for descriptive stats
# accepts arguments on the command line for replicate number (default=1000)
# also accepts argument for selection (default=0)

# default initial burn-in period is 5xPN generations (P=ploidy and N=initial pop size)
# change initial burn-in using --BURN (-B) <burn>
# subsequent burn-in periods are 2xPN
# change subsequent burn-in periods (for iterations >1) using --BURN2 (-b) <burn>

# first sims to be run with no selection to get running

reps=2
# this section hasn't been updated yet and is from Peter's sims
# selective coeffiecent, 5, 10, 20, 40%
# scaled as 2N
# this is a bash array!
# selection=(3000 6000 12000 24000) (remove # from this line when ready to icdmplement selection)
selection=3000

# ploidy.  default is diploid, need to use P=1 for haploid population
ploidy=1

# telling simulation when to end, scaled in PN generations where P=ploidy and N=initial pop size
# not sure how many generations to run, might need to play around with this parameter a bit and see if/how results change based on diff. sim times
TE=1000

# not sure what getopts is, will leave this section as is for now
# not currently using getopts, should fix this
#while getopts r:s: o 
#do    case "$o" in
#	s)    selection="$OPTARG";;
#	r)    reps="$OPTARG";;
#	[?])  print >&2 "Usage: $0 [-r] replicates..."
#       exit 1;;
#   esac
#done
#shift $OPTIND

# need to look more into why molpopgen is used, no explanation from Peter's sims
module load molpopgen

# create some workspace and move there
DIRECTORY='/home/morrellp/pier0273/simulation_projects'

# not sure if this is needed since this directory (or a similar one) already exists
#if [ ! -d "$DIRECTORY" -a -w "$DIRECTORY" ]; then
#	mkdir $DIRECTORY
#	mkdir $DIRECTORY/SFS_code
#	fi
# mkdir $DIRECTORY/SFS_code (remove # to implement)
# cd $DIRECTORY/SFS_Code/ (remove # to implement)

# biologicals
# theta = mutation rate per site
theta=0.005 # mutation rate is fixed, varies between 10^-8 - 10^-1
# recombination rate: no recombination, so removed, remove # in future if desired
# rho=$(echo "$theta * 0" | bc )
# echo $rho
# locus length for simulation
# locus_length=3385 # unsure which locus length to use, for now will use default locus length of 5000

# mutation position
# not sure if need to specify position of specifc mutation(s), might want to change this?
# mutation=1607 (remove # if want to implement specific position for mutation)

# mutation time
# set to 2Ne by generations or 160/60000
# try a few values for age of muation
# so mutation at 100 1000 6000 10000 20000
# don't need specific mutation times, so going to remove this for now 
# mut_time=(0.00167 0.0167 0.100 0.167 0.300) (remove # if need to implement mut_time parameter)

# minimum frequency and maximum frequency appear to be for tracking trajectory of a selected mutation, and only print the output when it achieves a particular frequency range
# removing minimum and maximum frequency parameters

# number of populations
pops=1
# size of population to simulate
# population size is fixed, will vary between simulations from 100-10,000.  Other pop sizes to include?
pop_size=2000

# number of replicates
reps=100

#full path to sfs_code for simulations
SFS=${HOME}/SFSCode/bin/sfs_code
#full path to convertSFS_code for transforming simulation output
convertSFS=${HOME}/SFSCode/bin/convertSFS_CODE 
# Hudson's stats program - summarizing values (remove # from following line when implementing stats)
stats=${HOME}/MS/stats 

# iterating over the above arrays of the array for selection strength
# and mutation time
# disabling the for loop on next 4 lines for now. remove # on each line when needing to implement
# for selection in "${selection[@]}"
#	do
#		for mut_time in "${mut_time[@]}"
#			do

# simulation control variables
seed=$(echo $RANDOM)

# outfile from simulations
SFS_out=${HOME}/SFSCode/outfile_reps_${reps}.txt

#	Make the output file exist
touch "${SFS_out}"

# MS outfile
MSStats=${HOME}/SFSCode/msstats_reps_${reps}_out.txt

# make the ms output file exist
touch "${MSStats}"

# removed (--mutation $mut_time S $mutation G $selection --trackTrajectory S $mutation) b/c not using selection or mutation in first round of simulations
$SFS $pops $reps --ploidy $ploidy --seed $seed --theta $theta --popSize $pop_size --outfile ${HOME}/SFSCode/outfile_reps_${reps}.txt 
# sleep 30m
#
$convertSFS $SFS_out --ms T 2 | ${HOME}/MS/sample_stats > ${HOME}/SFSCode/msstats_reps_${reps}_out.txt

# think i need to disable these (done) on the next 2 lines, as they're part of the for loop?  (remove # when need to implement)
#    done
# done
