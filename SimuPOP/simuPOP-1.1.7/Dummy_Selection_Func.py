#!/usr/bin/env python

import random

def GenerateSelectiveEnv(selcoeff, switches, gens):
	#	Check if selcoeff is a special value that designates random S, generate them
	if selcoeff == 'random':
		selcoeff = [random.uniform(1, 1.5) for i in range(0, switches)]
	#	Calculate how many generations will be in each stable period
	stable_period = gens/switches
	#	Create a list of selective coefficients for each "chunk" of the simulation
	coeffs = []
	while len(coeffs) < switches:
		for s in selcoeff:
			coeffs.append(s)
	#	Generate a list of actual generation numbers where the selective coefficient changes
	#	X%Y is x modulus y; x divided by y, return the remainder
	breakpoints = [i for i in range(0, gens+1) if i%stable_period == 0]
	#	Associate a selective coefficient with a start and end period
	sel = []
	for i in range(1, len(breakpoints)):
		j = i-1
		#	Change this line to make a simuPOP.MaSelector object instead of a tuple
		s = (coeffs[j], breakpoints[j], breakpoints[i])
		sel.append(s)
	return(sel)


selective_regime = GenerateSelectiveEnv(selcoeff=[0, 0.5], switches=10, gens=1000)
print selective_regime
selective_regime2 = GenerateSelectiveEnv(selcoeff=[0, 0.25, 0.5, 0.25], switches=15, gens=1200)
print selective_regime2
selective_regime3 = GenerateSelectiveEnv(selcoeff='random', switches=20, gens=2000)
print selective_regime3