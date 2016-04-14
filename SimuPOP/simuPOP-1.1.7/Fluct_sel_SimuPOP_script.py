#!/usr/bin/env python

#Author: Colin Pierce

"""
This script is intended to elucidate allele frequencies in a haploid population 
that is undergoing fluctuating selection.  Future iterations of the script will be 
used to uncover allele frequencies using the Moran model of overlapping generations.
"""

import os, sys, types, time #not sure if all of these are needed, depends on modules to be used
import simuOpt # probably will need to import more modules here
import simuPOP as sim

#Start SimuPOP program

# List of parameters/options
PopSize=1000

Mutation=0.005

Generations=5001

Step=500

NumChrom=1

NumLoci=1

Ploidy=1

Fitness1=[1.01, 1]

Fitness2=[1, 1.01]



 # initialize Population
 # set population size
# create field at where allele frequency values can be stored
pop = sim.Population(size=10000, loci=NumLoci, ploidy=Ploidy, infoFields=['alleleFreq', 'fitness'])
    
    # Evolve the population!
pop.evolve(
        # Initial Operators
    initOps = [ 
    sim.InitGenotype(freq=[0.5, 0.5]) # Sets initial allele frequencies
    ],

        # Pre-mating operators
    preOps = [
        # begin evolve function
        sim.SNPMutator(u=Mutation, v=Mutation), # "u" specifies Allele 1->allele 2 mutation rate, "v" is opposite

            # Fitness effects (i.e. the environment) change every 500 generations
        sim.MaSelector(loci=0, fitness=Fitness1, begin=0, end=500), 
        sim.MaSelector(loci=0, fitness=Fitness2, begin=500, end=1000),
        sim.MaSelector(loci=0, fitness=Fitness1, begin=1000, end=1500),
        sim.MaSelector(loci=0, fitness=Fitness2, begin=1500, end=2000),
        sim.MaSelector(loci=0, fitness=Fitness1, begin=2000, end=2500),
        sim.MaSelector(loci=0, fitness=Fitness2, begin=2500, end=3000),
        sim.MaSelector(loci=0, fitness=Fitness1, begin=3000, end=3500),
        sim.MaSelector(loci=0, fitness=Fitness2, begin=3500, end=4000),
        sim.MaSelector(loci=0, fitness=Fitness1, begin=4000, end=4500),
        sim.MaSelector(loci=0, fitness=Fitness2, begin=4500, end=5000)

    ],
    matingScheme = sim.RandomSelection(),
    postOps = [
            # calculate allele frequencies beginning at the 500th generation and every 500 generations thereafter
        sim.Stat(alleleFreq=0, begin=0, step=Step), #
            # Print allele frequencies, ".3f" refers to floating decimal point with three places, "\n" moves to the next line
        sim.PyEval(r"'Generation: %.3f\n' % (gen)", step=Step),
        sim.PyEval(r"'f(A): %.3f\n' % (alleleFreq[0][0])", step=Step),
        sim.PyEval(r"'f(a): %.3f\n' % (alleleFreq[0][1])", step=Step),


            ],
        # program run over set amount of generations
    gen = Generations 
)



