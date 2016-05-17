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

#Start SimuPOP program

# List of parameters/options

PopSize=10000

Mutation=0.00000005

Generations=1200

NumChrom=1 # Number of chromosomes to sample

NumLoci=1  # Number of loci on chromosome(s)

Ploidy=1  #  Ploidy.  Haploid = 1

Fitness=1.01  # Fitness value to be used for fluctuating selection

Fitness1=[Fitness, 1]  # Fitness values for each allele in environment 1

Fitness2=[1, Fitness]  # Fitness values for each allele in environment 2

Divisions=10  # Denominator of Gen equations, i.e. # by which generations is divided in order to determine frequency of environment shift

SampleDivisions=100 # Denominator of Step equation, i.e. # by which Generations is divided in order to determine how frequently allele frequencies are sampled

Step=(Generations/SampleDivisions) # How frequently are allele frequencies sampled and printed

Repetitions=3  # Number of repetitions of the simulation to run

Filename='-'.join([str(PopSize),str(Generations),str(Fitness)])



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


# Define a function that creates selection coefficients for fluctuating selection (either symmetrical or drawn randomly) as well as frequency of environmetnal shift and generation number
def GenerateSelectiveEnv(selcoeff, switches, gens):
    #   Check if selcoeff is a special value that designates random S, generate them
    if selcoeff == 'random':
        selcoeff = [random.uniform(1, 1.001) for i in range(0, switches)]
    #   Calculate how many generations will be in each stable period
    stable_period = gens/switches
    #   Create an empty list of selective coefficients, which will be appended with selective coefficient values for each "chunk" of the simulation
    coeffs = []
    while len(coeffs) < switches:
        for s in selcoeff: #why the s in selcoeff?
            coeffs.append(s) #why the (s) following the append?
    #   Generate a list of actual generation numbers where the selective coefficient changes
    #   X%Y is x modulus y; x divided by y, return the remainder
    breakpoints = [i for i in range(0, gens+1) if i%stable_period == 0]  # for every value i in the range (0-gens+1), if i/stable period returns a remainder of 0,
    # Why the 'i for i in range...?'
    #   Associate a selective coefficient with a start and end period
    sel = [] # Create an empty list that will contain appended values
    for i in range(1, len(breakpoints)): # for every value i in the range (1-(the length of the breakpoints set))
        j = i-1
        if i % 2 == 1:
            c = [coeffs[j], 1]
        else:
            c = [1, coeffs[j]]
        #  Not sure about this next line of code, need to test and see if it works
        s = simuPOP.MaSelector(loci=0, fitness=c, begin=breakpoints[j], end=breakpoints[i])
        sel.append(s)
    return(sel)
    print selcoeff

#selective_regime = [simuPOP.MaSelector(loci=0, fitness=Fitness1)]
selective_regime = GenerateSelectiveEnv(selcoeff='random', switches=12, gens=1200)


# Input the number of times you want to switch, and selection coefficients
 
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
                simuPOP.SNPMutator(u=Mutation, v=Mutation)
            ] + selective_regime,
            # # Random selection mating scheme because using haploid population without sex.  Mating parents are randomly selection from the parent population
            matingScheme = simuPOP.RandomSelection(),
            # Post mating operators
            postOps = [
                # calculate allele frequencies beginning at the (Generations/10)th generation and every (Generations/10)th generations thereafter
                simuPOP.Stat(alleleFreq=0, begin=0, step=Step), 
                # Print allele frequencies, ".3f" refers to floating decimal point with three places, "\n" moves to the next line, \t adds a tab so that the file is tab delimited and easily readable in R
                simuPOP.PyOutput(r"Iteration:" + '\t' + str(Count) + "\t", step=Step, 
                    output='>>>%s.txt' % Filename),
                simuPOP.PyEval(r"'Generation:\t%.0f\t' % (gen)", step=Step, 
                   output='>>>%s.txt' % Filename),
                simuPOP.PyEval(r"'%.3f\t' % (alleleFreq[0][0])", step=Step,
                    output='>>>%s.txt' % Filename),
                simuPOP.PyEval(r"'%.3f\n' % (1 - (alleleFreq[0][0]))", step=Step,
                    output='>>>%s.txt' % Filename),
            ],
            # Generations to run
            gen = Generations
        )
        # Add 1 to Count for next repetition/iteration
        Count = Count + 1
        # Open the output file and print to it
        print(open('%s.txt' % Filename).read())


# Run the simulation function!
simuFluctuatingSelectionWF()

print Filename