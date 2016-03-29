import numpy as np
import scipy as sp
from scipy import stats
from sys import argv
from sklearn import datasets
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

__author__ = 'Jakub Klapacz (jklapac2@illinois.edu)'

usage = "Usage: \n\
			python 1.py [-1 | -2 | -3] \n\
			-1: problem 1\n\
			-2: problem 2\n\
			-3: problem 3\n\
			no args: run all problems\n"

'''
	This function returns the maximum number of a collection of numbers
'''
def max(array):
	assert len(array) > 0
	cur_max = array[0]
	for item in array:
		if item >= cur_max:
			cur_max = item
	return cur_max
'''
	This funciton returns the minimum number of a collection of numbers
'''
def min(array):
	assert len(array) > 0
	cur_min = array[0]
	for item in array:
		if item < cur_min:
			cur_min = item
	return cur_min

'''
	Returns the mean of a collection of numbers
'''
def mean(array):
	assert len(array) > 0
	total = 0
	for item in array:
		total += item
	return (total / len(array))

'''
	Calculates the value at the desired percentile q
	q should be between [0, 1]
'''
def percentile(array, q):
	assert len(array) > 0
	s = sorted(array)
	index = int(q * len(array))
	return s[index]

'''
	Returns the mode of a dataset
'''
def mode(array):
	s = sorted(array)
	counts = {}
	for item in s:
		if item not in counts:
			counts[item] = 1
		else:
			counts[item] += 1
	cur_mode = (0, 0)
	for item in counts:
		if counts[item] > cur_mode[1]:
			cur_mode = (item, counts[item])
	return cur_mode[0]
	
'''
	Returns the variance of a dataset
	Calculates the sum of squared differences from the mean of the dataset
'''
def variance(array):
	m = mean(array)
	total = 0
	for item in array:
		dif = item - m
		dif *= dif
		total += dif
	return (total / (len(array) - 1))

'''
	This function calculates the distance between vectors
	x,y are vectors, h designates the type of distance to calculate.
	(From Lecture):
		h = 1: manhattan distance
		h = 2: euclidean distance
		h = -1: supremum distance
'''
def distance(x, y, h):
	if h == -1:
		# supremum: use max of the distances between two attributes
		return max(abs(x - y))
		pass
	else:

		# Use h
		assert len(x) == len(y)
		total = 0
		for i in range(len(x)):
			diff = abs(x[i] - y[i])
			diff = pow(diff, h)
			total += diff
		
		if h == 2:
			total = np.sqrt(total)
		# total = total**(1/h)
		

		# total = pow(total, (1/h))
		return total
'''
	This function calculates the cosine similarity between two vectors x and y
	The formula that this uses is:
		 <x dot y>
		----------
		||x||||y||

		where ||x|| and ||y|| are the L_2 norms of the x,y vectors
'''
def cosdist(x, y):
	assert len(x) == len(y)
	z = np.zeros(x.shape)
	x_norm = distance(x, z, 2)
	y_norm = distance(y, z, 2)
	total = 0
	for i in range(len(x)):
		cur = x[i] * y[i]
		total += cur
	# print "AAA"
	# print x_norm
	# print y_norm
	return (total / (x_norm * y_norm))
	# exit()

def problem1():
	# Load in dataset
	dataset = "data/data.online.scores"
	array = np.loadtxt(dataset)
	
	# Extract only midterm scores
	midterms = array[:,1]
	
	# Min and Max
	print "Max:\t" + str(max(midterms))
	print "Min:\t" + str(min(midterms))


	# Q1, Median, Q3
	print "Q1:\t" + str(percentile(midterms, .25))
	print "Q3:\t" + str(percentile(midterms, .75))
	print "Median:\t" + str(percentile(midterms, .5))
	

	# Sample Mean
	print "Sample Mean:\t" + str(mean(midterms))
	

	# Mode
	
	print "Sample Mode:\t" + str(mode(midterms))
	

	# Sample Variance
	
	print "Sample Variance:\t" + str(variance(midterms))




