from collections import defaultdict
from copy import copy

debug = True

class apriori:
	def __init__(self, infile, outfile, min_sup):
		self.infile = infile
		self.outfile = outfile
		self.support = (float)(min_sup)
		self.total_count = 0
		self.k_itemsets = list()
		self.file_lines = None
	def __str__(self):
		return str(len(self.k_itemsets))

	def prune(self, itemset):
		pruned = {}
		for element in itemset:
			count = itemset[element]
			if self.support < 1:
				element_support = (float)((float)(count) / (float)(self.total_count))
			else:
				element_support = count
			if element_support > self.support:
				pruned[element] = count
		return pruned

	def process_input(self):
		f = open(self.infile)
		self.file_lines = f.readlines()
		f.close()
		self.total_count = len(self.file_lines)
		one_itemset_pre = defaultdict(int)
		one_itemset_pruned = {}
		for line in self.file_lines:
			curr_line = line.split()
			for element in curr_line:
				e = int(element)
				one_itemset_pre[e] += 1
		if debug: print len(one_itemset_pre)
		# for element in one_itemset_pre:
		# 	count = one_itemset_pre[element]
		# 	if self.support < 1:
		# 		element_support = (float)((float)(count) / (float)(self.total_count))
		# 	else:
		# 		element_support = count
		# 	if element_support > self.support:
		# 		one_itemset_pruned[element] = count
		one_itemset_pruned = self.prune(one_itemset_pre)
		if debug: print len(one_itemset_pruned)
		self.k_itemsets.append(one_itemset_pruned)
	
	def generate_itemset(self, k):
		k_plus_one = defaultdict(int)
		k_itemset = self.k_itemsets[k]
		temp = {}
		counter = 0
		temp = copy(self.k_itemsets[0])
		generated = False
		for element in k_itemset:
			counter += 1
			print counter
			if k == 0:
				temp_list = list()
				temp_list.append(element)
			else:
				temp_list = list(element)
			# temp = copy(k_itemset)
			for i in temp_list:
				print "item" + str(i)
				if i in temp:
					del temp[i]
			# del temp[element]
			print len(temp)
			for item in temp:
				
				# if k == 0:
				inner_temp_list = list()
				inner_temp_list.append(item)
				# else:
					# inner_temp_list = list(item)

				new_element = temp_list + inner_temp_list
				new_tuple = tuple(new_element)
				
				for line in self.file_lines:
					curr_line = line.split()
					numbers = [int(x) for x in curr_line]
					# print numbers
					# print new_element
					if set(new_element) <= set(numbers):
						generated = True
						# print "!"
						# print numbers
						# print new_element
						# print new_tuple
						# quit()
						k_plus_one[new_tuple] += 1

			# print len(k_itemset)
			# print len(k_plus_one)
			# print k_plus_one
			# quit()
			# print len(temp)
		if generated == False:
			return False
		pruned = self.prune(k_plus_one)
		self.k_itemsets.append(pruned)
		return True
		# print len(k_itemset)
		# print len(k_plus_one)
		# print k_itemset
		# print k_plus_one
			# quit()			

	def patter_mining(self):
		curr_itemset = 0
		while(True):
			escape = self.generate_itemset(curr_itemset) 
			curr_itemset += 1
			if escape == False:
				break

		print len(self.k_itemsets)
		for itemset in self.k_itemsets:
			print itemset


	# 	test_list = list()
	# 	test_list.append('4')
	# 	test_list.append('6')
	# 	for line in self.file_lines:
	# 		curr_line = line.split()
	# 		print curr_line
	# 		print test_list
	# 		# quit()
	# 		if set(test_list) <= set(curr_line):
	# 			print "!"
	# 			quit()
