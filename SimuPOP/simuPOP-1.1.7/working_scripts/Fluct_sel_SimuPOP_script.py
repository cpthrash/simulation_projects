
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
import simuPOP.utils # Contains export function for exporting in MS format


#Define parameters in a dictionary to be used in simulation
params = {
    'PopSize':500,
    'Generations':10000,
    'Mutation':.001,
    'NumChrom':1,
    'NumLoci':1,
    'Ploidy':1,
    'Repetitions':3,
    'Switches':1000,
    'LowerSelValue':1.0,  # Lower limit of selection coefficients
    'UpperSelValue':2.0,  # Upper limit of seleciton coefficients
    'Selcoeff':'random',  # If 'random', selection coefficients will be drawn randomly from a uniform distribution
    'SelectionType':'RandomlyFluctuating', # 'Symmetrical'' for semi-symmetrical selection pressure.  'RandomlyFluctuating' for random selection pressure drawn from distribution
    'SampleDivisions':5000,
    'PopList':[] # Create an empty list 
    
}

# Define other parameters that require 'params' for calculation of value
other_params = {
    'Step':((params['Generations'])/(params['SampleDivisions']))
}

# Create a list of populations that functions as the number of replicates/iterations of the simulation
for i in range(params['Repetitions']):
    params['PopList'].append(params['PopSize'])

# Chech to make sure # generations is not less than # of environmental shifts
if (params["Switches"]) > (params["Generations"]):
   raise SystemExit('Generations must be greater than switches')


# Define a function that creates selection coefficients for fluctuating selection (either symmetrical or drawn randomly) as well as frequency of environmetnal shift and generation number
def GenerateSelectiveEnv(params):
    #Check to make sure that params and other_params are dicts, raise AssertionError if not
    try:
        assert isinstance(params, dict)
        assert isinstance(other_params, dict)
    except AssertionError:
        raise

    #   Check if selcoeff is a special value that designates random S, generate them
    if params['Selcoeff'] == 'random':
        Sel_coeff = [random.uniform(params['LowerSelValue'], params['UpperSelValue']) for i in range(0, params['Switches'])]

    #   Calculate how many generations will be in each stable period
    stable_period = (params['Generations']/params['Switches'])

    print stable_period

    #   Create an empty list of selective coefficients, which will be appended with selective coefficient values for each "chunk" of the simulation
    coeffs = []
    while len(coeffs) < params['Switches']:
        for s in Sel_coeff: 
            coeffs.append(s) 
    print(coeffs)

    #   Generate a list of actual generation numbers where the selective coefficient changes
    #   X%Y is x modulus y; x divided by y, return the remainder
    breakpoints = [i for i in range(0, params['Generations']+1) if i%stable_period == 0]  # for every value i in the range (0-gens+1), if i/stable period returns a remainder of 0,

    # Generate a list of random numbers in the desired range if implementing randomly fluctuating selection
    listselcoeff = [random.uniform(params['LowerSelValue'], params['UpperSelValue']) for i in range(0, 100000)] # Generates a list of values between 1-1.005

    #   Associate a selective coefficient with a start and end period
    sel = [] # Create an empty list that will contain appended selection coefficient values

    # If selection type is defined as 'Symmetrical', implement semi-symmetrical selection.  Otherwise, implement randomly fluctuating selection.

    if params['SelectionType'] == 'Symmetrical':
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
    return(sel, stable_period)


# Run the selective regime function
selective_regime, stable_period = GenerateSelectiveEnv(params)

# Define the filename for priting
Filename = '-'.join([str(params['PopSize']), str(params['Generations']), str(stable_period), str(params['LowerSelValue']), str(params['UpperSelValue'])])


def extractRandomSeed(): # Define a function to print the random seed for the simulation
    seed = simuPOP.getRNG().seed()
    #random.seed(seed)
    return(seed)

# Print the random seed from the simulation to the 'storeSeed.txt' file
with open('storeSeed.txt', 'a') as file:
    file.write('\n%r\n%r' % (Filename, extractRandomSeed()))
    file.close()


def simuFluctuatingSelectionWF(params, other_params): # Define a simulation function using simuPOP
    #Check to make sure that params and other_params are dicts, raise AssertionError if not
    try:
        assert isinstance(params, dict)
        assert isinstance(other_params, dict)
    except AssertionError:
        raise

    
    pop = simuPOP.Population(size=tuple(params['PopList']), loci=params['NumLoci'], ploidy=params['Ploidy'], # 'tuple(params['PopList']' inserts the number of populations that serves as the number of replicates/iterations, which is defined in the params dict

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
            simuPOP.SNPMutator(u=params['Mutation'], v=params['Mutation'])] + selective_regime,

        # # Random selection mating scheme because using haploid population without sex. Parents are randomly selected from the parent population to give birth
        matingScheme = simuPOP.RandomSelection(),

        # Post mating operators - only use when need to calculate and print allele frequencies

        # postOps = [

        
            # calculate allele frequencies 
            # simuPOP.Stat(alleleFreq=0, begin=0, step=other_params['Step']), 

            # Print allele frequencies, ".3f" refers to floating decimal point with three places, "\n" moves to the next line, \t adds a tab so that the file is tab delimited and easily readable in R
            #simuPOP.PyOutput(r"Iteration:" + '\t' + str(Count) + "\t", step=other_params['Step'], 
            #    output='>>%s.txt' % Filename),
            #simuPOP.PyEval(r"'Generation:\t%.0f\t' % (gen)", step=other_params['Step'], 
            #    output='>>%s.txt' % Filename),
            #simuPOP.PyEval(r"'%.3f\t' % (alleleFreq[0][0])", step=other_params['Step'],
            #    output='>>%s.txt' % Filename),
            #simuPOP.PyEval(r"'%.3f\n' % (1 - (alleleFreq[0][0]))", step=other_params['Step'],
            #    output='>>%s.txt' % Filename)
        
        # ,
        # ],

        
        # Generations to run
        gen =params['Generations']
    )


    simuPOP.utils.export(pop, format='ms', output=('MS-%s.txt' % Filename), gui=False, splitBy='subPop') # Export the data in MS format

    print(open('MS-%s.txt' % Filename).read())  # 
    
    #print(open('%s.txt' % Filename).read())  # Open the output file and print to it

    # Extract and print the random seed
    extractRandomSeed()


# Run the simulation function!
simuFluctuatingSelectionWF(params, other_params)

print('MS-%s.txt' % Filename)