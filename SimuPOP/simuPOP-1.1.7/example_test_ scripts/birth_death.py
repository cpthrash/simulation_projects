import random
import simuPOP

pop = simuPOP.Population(1000, ploidy=1, loci=2, infoFields='fitness')

# initialize genotype
simuPOP.initGenotype(pop, [0.5, 0.5])

# some arbitrary fitness model
def model(geno):
    return [0.9, 0.95, 1][geno[0] + geno[1]]

# assign fitness to everyone
# When this operator is applied to a population, it passes genotypes or mutants at specified loci, generation number, a reference to an individual, a reference to the current population (usually used to retrieve population variable), and values at specified information fields to respective parameters of this function. Genotypes are passed as a tuple of alleles arranged locus by locus (in the order of A1,A2,B1,B2 for loci A and B). Mutants are passed as a default dictionary of loci index (with respect to all genotype of individuals, not just the first ploidy) and alleles. The returned value will be used to determine the fitness of each individual.
# The function called upon is the 'model' function defined above.  Will need to tailor that for my simulations
simuPOP.PySelector(loci=[0, 1], func=model).apply(pop)

#print(pop.indInfo('fitness'))

for gen in range(1000):
    # find one random guy to remove
    # DEATH
    removed = random.randint(0, pop.popSize() - 1)
    fitness = list(pop.indInfo('fitness'))
    fitness[removed] = 0
    # BIRTH
    sampler = simuPOP.WeightedSampler(fitness)
    selected = sampler.draw()
    new_individual = removed # HAVE BIRTH REPLACE DEATH

    # copy genotype - next 4 lines are from simuPOP documentation
    #setGenotype(geno, subPop=[]) 
        #Fill the genotype of all individuals in a population (if subPop=[]) or in a (virtual) subpopulation subPop (if subPop=sp or (sp, vsp)) using a list of alleles geno. geno will be reused if its length is less than subPopSize(subPop)*totNumLoci()*ploidy()
    # setGenotype(geno, ploidy=ALL_AVAIL, chroms=ALL_AVAIL)
        #Fill the genotype of an individual using a list of alleles geno. If parameters ploidy and/or chroms are specified, alleles will be copied to only all or specified chromosomes on selected homologous copies of chromosomes. geno will be reused if its length is less than number of alleles to be filled. This function ignores type of chromosomes so it will set genotype for unused alleles for sex and mitochondrial chromosomes.
    # ADD BIRTH TO POPULATION
    pop.individual(new_individual).setGenotype(pop.individual(selected).genotype())

    # set fitness
    pop.individual(new_individual).fitness = model(pop.individual(new_individual).genotype())