"""Genetic Algorithm.py

Swarming behaviour is based on aggregation of simple drones exhibiting basic instinctive reactions to stimuli. However, 
to achieve overall balanced/interesting behaviour the relative importance of these instincts, as well their internal
parameters, must be tuned. In this project, you will learn how to apply Genetic Programming as means of such tuning, 
and attempt to achieve a series of non-trivial swarm-level behaviours.
"""

from __future__ import barry_as_FLUFL

__all__ = None
__author__ = "#CHEE JUN YUAN GLENN#"
__copyright__ = "Copyright © 2019, Cheejyg"
__email__ = "CHEE0124@e.ntu.edu.sg"
__license__ = "MIT"
__maintainer__ = "#CHEE JUN YUAN GLENN#"
__status__ = "Development"
__version__ = "1.0"

# import argparse
# import json
# import matplotlib
# import matplotlib.animation
# import matplotlib.pyplot
# from mpl_toolkits.mplot3d import Axes3D
import numpy
# import os
import random
# import scipy
# import sys
# import tensorflow
# import time

GeneticAlgorithmsForSwarmParameterTuning = __import__("Genetic Algorithms for Swarm Parameter Tuning")

random.seed(24)
numpy.random.seed(24)
crossover_type = 2  # [0 = Uniform, 1 = Single-point, 2 = Two-point, k = k-point]
mutation_type = 0  # [0 = Bit, 1 = Flip, 2 = Boundary, 3 = Non-Uniform, 4 = Uniform, 5 = Gaussian, 6 = Shrink]
n = 24
properties = 12
specialisations = 6
generations = 1000

scenes = None

population = None
populationFitness = None
specialisation = None

parameters = None


def __main__() -> None:
	global populationFitness
	
	__initialise__()
	
	print(str(populationFitness).replace("],", "], \n"))
	
	return


def __initialise__() -> None:
	global population
	global populationFitness
	global specialisation
	
	population = numpy.random.rand(n, properties) * 100
	
	populationFitness = []
	for x in range(n):
		fitness = __fitness__(population[x], "scene/scene.json")
		populationFitness.append(fitness[1])
	
	specialisation = numpy.random.randint(0, specialisations, n, dtype=int)
	
	return


def __fitness__(candidate_solution: list, scene_file: str) -> float:
	global parameters
	
	parameters = {
		"boidSize": 0.10922,
		"radii": {
			"separation": candidate_solution[1], 
			"alignment": candidate_solution[2], 
			"cohesion": candidate_solution[3], 
			"predator": candidate_solution[4], 
			"prey": candidate_solution[5]
		},
		"weights": {
			"separation": candidate_solution[6], 
			"alignment": candidate_solution[7], 
			"cohesion": candidate_solution[8], 
			"predator": candidate_solution[9], 
			"predatorBoost": 2.0, 
			"prey": candidate_solution[10], 
			"preyBoost": 2.0
		},
		"maximumSpeed": candidate_solution[11]
	}
	
	return GeneticAlgorithmsForSwarmParameterTuning.__run__(parameters, scene_file)


def crossover(a: list, b: list) -> (list, list):
	size = min(len(a), len(b))
	
	if crossover_type < 1:
		lhs = numpy.random.randint(1 + 1, size=size) > 0
		rhs = lhs < 1
		
		children = (
			(a * lhs + b * rhs).tolist(), 
			(b * lhs + a * rhs).tolist()
		)
	elif crossover_type == 1:
		start_point = random.randint(1, size - 2)
		
		children = (
			numpy.concatenate((a[:start_point], b[start_point:])).tolist(), 
			numpy.concatenate((b[:start_point], a[start_point:])).tolist()
		)
	elif crossover_type == 2:
		start_point = random.randint(1, size - 3)
		mid_point = random.randint(start_point + 1, size - 2)
		
		children = (
			numpy.concatenate((a[0:start_point], b[start_point:mid_point], a[mid_point:])).tolist(), 
			numpy.concatenate((b[0:start_point], a[start_point:mid_point], b[mid_point:])).tolist()
		)
	else:
		return None
	
	return children


def mutation(a: list) -> list:
	size = len(a)
	
	if mutation_type == 0:
		bit = numpy.random.rand(size) < (1 / size)
		
		a = ((numpy.random.rand(size) * 100) * (bit > 0) + a * (bit < 1)).tolist()
	elif mutation_type == 1:
		a = (numpy.array(100) - a).tolist()
	elif mutation_type == 2:
		boundary = numpy.random.rand()
		
		if boundary < (1 / 3):
			a = numpy.clip(a, random.random() * 100, None).tolist()  # lower bound
		elif boundary < (2 / 3):
			a = numpy.clip(a, None, random.random() * 100).tolist()  # upper bound
		else:
			a = numpy.clip(a, random.random() * 100, random.random() * 100).tolist()  # lower and upper bound
	else:
		a = list((numpy.random.rand(size) * 100).tolist())
	
	return a


if __name__ == "__main__":
	__main__()
