#!/usr/bin/env python
"""Example fwdpy script from K. Thornton's README. This script simulates a
population with the following parameters:
    N = 1000 diploids
    Theta = 4Nu = 100
    Genomic segment with coordinates [0, 1)
    Rho = 4Nr = 100
    Non-neutral mutation rate per gamete per gen = 0.01
    p(deleterious | non-neutral) = 0.99, sh = -0.1
    p(beneficial | non-neutral) = 0.01, sh = 0.001
    Deleterious mutations happen on [-1, 0) or [1, 2)
    Beneficial mutations happen on [-1, 2)
    Recombination uniform on [-2, 2)
    Demographic model from European Drosophila, as inferred by Thornton and
        Andolfatto (2006)
"""

#   Import the fwdpy module
import fwdpy
#   And numpy
import numpy

#   Set up the regions.
#       fwdpy.Region() creates a new genomic region
#       The arguments are as follows:
#           fwdpy.Region(beg, end, wt, coupled = True)
#       beg = beginning of region, float
#       end = end of region, float
#       wt = weight, float
#       if coupled = True, weight is converted to a "per unit" weight, and it
#       can be interpreted as a per-basepair weight
nregions = [
    fwdpy.Region(-1, 0, 1),
    fwdpy.Region(1, 2, 1)
    ]

#   Set up the selected regions
#       fwdpy.ConstantS() is a child class of a Region(). It follow this
#       hierarchy:
#           Region() -> Sregion() -> ConstantS()
#           A region    With s + h   constant s
#       The arguments are as follows:
#           ConstantS(beg, end, wt, s, h=1.0, coupled=True)
#       beg, end, wt are as above.
#       s = selective coefficient
#       h = dominance term. Defaults to 1.0
#       coupled as above
#   In this case, we have three selected regions:
#   The first two are deleterious mutation regions
#       Note that I think there is a typo in the main example page. There is an
#       extra 1 argument in the first region
#   The next region is a beneficial mutation region
sregions = [
    fwdpy.ConstantS(-1, 0, 0.99/2.0, -0.1, 1),
    fwdpy.ConstantS(1, 2, 0.99/2.0, -0.1, 1),
    fwdpy.ConstantS(-1, 2, 0.01, 0.001, 1)
    ]

#   Recombination rate is uniform
rregions = [
    fwdpy.Region(-2, 2, 1)
    ]

#   Get a random seed
rng = fwdpy.GSLrng(100)

#   Set the population sizes
popsizes = numpy.array(
    [1000],
    dtype=numpy.uint32
    )
#   Simulate 10N generations (10,000 gens)
popsizes = numpy.tile(popsizes, 10000)

#   Simulate a single deme. Neutral mutation rate is 1e-3, the same as the
#   recombination rate. The function is called as follows:
#       evolve_regions(
#           RNG seed,
#           npops,
#           diploid popsize,
#           neutral mutation rate,
#           selected mutation rate,
#           recombination rate,
#           neutral regions,
#           selected regions,
#           recombining regions,
#           selfing probability (default f=0),
#           fitness model (either multiplicative or additive)
#            )
pops = fwdpy.evolve_regions(
    rng,
    10,
    1000,
    popsizes,
    0.001,
    0.0001,
    0.001,
    nregions,
    sregions,
    rregions
    )

#   evolve_regions() returns a 'popvec' object. It is an iterablet hat contains
#   a bunch of 'singlepop' objects.
#   Let's get some basic information about each one
for index, p in enumerate(pops):
    print "Population", index
    print "    Evolved to generation", p.gen()
    print "    Has", p.popsize(), "diploid individuals"

#   Now, to calculate some summary statistics
#   fwdpy has a handle into the libsequence library
import fwdpy.libseq

#   To calculate summary stats, we have to take a sample from our populations
#       get_samples(
#           RNG,
#           singlepop object,
#           nsam,
#           removeFixed=True, (True: keep only polymorphic sites)
#           deme=None (required for if there is pop structure)
#       )
samples = [fwdpy.get_samples(rng, p, 20) for p in pops]

#   Then we can calculate windowed summary statistics
#       windows(
windowed_stats = [
    fwdpp.libseq.windows(i[0], 0.1, 0.1, -2, 2) for i in samples
    ]

