import pandas as pd
import numpy as np
import sys
from collections import defaultdict
from math import log, exp
usage = "python hw5.py <train_file> <test_file>"
verbose = False


class Category():
	def __init__(self, label = None):
		self.label = label
		self.attributes=defaultdict(dict)
		self.attribute_prob = defaultdict(int)
		self.total = 0
		self.probability = 0.0

def train(train_data, classes):
	for line in train_data:
		cur_line = line.split()
		cur_label = int(cur_line[0])
		classes[cur_label].total += 1
		for i in range(1, len(cur_line)):
			attribute, value = cur_line[i].split(':')
			classes[cur_label].attribute_prob[(attribute,value)] += 1
			try:
				classes[cur_label].attributes[attribute][value] += 1
			except KeyError:
				classes[cur_label].attributes[attribute][value] = 1
	total = float(classes[1].total + classes[-1].total)
	classes[1].probability = float(classes[1].total) / total
	classes[-1].probability = float(classes[-1].total) / total


def predict(vector, classes):
	positive = log(classes[1].probability)
	negative = log(classes[-1].probability)
	for i in range(len(vector)):
		attribute, value = vector[i].split(":")
		a = float(classes[1].attribute_prob[(attribute,value)])
		b = float(classes[1].total)
		c = float(classes[-1].attribute_prob[(attribute,value)])
		d = float(classes[-1].total)
		pos = a/b
		neg = c/d
		if pos == 0:
			pos = 1.0/float(classes[1].total + 1)
		if neg == 0:
			neg = 1.0/float(classes[-1].total + 1)

		positive += log(pos)
		negative += log(neg)

	if positive > negative: return 1
	else: return -1

def adaPredict(vector, classifiers):
	vote_pos, vote_neg = 0, 0
	for classifier in classifiers:
		predicted = predict(vector, classifier)
		if predicted == 1: vote_pos += 1
		else: vote_neg += 1
	if vote_pos > vote_neg: return 1
	else: return -1

def test(test_data, classes, ada=False):
	tp, fp, tn, fn = 0, 0, 0, 0
	testlabels = getLabels(test_data)
	output = []
	for i in range(len(testlabels)):
		cur_line = test_data[i].split()
		if ada == True: 
			prediction = adaPredict(cur_line[1:], classes)
		else:
			prediction = predict(cur_line[1:], classes)
		output.append(prediction)
		if testlabels[i] == 1:
			if prediction == 1: tp += 1
			else: fp += 1
		else:
			if prediction == 1: fn += 1
			else: tn += 1
	return output, tp, fp, fn, tn

def getDatasets(train_file, test_file):
	traindata = open(train_file)
	traindata = list(traindata.readlines())
	testdata = open(test_file)
	testdata = list(testdata.readlines())
	return traindata, testdata	

def getLabels(data):
	output = []
	for line in data:
		cur_line = line.split()
		output.append(int(cur_line[0]))
	return output 

def getZ(alpha, labels, predictions, d):
	assert len(labels) == len(predictions) == len(d)	
	z = 0
	for i in range(len(labels)):
		z += d[i] * exp(-alpha*labels[i]*predictions[i])
	return z

def updateDistribution(error, predictions, labels, d):
	d_new = []
	alpha = getAlpha(error)
	z = getZ(alpha, labels, predictions, d)
	for i in range(len(labels)):
		new_value = d[i]*exp(-alpha*labels[i]*predictions[i])
		new_value = new_value / z
		d_new.append(new_value)
	return d_new

def getAlpha(error):
	return (.5)*log(float(1-error)/float(error)) 

def adaboost(data, num_iterations ,testdata):
	d = []
	for i in range(len(data)):
		prob = float(1)/float(len(data))
		d.append(prob)

	labels = getLabels(data)
	classifiers = []
	for i in range(num_iterations):
		sample = np.random.choice(data, len(data), replace=True, p=d)
		classes = {
			1: Category(label=1),
			-1: Category(label=-1)
		}

		train(sample, classes)
		predictions, g, g, g, g = test(data, classes)
		total = len(predictions)
		correct = 0
		for j in range(len(predictions)):
			if labels[j] == predictions[j]:
				correct += 1
		error = 1 - (float(correct)/float(total))
		d = updateDistribution(error, predictions, labels, d)

		classifiers.append(classes)
	# classifiers = [classes]
	o, tp, fp, fn, tn = test(data, classifiers, ada=True)
	outputStats(tp, fp, fn, tn, "AdaBoost Training Set")

	o, tp, fp, fn, tn = test(testdata, classifiers, ada=True)
	outputStats(tp, fp, fn, tn, "AdaBoost Test Set")

def outputStats(tp, fp, fn, tn, label):

	
	accuracy = float(tp + tn) / float(tp + fp + fn + tn)
	error = 1-accuracy
	sensitivity = float(tp) / float(tp + fn)
	try:	
		specificity = float(tn) / float(tn + fp)
	except ZeroDivisionError:
		specificity = 0
	precision = float(tp) / float(tp + fp)
	f1 = (2.0*tp) / float(2.0*tp + fp + fn)
	fp5 = float((1 + (.5*.5))*tp) / float((1 + (.5*.5))*tp + (.5*.5)*fn + fp)
	f2 = float((1 + (2*2))*tp) / float((1 + (2*2))*tp + (2*2)*fn + fp)
	print "="*50
	print label + " Stats"
	print "="*50
	print "\tAccuracy = {}".format(accuracy)
	if verbose == True:

		print "\tError = {}".format(error)
		print "\tSensitivity = {}".format(sensitivity)
		print "\tSpecificity = {}".format(specificity)
		print "\tPrecision = {}".format(precision)
		print "\tF_1 value = {}".format(f1)
		print "\tF_.5 value = {}".format(fp5)
		print "\tF_2 value = {}".format(f2)
		print "\t------------"
		print "\t{}\t{}\n\t{}\t{}".format(tp, fp, fn, tn)



def naivebayes(train_file, test_file):
	traindata, testdata = getDatasets(train_file, test_file)
	classes = {
		1: Category(label=1),
		-1: Category(label=-1)
	}
	train(traindata, classes)
	predictions, tp, fp, fn, tn = test(traindata, classes)
	outputStats(tp, fp, fn, tn, "Naive Bayes Training Set")
	
	predictions, tp, fp, fn, tn = test(testdata, classes)
	outputStats(tp, fp, fn, tn, "Naive Bayes Test Set")


def main(train_file, test_file):
	traindata, testdata = getDatasets(train_file, test_file)
	naivebayes(train_file, test_file)
	adaboost(traindata, 5, testdata)
	

if __name__ == '__main__':
	if len(sys.argv) < 3 or len(sys.argv) > 5:
		print usage
	else:
		main(sys.argv[1], sys.argv[2])
