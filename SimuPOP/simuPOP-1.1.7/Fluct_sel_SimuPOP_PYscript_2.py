#!/usr/bin/env python

#Author: Colin Pierce

"""
This script is intended to elucidate allele frequencies in a haploid population 
that is undergoing fluctuating selection.  Future iterations of the script will be 
used to uncover allele frequencies using the Moran model of overlapping generations.
"""



import os, sys, types, time #not sure if all of these are needed, depends on modules to be used
import simuOpt # probably will need to import more modules here
import  simuPOP as sim

#Start SimuPOP program

# List of Options/parameters that will be called on in simulation
options = [
    {
     'name':'PopSize',
     'default':10000,
     'label':'Population Size',
     'type':[int, long],
     'validator':simuOpt.valueGT(0),
     },
    {
     'name':'Mutation',
     'default':0.001,
     'label':'Mutation Rate',
     'type':[float],
     'validator':simuOpt.valueBetween(0., 1.),
     },
    {
     'name':'Generations',
     'default':10000,
     'label':'Generations to evolve',
     'description':'Length of evolution',
     'type':[int, long],
     'validator':simuOpt.valueGT(0)
     },
    {
     'name':'Step',  # How many steps (in number of generations) to sample allele frequencies
     'default':100,
     'label':'Steps to take per generation',
     'description':'Values displayed per generation',
     'type':[int, long],
     'validator':simuOpt.valueGT(0)
     },  
    {
     'name': 'NumChrom',
     'default':1,
     'label': 'Number of chromosomes',
     'description': 'Number of chromosomes.',
     'type': [int],
     'validator':    simuOpt.valueGT(0)
    },
     {
     'name': 'NumLoci',
     'default':1,
     'label': 'Number of loci on each chrom',
     'description': '''Number of loci on each chromosome, current there 
             only equal number of markers on each chromosome is supported.''',
     'type': [int],
     'validator':    simuOpt.valueGT(0)
    },
    { # Don't need burn-in when specifying initial allele frequencies
     'name': 'BurninGen',
     'default':100,
     'label': 'Length of burn-in stage',
     'type': [int],
     'description': 'Number of generations of the burn in stage.',
     'validator':    simuOpt.valueGT(0)
    },
    {
     'name': 'EndingGen',
     'default':10000,
     'label': 'Ending generation number',
     'type': [int, long],
     'description': '''At which generation to stop the simulation.
                This is the total generation number.''',
     'validator':    simuOpt.valueGE(0)
    },
    {
    'name': 'AncGen',
    'default':10,
    'label': 'Number of ancestral generations',
    'type': [int],
    'description': 'Number of ancestral generations to be tracked for allele frequencies',
    'validator':    simuOpt.valueGE(0),
    },
    {
    'name': 'Ploidy',
    'default':1,
    'label': "Ploidy",
    'type': [int],
    'description': 'Chromosome copy number',
    'validator':    simuOpt.valueGE(0),
    },
    {
    'name': 'Fitness1',  
     'default': [1.05, 1],
     'label': 'Fitness of genotypes A,a in environment 1',
     'type': [types.ListType, types.TupleType],
     'description': ' Genotype A has fitness advantage',
     'validator':    simuOpt.valueListOf(simuOpt.valueGE(0.)),
    },
    {
     'name': 'Fitness2',  
     'default': [1, 1.05],
     'label': 'Fitness of genotypes A,a in environment 2',
     'type': [types.ListType, types.TupleType],
     'description': 'Genoype a has fitness advantage',
     'validator':    simuOpt.valueListOf(simuOpt.valueGE(0.)),
    },
    {'name': 'name',
     'default': 'simu',
     'type': [str],
     'label': 'Simulation name',
     'description': '''Name of simulation, files saved will be 
                    name + '.log': statistics output
                    name + '.cfg': configuration
                    name + .bin/txt/xml: saved popuation''',
    },
]

