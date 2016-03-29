from collections import defaultdict
from copy import copy
from operator import itemgetter

debug = False	
vocabfile = "data-assign3/vocab.txt"
max_out_prefix = "max/max-"
closed_out_prefix = "closed/closed-"
frequent_out_prefix = "patterns/pattern-"

class apriori:
	def __init__(self, infile, outfile, min_sup):
		self.infile = infile
		self.outfile = outfile
		self.support = (float)(min_sup)
		self.total_count = 0
		self.k_itemsets = list()
		self.transactions = list()
		self.vocab = self.init_vocab()
		self.pattern_list = None
		self.closed_list = list()
		self.max_list = list()


	def init_vocab(self):
		output = {}
		f = open(vocabfile)
		for line in f.readlines():
			l = line.split()
			key = int(l[0])
			output[key] = l[1]
		return output

			


	def prune(self, itemset):
		pruned = {}
		for element in itemset:
			count = itemset[element]
			if self.meets_support(count):
				pruned[element] = count
		return pruned

	def meets_support(self, support):
		if self.support < 1:
			element_support = (float)((float)(support) / (float)(self.total_count))
		else:
			element_support = support
		return element_support >= self.support

	def process_input(self):
		f = open(self.infile)
		lines = f.readlines()
		f.close()
		self.total_count = len(lines)
		one_itemset_pre = defaultdict(int)
		one_itemset_pruned = {}
		for line in lines:
			curr_line = line.split()
			transaction = [int(x) for x in curr_line]
			transaction = set(transaction)
			self.transactions.append(transaction)
			for element in curr_line:
				e = int(element)
				one_itemset_pre[e] += 1
		if debug: print len(one_itemset_pre)
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
			if debug:
				counter += 1
				print counter
			if k == 0:
				temp_list = list()
				temp_list.append(element)
			else:
				temp_list = list(element)
			# temp = copy(k_itemset)
			for i in temp_list:
				if debug: print "item" + str(i)
				if i in temp:
					del temp[i]
			# del temp[element]
			if debug: print len(temp)
			for item in temp:
				
				# if k == 0:
				inner_temp_list = list()
				inner_temp_list.append(item)
				# else:
					# inner_temp_list = list(item)

				new_element = temp_list + inner_temp_list
				new_tuple = tuple(new_element)
				for transaction in self.transactions:
					if set(new_element) <= transaction:
						generated = True
						k_plus_one[new_tuple] += 1
				# if self.meets_support(k_plus_one[new_tuple]) == False:
					# del k_plus_one[new_tuple]

		if generated == False:
			return False
		pruned = self.prune(k_plus_one)
		if len(pruned) == 0:
			return False
		self.k_itemsets.append(pruned)
		return True

	def output_rules(self, list_to_use, rule_type):
		if list_to_use is None:
			output = list()
			for i in range(len(self.k_itemsets)):
				curr_dict = self.k_itemsets[i]
				for element in self.k_itemsets[i]:
					item = (element, curr_dict[element])
					output.append(item)
			output = sorted(output, key=itemgetter(1), reverse=True)
			self.pattern_list = output
			list_to_use = output
		outputstr = ''
		if rule_type == "frequent":
			outputstr += "====== Frequent Patterns ======\n"
		if rule_type == "closed":
			outputstr += "======= Closed Patterns =======\n"
		if rule_type == "max":
			outputstr += "========= Max Patterns ========\n"

		if self.support < 1:
			outputstr += "Minimum support = {} (approx. {:.0f})".format(self.support, self.total_count*self.support)
		else:
			outputstr += "Minimum support = {}".format(self.support)
		outputstr += "\nSUPPORT | FREQUENCY | RULE\n"
		for i in range(len(list_to_use)):
			
			t = list_to_use[i]
			translate = None
			if type(t[0]) is tuple:
				translate = list(t[0])
			frequency = float(t[1]) / float(self.total_count)
			outputstr += "{}\t{:.3f}\t".format(t[1], frequency)
			outputstr += "["
			if translate is not None:

				for candidate in translate:
					
					outputstr += self.vocab[candidate] + ", " 
					
			else:
				outputstr += self.vocab[t[0]]
			outputstr += ']\n'
		outputstr += "Generated {} patterns".format(len(list_to_use))
		# print outputstr
		if rule_type == "frequent":
			outfilename = frequent_out_prefix + self.outfile + ".txt"
		if rule_type == "closed":
			outfilename = closed_out_prefix + self.outfile + ".txt"
		if rule_type == "max":
			outfilename = max_out_prefix + self.outfile + ".txt"
		
		outf = open(outfilename, 'w')
		outf.write(outputstr)
		outf.close()

		# print outputstr

			# temp_list = list(t[0])
			# print temp_list

			# print output[i]
			# quit()
	def closed_mining(self):
		for i in range(len(self.pattern_list)):
			add_to_closed = True
			current = self.pattern_list[i]
			sub = current[0]
			if type(sub) is int:
				l = list()
				l.append(sub)
				sub = set(l)
			else:
				sub = set(sub)
			for j in range(len(self.pattern_list)):
				candidate = self.pattern_list[j]
				sup = candidate[0]
				if type(sup) is int:
					t = list()
					t.append(sup)
					sup = set(t)
				else:
					sup = set(sup)
				if sup > sub and current[1] == candidate[1]:
					add_to_closed = False
			if add_to_closed == True:
				self.closed_list.append(current)
		self.output_rules(self.closed_list, "closed")

	def max_mining(self):			
		for i in range(len(self.pattern_list)):
			add_to_max = True
			current = self.pattern_list[i]
			sub = current[0]
			if type(sub) is int:
				l = list()
				l.append(sub)
				sub = set(l)
			else:
				sub = set(sub)
			for j in range(len(self.pattern_list)):
				candidate = self.pattern_list[j]
				sup = candidate[0]
				if type(sup) is int:
					t = list()
					t.append(sup)
					sup = set(t)
				else:
					sup = set(sup)
				if sup > sub:
					add_to_max = False
			if add_to_max == True:
				self.max_list.append(current)
		self.output_rules(self.max_list, "max")

	def pattern_mining(self):
		curr_itemset = 0
		while(True):
			print "Generating " + str(curr_itemset + 1) + "-itemset"
			escape = self.generate_itemset(curr_itemset) 
			curr_itemset += 1
			if escape == False:
				break

		self.output_rules(self.pattern_list, "frequent")
		# self.closed_mining()

		if debug:
			print len(self.k_itemsets)
			for itemset in self.k_itemsets:
				print itemset

