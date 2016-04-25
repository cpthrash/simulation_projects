#!/usr/bin/env python

#PBS -l mem=8000mb,nodes=1:ppn=1,walltime=72:00:00
#PBS -m abe
#PBS -M pier0273@umn.edu
#PBS -q lab

#Author: Colin Pierce

"""
This script is intended to elucidate allele frequencies in a haploid population 
that is undergoing fluctuating selection.  Future iterations of the script will be 
used to uncover allele frequencies using the Moran model of overlapping generations.
"""

import os, sys, types, time # Not used currently 
import simuOpt # Not used currently
import simuPOP

#Start SimuPOP program

# List of parameters/options

PopSize=10000

Mutation=0.00000005

Generations=5001

NumChrom=1 # Number of chromosomes to sample

NumLoci=1  # Number of loci on chromosome(s)

Ploidy=1  #  Ploidy.  Haploid = 1

Fitness1=[1.005, 1]  # Fitness values for each allele in environment 1

Fitness2=[1, 1.005]  # Fitness values for each allele in environment 2

Divisions=10  # Denominator of Step equation, i.e. # by which generations is divided in order to determine frequency of allle sampling

Step=(Generations/Divisions) # How frequently are allele frequencies sampled and printed

Repetitions=2  # Number of repetitions of the simulation to run


# Calculate # generations at which allele frequency will be calculated based on total number of generations

Gen0=0

Gen1=Generations/Divisions

Gen2=(Generations/Divisions)+(Generations/Divisions)

Gen3=(Generations/Divisions)+Gen2

Gen4=(Generations/Divisions)+Gen3

Gen5=(Generations/Divisions)+Gen4

Gen6=(Generations/Divisions)+Gen5

Gen7=(Generations/Divisions)+Gen6

Gen8=(Generations/Divisions)+Gen7

Gen9=(Generations/Divisions)+Gen8

Gen10=(Generations/Divisions)+Gen9


 
def simuFluctuatingSelectionWF():
    
    # Start count at 0 for loop
    Count = 0

    # Number of repetitions of the simulation to run
    Reps = Repetitions  

    # Run the loop only when the count is less than the # reps
    while Count < (Reps):

        # initialize Population
        # set population size, loci, ploidy
        pop = simuPOP.Population(size=PopSize, loci=NumLoci, ploidy=Ploidy, 

            # create fields where allele frequency and fitness values can be stored
            infoFields=['alleleFreq', 'fitness'])
            
        # Evolve the population!
        pop.evolve(

            # Initial Operators
            initOps = [ 

                # Sets initial allele frequencies
                simuPOP.InitGenotype(freq=[0.5, 0.5]) 
            ],

            # Pre-mating operators
            preOps = [

                # "u" specifies Allele 1->allele 2 mutation rate, "v" is opposite
                simuPOP.SNPMutator(u=Mutation, v=Mutation), 

                # Fitness effects (i.e. the environment) change every 500 generations
                simuPOP.MaSelector(loci=0, fitness=Fitness1, begin=Gen0, end=Gen1), 
                simuPOP.MaSelector(loci=0, fitness=Fitness2, begin=Gen1, end=Gen2),
                simuPOP.MaSelector(loci=0, fitness=Fitness1, begin=Gen2, end=Gen3),
                simuPOP.MaSelector(loci=0, fitness=Fitness2, begin=Gen3, end=Gen4),
                simuPOP.MaSelector(loci=0, fitness=Fitness1, begin=Gen4, end=Gen5),
                simuPOP.MaSelector(loci=0, fitness=Fitness2, begin=Gen5, end=Gen6),
                simuPOP.MaSelector(loci=0, fitness=Fitness1, begin=Gen6, end=Gen7),
                simuPOP.MaSelector(loci=0, fitness=Fitness2, begin=Gen7, end=Gen8),
                simuPOP.MaSelector(loci=0, fitness=Fitness1, begin=Gen8, end=Gen9),
                simuPOP.MaSelector(loci=0, fitness=Fitness2, begin=Gen9, end=Gen10)

            ],

            # # Random selection mating scheme because using haploid population without sex.  Mating parents are randomly selection from the parent population
            matingScheme = simuPOP.RandomSelection(),

            # Post mating operators
            postOps = [

                # calculate allele frequencies beginning at the (Generations/10)th generation and every (Generations/10)th generations thereafter
                simuPOP.Stat(alleleFreq=0, begin=0, step=Step), 

                # Print allele frequencies, ".3f" refers to floating decimal point with three places, "\n" moves to the next line

                # Print iteration number to screen
                simuPOP.PyOutput(r"Iteration:" + '\t' + str(Count) + "\t", step=Step),  

                #Might want to calculte second allele frequency as (1-p)
                simuPOP.PyEval(r"'Generation: %.0f\n' % (gen)", step=Step),
                simuPOP.PyEval(r"'f(A): %.3f\n' % (alleleFreq[0][0])", step=Step),
                simuPOP.PyEval(r"'f(a): %.3f\n' % (alleleFreq[0][1])", step=Step),


            ],
            
            # program run over set amount of generations
            gen = Generations 
        )

        # Add 1 to Count for next repetition
        Count = Count + 1

# Run the simulation function!
simuFluctuatingSelectionWF()