# Define a function for fluctuating selection
def lotsOfFitness(fitness1, fitness2, begin, end, step, loci):
	selectionList = [] # Making an empty list as a placeholder
	generations = range(begin, end + step, step) # Python counts from 0 to n-1, complete list of all start and ending generations
	for i in range(len(generations) - 1):
		if i % 2 == 0:
			selectionList += [MaSelector(loci=loci, fitness=fitness1, begin=generations[i], end=generations[i + 1])]
		else:
			selectionList += [`MaSelector(loci=loci, fitness=fitness2, begin=generations[i], end=generations[i + 1])]
	return selectionList


# Define a function for the simulation
def simuFluctuatingSelectionWF(PopSize, mutation, generations, step, numChrom, numLoci, burninGen, endingGen, fitness):
 

    # Save population at given generation
    if len(savePop) > 0:
        # save population at given generations
        postOperators.append(SavePopulation(outputExpr='os.path.join(name, "%s_%d.%s" % (name, gen, format))', 
            at=savePop))

    # initialize Population
    # set population size
    # create field at where allele frequency values can be stored
    pop = Population(size=PopSize, loci=NumLoci, ploidy=Ploidy, infoFields='alleleFreq')
    
    # Evolve the population!
    pop.evolve(
        # Initial Operators
        initOps = [ 
        InitGenotype(genotype=[0.5, 0.5]) # Sets initial allele frequencies
        ],

        # Pre-mating operators
        preOps = [SNPMutator(u=mutation, v=mutation)] + lotsofFitness(fitness1, fitness2, begin, end, step, loci),
        matingScheme = RandomMating(),
        postOps = [
            # calculate allele frequencies beginning at the 500th generation and every 500 generations thereafter
            Stat(alleleFreq=0, begin=0, step=500), #
            # Print allele frequencies, ".3f" refers to floating decimal point with three places, "\n" moves to the next line
            PyEval(r"'%.3f\n' alleleFreq[0]", begin=500)
        ],
        # program run over set amount of generations
        gen = generations 
)

if __name__ == '__main__':
    # get parameters
    par = simuOpt.Params(options, 
      '''This program simulates the evolution of 2 alleles in a fluctuating environment.''', __doc__)
    if not par.getParam():
        sys.exit(1)

   # if not os.path.isdir(par.name):
    #    os.makedirs(par.name)
     #   par.saveConfig(os.path.join(par.name, par.name + '.cfg'))

# unpack options 

    (PopSize, Mutation, Generations, Step, NumChrom, NumLoci, BurninGen, EndingGen,
        AncGen, Ploidy, Fitness1, Fitness2, name) = par.asList()
    
#  This is from "Exanmple_SimuPOP.py script, need to modify options for this script
    #   (numChrom, numLoci, markerType, DSLafter, DSLdist, 
    #   initSize, endingSize, growthModel, 
    #    burninGen, splitGen, mixingGen, endingGen, 
    #    numSubPop, migrModel, migrRate, alleleDistInSubPop,
    #    curAlleleFreq, minMutAge, maxMutAge, fitness, selMultiLocusModel,
    #    utaRate, recRate, savedGen, numOffspring, numOffMode,
    #    dryrun, savePop, name) = par.asList()

# params.setOptions(quiet=True)
# need to modify options for this script

    ################## RUN THE SIMULATION ###############
(PopSize, Mutation, Generations, Step, NumChrom, NumLoci, BurninGen, EndingGen,
        AncGen, Ploidy, Fitness1, Fitness2, os.path.join(name, name + '.pop')) 

# This is from "Exanmple_SimuPOP.py script,
#    simuFluctuatingSelectionWF(numChrom, numLoci, markerType, DSLafter, DSLdist, 
#    initSize, endingSize, growthModel, burninGen, splitGen, mixingGen, endingGen, 
#    numSubPop, migrModel, migrRate, alleleDistInSubPop, curAlleleFreq, minMutAge, 
#    maxMutAge, fitness, selMultiLocusModel, mutaRate, recRate, savedGen, 
#    numOffspring, numOffMode, dryrun, savePop, os.path.join(name, name + '.pop'))
    
# Need to figure out how to have output file named based on Pop size, mutation, generations
print "Done!"







