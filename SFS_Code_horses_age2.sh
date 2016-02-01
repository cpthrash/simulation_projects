#!/usr/bin/env bash

set -e
set -u
set -o pipefail

#PBS -l mem=1000mb,nodes=1:ppn=1,walltime=72:00:00
#PBS -m abe
#PBS -M pmorrell@umn.edu

# shell script for forward simulations for GYS1
# frequency of GYS1 mutation from McCue et al. Animal Genetics 2010

# requires libsequence for descriptive stats
# accepts arguments on the command line for replicate number (default=1000)
# also accepts argument for selection (default=0)
# switches work as follows "./SFS_Code_horse.sh -r 10000 -s 0.01"

reps=2
# selective coeffiecent, 5, 10, 20, 40%
# scaled as 2N
# this is a bash array!
# not sure if this syntax works for all shells, or just bash
selection=(3000 6000 12000 24000)

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

module load molpopgen

# create some workspace and move there
DIRECTORY=~/Working

#if [ ! -d "$DIRECTORY" -a -w "$DIRECTORY" ]; then
#	mkdir $DIRECTORY
#	mkdir $DIRECTORY/SFS_code
#	fi
cd $DIRECTORY/SFS_Code/

# biologicals
# mean theta across loci (not including GYS1), species theta
# mean theta across unaffected
theta=0.001627 # average thetaW per bp for horse sample from genome paper
# recombination rate 3X theta
rho=$(echo "$theta * 3" | bc )
echo $rho
# locus length for simulation
locus_length=3385 # length of resequenced segment of GYS1

# mutation position
mutation=1607
# mutation time
# set to 2Ne by generations or 160/60000
# try a few values for age of muation
# so mutation at 100 1000 6000 10000 20000
mut_time=(0.00167 0.0167 0.100 0.167 0.300)
# minimum frequency
min_freq=0.0001
# maximum frequency
max_freq=1.0

# number of populations
pops=1
# size of population to simulate
# need to increase size because of very recent event
pop_size=2000

# number of replicates
#reps=10000

#full path to sfs_code for simulations
SFS=~/Apps/SFSCode/bin/sfs_code
#full path to convertSFS_code for transforming simulation output
convertSFS=~/Apps/SFSCode/bin/convertSFS_CODE
# Hudson's stats program - summarizing values
stats=~/Apps/Hudson/msdir/stats

# iterating over the above arrays of the array for selection strength
# and mutation time
for selection in "${selection[@]}"
	do
		for mut_time in "${mut_time[@]}"
			do

# simulation control variables
seed=$(echo $RANDOM)

# outfile from simulations
SFS_out=$DIRECTORY/SFS_Code/outfile_sel_${selection}_mut_time_${mut_time}.txt

$SFS $pops $reps --seed $seed --sampSize 50 --theta $theta --rho $rho --length $pops $locus_length --popSize $pop_size --outfile outfile_sel_${selection}_mut_time_${mut_time}.txt --mutation $mut_time S $mutation G $selection --trackTrajectory S $mutation -F trajectory_sel_${selection}_mut_time_${mut_time}.txt
#sleep 30m
#
#$convertSFS $SFS_out --ms | msstats >msstats_sel_${selection}_mut_time_${mut_time}_out.txt

    done
done