def problem2():

	# Load dataset
	dataset = "data/data.supermarkets.inventories"
	
	file = open(dataset, "r")
	lines = file.readlines()
	# Get store1 data
	store1 = lines[1].split()
	store1 = np.asarray(store1)
	store1 = store1[2:len(store1)]
	store1 = np.asarray(store1, dtype=float)
	# Get store2 data
	store2 = lines[2].split()
	store2 = np.asarray(store2)
	store2 = store2[2:len(store2)]
	store2 = np.asarray(store2, dtype=float)
	
	# Report distances
	print "Manhattan Distance:\t" + str(distance(store1, store2, 1))
	print "Euclidian Distance:\t" + str(distance(store1, store2, 2))
	print "Supremum Distance:\t" + str(distance(store1, store2, -1))

	# Report cosine similarity
	print "Cosine Similarity:\t" + str(cosdist(store1, store2))
	# array = np.genfromtxt(dataset, dtype=None)

	# print array

def problem3():
	# Load dataset
	dataset = "data/data.online.scores"
	array = np.loadtxt(dataset)
	
	midterms = array[:,1]

	# Calculate variance, mean and standard deviation (pre normalization)
	var = variance(midterms)
	sd = np.sqrt(var)
	m = mean(midterms)

	# Normalize the data
	midterms_norm = midterms - m
	midterms_norm = midterms_norm / sd

	# Calculate new mean (and round down if small enough)
	normed_mean = mean(midterms_norm)
	if normed_mean < 0.00001:
		normed_mean = 0

	# Report results
	print "Pre-normalized Sample Mean:\t" + str(m)
	print "Pre-normalized Sample Variance:\t" + str(var)
	print "Normalized Sample Mean:\t" + str(normed_mean)
	print "Normalized Sample Variance:\t" + str(variance(midterms_norm))
	print "Value of 90 normalized = " + str((90 - m)/sd)

def problem4():

	iris = datasets.load_iris()
	
	irisdata = iris.data
	irislabels = iris.target
	irisnames = iris.target_names
	
	# Initialize a PCA object with 4 components
	pca = PCA(n_components = 4)

	# Calculate eigenvectors and project data to principal components
	results = pca.fit(irisdata).transform(irisdata)

	# This metric tells us how much % of the variance each component makes up
	print "Variances for first two components:\t" + str(pca.explained_variance_ratio_)

	# Plot the projection scatter plot
	plt.figure()
	for c, i, target_name in zip("rgb", [0, 1, 2], irisnames):
		plt.scatter(results[irislabels == i, 3], results[irislabels == i, 2], c=c, label=target_name)
	plt.legend()
	plt.title('PCA of IRIS dataset')
	plt.show()

def main(option):
	if (option == "all"):
		problem1()
		print "======================================="
		problem2()
		print "======================================="
		problem3()
		print "======================================="
		problem4()


	# TESTING CODE

	# print "+++++++++++++++++++++++++++++++++++++++++"

	
	# print "Max:\t" + str(midterms.max())
	# print "Min:\t" + str(midterms.min())

	# print "Q1:\t" + str(np.percentile(midterms, 25))
	# print "Q3:\t" + str(np.percentile(midterms, 75))
	# print "Median:\t" + str(np.median(midterms))
	# modey = stats.mode(midterms)[0][0]
	# print "Sample Mode:\t" + str(modey)
	# print "Sample Mean:\t" + str(np.mean(midterms))
	# print "Sample Variance:\t" + str(np.var(midterms))
	# mode(midterms)
	
	

if __name__ == '__main__':
	if len(argv) == 1:
		main("all")
	elif len(argv) == 2:
		if argv[1] == "-1":
			problem1()
		elif argv[1] == "-2":
			problem2()
		elif argv[1] == "-3":
			problem3()
		elif argv[1] == "-4":
			problem4()
		else:
			print usage
	else:
		print usage
	