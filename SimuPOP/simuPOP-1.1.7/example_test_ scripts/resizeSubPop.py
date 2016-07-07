import simuPOP 
pop = simuPOP.Population([100]*2)
pop.evolve(
    preOps=[
        simuPOP.ResizeSubPops(sizes=(101, 150), at=(1, 3)),
        simuPOP.ResizeSubPops(sizes=(99, 200), at=(2,4)),
        simuPOP.Stat(popSize=True),
        simuPOP.PyEval(r'"Gen %d:\t%s\n" % (gen, subPopSize)')
    ],
    matingScheme=simuPOP.RandomSelection(),
    gen = 6
)