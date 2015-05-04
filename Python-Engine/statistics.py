"""
	Statistics

	Funstions for some simple statistical calculations

	AUTHOR: albin.hubsch@gmail.com
	UPDATED: 2015-05
"""

import math

def mean(l):
	"""
		Calculate the mean of a list
	"""
	return average(l)

def average(l):
	"""
		Calculate the average of a list, is the same as mean
	"""
	return sum(l)*1.0/len(l)

def var(l):
	"""
		Calculate the variance of a list
	"""
	return variance(l)

def variance(l):
	"""
		Calculate the variance of a list
	"""
	avg = average(l)
	return sum( abs((val - avg)) ** 2 for val in l ) / (len(l)-1)

def stdev(l):
	"""
		Calculate the standard deviation of a list
	"""
	return math.sqrt(variance(l))
