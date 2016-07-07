import simuPOP
import simuPOP.utils as utils
#pop = simuPOP.Population(20, loci=[10, 10])
# simulate a population but mutate only a subset of loci
#pop.evolve(
#   preOps=[
#        simuPOP.InitSex(),
#        simuPOP.SNPMutator(u=0.1, v=0.01, loci=range(5, 17))
#    ],
#    matingScheme=simuPOP.RandomMating(),
#    gen=100
#)

# 

# import as haploid sequence
#pop = importPopulation(format='ms', filename='ms.txt')
# import as diploid 
#pop = importPopulation(format='ms', filename='ms.txt', ploidy=2)
# import as a single chromosome
#pop = importPopulation(format='ms', filename='ms_subPop.txt', mergeBy='subPop')


def simuFluctuatingSelectionWF(Repetitions):
    
    # Start count at 0 for loop
    Count = 0

    # Number of repetitions of the simulation to run
    Reps = Repetitions

    # Divisions=10  # Denominator of Gen equations, i.e. # by which generations is divided in order to determine frequency of environment shift

    #Repetitions=3  # Number of repetitions of the simulation to run

    #SampleDivisions=100 # Denominator of Step equation, i.e. # by which Generations is divided in order to determine how frequently allele frequencies are sampled

    #Step=(Generations/SampleDivisions) # How frequently are allele frequencies sampled and printed

    #Filename='-'.join([str(PopSize),str(Generations)])

   # print Filename

    # Run the loop only when the count is less than the # reps

    while Count < (Reps):

        pop = simuPOP.Population([20, 20], loci=[10, 10])
        # simulate a population but mutate only a subset of loci
        pop.evolve(
            preOps=[
            simuPOP.SNPMutator(u=0.1, v=0.01, loci=range(5, 17))
            ],
            matingScheme=simuPOP.RandomSelection(),
            gen=100
            )


        # Add 1 to Count for next repetition/iteration
    Count = Count + 1

simuFluctuatingSelectionWF(Repetitions=3)

# export first chromosome, all individuals
utils.export(pop, format='ms', output='ms.txt', gui=False)
# export first chromosome, subpops as replicates
#export(pop, format='ms', output='ms_subPop.txt', splitBy='subPop')
# export all chromosomes, but limit to all males in subPop 1
#pop.setVirtualSplitter(sim.SexSplitter())
#export(pop, format='ms', output='ms_chrom.txt', splitBy='chrom', subPops=[(1,0)])

print(open('ms.txt').read())