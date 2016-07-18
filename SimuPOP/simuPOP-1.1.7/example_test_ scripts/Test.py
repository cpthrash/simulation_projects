#!/usr/bin/env python


#Author: Colin Pierce

"""
This script is intended to elucidate allele frequencies in a haploid population 
that is undergoing fluctuating selection.  Future iterations of the script will be 
used to uncover allele frequencies using the Moran model of overlapping generations.
"""

import os, sys, types, time # Not used currently 
import simuOpt # Not used currently
import simuPOP
import random # random module used to generate a random number for when the selection pressure is chosen at random each environmental shift
import simuPOP.utils


#Define parameters to be used in simulation
params = {
    'popsize':1000,
    'gens':1200,
    'switches':12,
    'lowerselvalue':0.5,
    'upperselvalue':1.5
}

print(params['popsize'])



# Define a function that creates selection coefficients for fluctuating selection (either symmetrical or drawn randomly) as well as frequency of environmetnal shift and generation number

def GenerateSelectiveEnv(selcoeff, switches, gens, SelectionType, LowerSelValue, UpperSelValue, params):
    #Check to make sure that params is a dict, raise AssertionError if not
    try:
        assert isinstance(params, dict)
    except AssertionError:
        raise

    #   Check if selcoeff is a special value that designates random S, generate them
    if selcoeff == 'random':
        selcoeff = [random.uniform(params['lower'], params['upper']) for i in range(0, params['switches'])]
        selcoeff = [random.uniform(LowerSelValue, UpperSelValue) for i in range(0, switches)]

    Filename='-'.join([str(PopSize),str(stable_period), str(LowerSelValue), str(UpperSelValue)])

    print Filename

    #   Calculate how many generations will be in each stable period
    stable_period = gens/switches

    #   Create an empty list of selective coefficients, which will be appended with selective coefficient values for each "chunk" of the simulation
    coeffs = []
    while len(coeffs) < switches:
        for s in selcoeff: 
            coeffs.append(s) 
    print(coeffs)

    #   Generate a list of actual generation numbers where the selective coefficient changes
    #   X%Y is x modulus y; x divided by y, return the remainder
    breakpoints = [i for i in range(0, gens+1) if i%stable_period == 0]  # for every value i in the range (0-gens+1), if i/stable period returns a remainder of 0,

    # Generate a list of random numbers in the desired range if implementing randomly fluctuating selection
    listselcoeff = [random.uniform(1, UpperSelValue) for i in range(0, 100000)] # Generates a list of values between 1-1.005

    #   Associate a selective coefficient with a start and end period
    sel = [] # Create an empty list that will contain appended selection coefficient values

    # If selection type is defined as 'Symmetrical', implement semi-symmetrical selection.  Otherwise, implement randomly fluctuating selection.

    if SelectionType == 'Symmetrical':
        for i in range(1, len(breakpoints)): # for every value i in the range (1-(the length of the breakpoints set))
            j = i-1
            if i % 2 == 1:
                c = [coeffs[j], 1]
            else:
                c = [1, coeffs[j]]
            #  Not sure about this next line of code, need to test and see if it works
            s = simuPOP.MaSelector(loci=0, fitness=c, begin=breakpoints[j], end=breakpoints[i])
            print c
            sel.append(s)   
    else:
        for i in range(1, len(breakpoints)):
            j = i-1
            c = random.sample(listselcoeff, 2)
        #   Change this line to make a simuPOP.MaSelector object instead of a tuple
            s = simuPOP.MaSelector(loci=0, fitness=c, begin=breakpoints[j], end=breakpoints[i])
            print c
            sel.append(s)
    return(sel, switches, gens, stable_period, LowerSelValue, UpperSelValue, Filename)



# If 'SelectionType' = 'Symmetrical', then (somewhat) symmetrical selection wil be implemented.  Otherwise randomly fluctuating selection (where selection coefficients are chosen at random for both alleles) will be implemented
# UpperSelValue is the maximum possible selection coefficient.  

selective_regime, switches, gens, stable_period, LowerSelValue, UpperSelValue, Filename = GenerateSelectiveEnv(selcoeff='random', switches=12, gens=200, SelectionType='RandomlyFluctuating', LowerSelValue=0.5, UpperSelValue=1.005)



