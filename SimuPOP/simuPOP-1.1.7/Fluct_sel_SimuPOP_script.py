#!/usr/bin/env python

#Author: Colin Pierce

"""
This script is intended to elucidate allele frequencies in a haploid population 
that is undergoing fluctuating selection.  Future iterations of the script will be 
used to uncover allele frequencies using the Moran model of overlapping generations.
"""

import os, sys, types, time 
import simuOpt 
import simuPOP

#Start SimuPOP program

# List of parameters/options

PopSize=10000

Mutation=0.00000005

Generations=5001

Step=(Generations/10) # How frequently are allele frequencies sampled and printed

NumChrom=1 # Number of chromosomes to sample

NumLoci=1  # Number of loci on chromosome(s)

Ploidy=1  #  Ploidy.  Haploid = 1

Fitness1=[1.005, 1]  # Fitness values for each allele in environment 1

Fitness2=[1, 1.005]  # Fitness values for each allele in environment 2

Repetitions=10  # Number of repetitions of the simulation to run


# Calculate # generations at which allele frequency will be calculated based on total number of generations

Gen0=0

Gen1=Generations/10

Gen2=(Generations/10)+(Generations/10)

Gen3=(Generations/10)+Gen2

Gen4=(Generations/10)+Gen3

Gen5=(Generations/10)+Gen4

Gen6=(Generations/10)+Gen5

Gen7=(Generations/10)+Gen6

Gen8=(Generations/10)+Gen7

Gen9=(Generations/10)+Gen8

Gen10=(Generations/10)+Gen9


 
def simuFluctuatingSelectionWF():
    
    Count = 1

    # Number of repetitions of the simulation to run
    Reps = Repetitions  

    while Count <= Reps:

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
                simuPOP.PyEval(r"'Generation: %.0f\n' % (gen)", step=Step),
                simuPOP.PyEval(r"'f(A): %.3f\n' % (alleleFreq[0][0])", step=Step),
                simuPOP.PyEval(r"'f(a): %.3f\n' % (alleleFreq[0][1])", step=Step),


                    ],
            
            # program run over set amount of generations
            gen = Generations 
        )
# Run the simulation function!
simuFluctuatingSelectionWF()

