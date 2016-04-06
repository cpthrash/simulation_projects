#!/usr/bin/env python

"""
This script is intended to elucidate allele frequencies in a population that is undergoing fluctuating selection.
"""



import os, sys, types, time #not sure if all of these are needed, depends on modules that I'm using
import simuOpt
from simuPOP import *

#Start SimuPOP program

#Set initial population parameters
pop = Population()
# Set initial allele frequencies
sim.InitGenotype(freq=[0.8, 0.2])


options = [
    {
     'name':'PopSize',
     'default':2000,
     'label':'Population Size',
     'type':[int, long],
     'validator':simuOpt.valueGT(0),
     },
    {
     'name':'m',
     'default':0.001,
     'label':'Mutation Rate',
     'type':[float],
     'validator':simuOpt.valueBetween(0., 1.),
     },
    {
     'name':'generations',
     'default':500,
     'label':'Generations to evolve',
     'description':'Length of evolution',
     'type':[int, long],
     'validator':simuOpt.valueGT(0)
     },
    {
     'name':'step',
     'default':100,
     'label':'Steps to take per generation',
     'description':'Values displayed per generation',
     'type':[int, long],
     'validator':simuOpt.valueGT(0)
     },
]