# Define a function to print the random seed for the simulation
def extractRandomSeed():
    seed = simuPOP.getRNG().seed()
    #random.seed(seed)
    print(seed)


# Define a simulation function using simuPOP
 
def simuFluctuatingSelectionWF(PopSize, Mutation, Generations, NumChrom, NumLoci, Ploidy, Repetitions):
    
    # Start count at 0 for loop
    Count = 0

    # Number of repetitions of the simulation to run
    Reps = Repetitions  

    # Divisions=10  # Denominator of Gen equations, i.e. # by which generations is divided in order to determine frequency of environment shift

    #Repetitions=3  # Number of repetitions of the simulation to run

    SampleDivisions=100 # Denominator of Step equation, i.e. # by which Generations is divided in order to determine how frequently allele frequencies are sampled

    Step=(Generations/SampleDivisions) # How frequently are allele frequencies sampled and printed

    Filename='-'.join([str(PopSize),str(stable_period), str(LowerSelValue), str(UpperSelValue)])

    print Filename

    return(Filename)

    # Run the loop only when the count is less than the # reps
    while Count < (Reps):

        # initialize Population
        # set population size, loci, ploidy
        pop = simuPOP.Population(size=[PopSize, PopSize], loci=NumLoci, ploidy=Ploidy, 

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
                simuPOP.SNPMutator(u=Mutation, v=Mutation)] + selective_regime,

            # # Random selection mating scheme because using haploid population without sex.  Mating parents are randomly selection from the parent population
            matingScheme = simuPOP.RandomSelection(),

            # Post mating operators
            postOps = [

                # calculate allele frequencies 
                simuPOP.Stat(alleleFreq=0, begin=0, step=Step), 

                # Print allele frequencies, ".3f" refers to floating decimal point with three places, "\n" moves to the next line, \t adds a tab so that the file is tab delimited and easily readable in R
                simuPOP.PyOutput(r"Iteration:" + '\t' + str(Count) + "\t", step=Step, 
                    output='>>%s.txt' % Filename),
                simuPOP.PyEval(r"'Generation:\t%.0f\t' % (gen)", step=Step, 
                   output='>>%s.txt' % Filename),
                simuPOP.PyEval(r"'%.3f\t' % (alleleFreq[0][0])", step=Step,
                    output='>>%s.txt' % Filename),
                simuPOP.PyEval(r"'%.3f\n' % (1 - (alleleFreq[0][0]))", step=Step,
                    output='>>%s.txt' % Filename),
            ],
            
            # Generations to run
            gen = Generations 
        )

        # Add 1 to Count for next repetition/iteration
        Count = Count + 1


        simuPOP.utils.export(pop, format='ms', output='ms.txt', gui=False, splitBy='subPop')
        # export first chromosome, subpops as replicates
        #export(pop, format='ms', output='ms_subPop.txt', splitBy='subPop')
        # export all chromosomes, but limit to all males in subPop 1
        #pop.setVirtualSplitter(sim.SexSplitter())
        #export(pop, format='ms', output='ms_chrom.txt', splitBy='chrom', subPops=[(1,0)])



        print(open('ms.txt').read())
        
        # Open the output file and print to it
        print(open('%s.txt' % Filename).read())

        # Extract and print the random seed
        extractRandomSeed()



# If 'SelectionType' = 'Symmetrical', then (somewhat) symmetrical selection wil be implemented.  Otherwise randomly fluctuating selection (where selection coefficients are chosen at random for both alleles) will be implemented
# UpperSelValue is the maximum possible selection coefficient.  Can be anything above 1.0, biologically realistic selective coefficients are generally close to 1.0

selective_regime, switches, gens, stable_period, LowerSelValue, UpperSelValue = GenerateSelectiveEnv(selcoeff='random', switches=12, gens=200, SelectionType='RandomlyFluctuating', LowerSelValue=0.5, UpperSelValue=1.005)


# Run the simulation function!
simuFluctuatingSelectionWF(PopSize=100, Mutation=0.000005, Generations=200, NumChrom=1, NumLoci=50, Ploidy=1, Repetitions=10)

print Filename