import math

def mean(l):
	"""
	"""
	return average(l)

def average(l):
	"""
	"""
	return sum(l)*1.0/len(l)

def var(l):
	"""
	"""
	return variance(l)

def variance(l):
	"""
	"""
	avg = average(l)
	return sum( abs((val - avg)) ** 2 for val in l ) / (len(l)-1)

def stdev(l):
	"""
	"""
	return math.sqrt(variance(l))
