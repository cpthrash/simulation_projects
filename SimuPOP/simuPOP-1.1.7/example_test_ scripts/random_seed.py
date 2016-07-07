import simuPOP as sim
import random
def simulate():
    pop = sim.Population(1000, loci=10, infoFields='age')
    pop.evolve(
        initOps=[
            sim.InitSex(),
            sim.InitGenotype(freq=[0.5, 0.5]),
            sim.InitInfo(lambda: random.randint(0, 10), infoFields='age')
        ],
        matingScheme=sim.RandomMating(),
        finalOps=sim.Stat(alleleFreq=0),
        gen=100
    )
    return pop.dvars().alleleFreq[0][0]

seed = sim.getRNG().seed()
#random.seed(seed)
print(seed)
print('%.4f' % simulate())
# will yield different result
print('%.4f' % simulate())
sim.setRNG(seed=seed)
random.seed(seed)
# will yield identical result because the same seeds are used
print('%.4f' % simulate())