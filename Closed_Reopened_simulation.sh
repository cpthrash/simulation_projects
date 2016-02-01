#!/usr/bin/env bash

set -e
set -u
set -o pipefail

module load python-epd
module load molpopgen
module load R

# location of programs
MS=~/Documents/ms/msdir/ms
FF=~/Documents/ms/msdir/ms_FreqFilter.py
MSSTATS=~/msstats_varPi/src/msstats

replicates=100000
theta=150
rho=1000
locus_length=1000

# first, simulate the ancestral pop (N1)
# using Tom's frequency filter code, where -p 8 is panel depth, -f 3 is (minimum) frequency
$MS 120 $replicates -t $theta -r $rho $locus_length | python $FF -p 8 -f 3 | $MSSTATS > P_anc

# second, simulate the bottleneck (N2) and the closed pop (N3) to get the optimal bottleneck size and duration 
# below is R code for creating prior distributions
R --no-save <<EOF
setwd("~/Documents/ms/msdir")
# size of N2
write(runif(100000,0,0.05),file="prior_div",ncolumns=1)
# the end of bottleneck from (15,120 generations), 15/4Ne=0.000025, 120/4Ne=0.00025
write(runif(100000,0.000025,0.008),file="prior_T",ncolumns=1)
EOF
# create file with two sets of priors
paste prior_T prior_div > prior2

$MS 240 $replicates -t $theta -r $rho $locus_length \
# 2 pops, the diversity of the closed pop is 0.025 of N1, The bottleneck started at 8000/4*N0 = 0.013, so at that time, lineage 2 moves to lineage 1
-I 2 120 120 -n 2 0.025 -en tbs 2 tbs -ej 0.0133 2 1 < prior2  \
| python $FF -p 8 -f 3 | $MSSTATS -I 2 120 120 | cut -f 7 > P_close

# finally, simulate all pops together 
# prior for migration rate
R --no-save <<EOF
write(runif(100000,0,10000),file="prior_m",ncolumns=1)
EOF

# 3 pops, the diversity of the reopened pop is 0.09 of N1, the start of the reopened pop 0.000025
$MS 360 $replicates -t $theta -r $rho $locus_length -I 3 120 120 120 -n 2 0.025 -en 0.0015 2 0.01 -n 3 0.09 -ej 0.0133 2 1 -m 3 1 tbs -ej 0.000025 3 2 < prior_m | python $FF -p 8 -f 3 | $MSSTATS -I 3 120 120 120 | cut -f 7 > P_open 

