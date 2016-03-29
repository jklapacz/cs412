from sys import argv
from collections import defaultdict

class warehouse(object):

	def __init__(self, filename):
		self.matrix = list()
		raw = open(filename)
		for line in raw.readlines():
			line = line.strip('\n')
			self.matrix.append(line.split('\t'))
		raw.close()

	
	def printer(self, n):
		print self.matrix[n]

def check_targets(entry, targets):
	# print "==="
	# print entry
	# print targets
	for i in range(len(entry)):
		if targets[i] is not None and entry[i] != targets[i]:
			# print "\t\tFalse\n"
			return False	
	# print "\t\tTrue\n"
	return True

def getcounts(w, params, criteria):
	# print params
	# print criteria
	
	location_city = False
	location_state = False
	location_aggr = False
	cat_aggr = False
	rating_aggr = False
	price_aggr = False

	if params[0] == 'c':
		location_city = True
	if params[0] == 's':
		location_state = True
	if params[0] == '*':
		location_aggr = True
	if params[1] == '*':
		cat_aggr = True
	if params[2] == '*':
		rating_aggr = True
	if params[3] == '*':
		price_aggr = True
	
	targets = [None, None, None, None]
	for i in range(len(params)):
		if params[i] != criteria[i]:
			targets[i] = criteria[i]

	# print targets
	

	level0 = defaultdict(list)
	if location_aggr == True:
		# count = 0
		for item in w.matrix:
			# count += 1
			if(check_targets(['*'] + item[3:6], targets) == True):
				level0['anywhere'].append(item[3:6])
			# print count

		# quit()
	else:
		# count = 0	
		for item in w.matrix:
			if location_city:
				if(check_targets([item[1]] + item[3:6], targets) == True):
					level0[item[1]].append(item[3:6])
			else:
				
				if(check_targets([item[2]] + item[3:6], targets) == True):
					# count += 1
					level0[item[2]].append(item[3:6])
		# print count
		# quit()
	count = 0
	for location in level0:
		level1 = defaultdict(list)
		for item_cat in level0[location]:
			level1[item_cat[0]].append(item_cat[1:3])
		for category in level1:
			level2 = defaultdict(list)
			for item_quality in level1[category]:
				level2[item_quality[0]].append(item_quality[1:2])
			for item_price in level2:
				combined = list()
				for i in range(len(level2[item_price])):
					if level2[item_price][i] not in combined:
						combined.append(level2[item_price][i])
						count += 1
	# print count
	return count

def countcells(params, w):
	location_city = False
	location_state = False
	location_aggr = False
	cat_aggr = False
	rating_aggr = False
	price_aggr = False

	if params[0] == 'c':
		location_city = True
	if params[0] == 's':
		location_state = True
	if params[0] == '*':
		location_aggr = True
	if params[1] == '*':
		cat_aggr = True
	if params[2] == '*':
		rating_aggr = True
	if params[3] == '*':
		price_aggr = True

	level0 = defaultdict(list)
	if location_aggr == True:
		# count = 0
		for item in w.matrix:
			# count += 1
			level0['anywhere'].append(item[3:6])
		# print len(level0['anywhere'])
		# print level0['anywhere']
		# quit()		
		# print count
		# quit()
	else:	
		for item in w.matrix:
			if location_city:	
				level0[item[1]].append(item[3:6])
			else:
				level0[item[2]].append(item[3:6])
	count = 0
	for location in level0:
		level1 = defaultdict(list)
		
		for item_cat in level0[location]:
			if cat_aggr == True:
				level1['anycategory'].append(item_cat[1:3])
			else:
				level1[item_cat[0]].append(item_cat[1:3])
		# print len(level1['food'])
		# print len(level1['sports'])
		# print len(level1['clothes'])
		# print len(level1['food'])

		# quit()
		counta = 0
		for category in level1:
			counta += 1
			level2 = defaultdict(list)
			for item_quality in level1[category]:
				if rating_aggr == True:
					level2['anyquality'].append(item_quality[1:2])
				else:
					level2[item_quality[0]].append(item_quality[1:2])
			for item_price in level2:
				if price_aggr == True:
					count += 1
				else:
					combined = list()
					for i in range(len(level2[item_price])):
						if level2[item_price][i] not in combined:
							combined.append(level2[item_price][i])
							count += 1
		# print counta
		# quit()
	# print count
	return count

def main(file):
	
	w = warehouse(file)
	# countcells(('s', '?', '?', '?'), w)
	while(1):
		line = raw_input('Enter a command:\n\t')
		if line == 'quit':
			break
		line = line.split('\t')
		if len(line) != 2:
			print "Invalid 1"
			continue
		params = line[1].split(',')
		if len(params) != 4:
			print "Invalid 2"
			continue

		criteria = list()
		location = params[0]
		a = location.split('=')
		if len(a) == 2:
			location = a[0]
			criteria.append(a[1])
		else:
			criteria.append(location)

		category = params[1]
		a = category.split('=')
		if len(a) == 2:
			category = a[0]
			criteria.append(a[1])
		else:
			criteria.append(category)

		rating = params[2]
		a = rating.split('=')
		if len(a) == 2:
			rating = a[0]
			criteria.append(a[1])
		else:
			criteria.append(rating)

		price = params[3]
		a = price.split('=')
		if len(a) == 2:
			price = a[0]
			criteria.append(a[1])
		else:
			criteria.append(price)


		# print location
		if location != 'c' and \
			location != 's' and \
			location != '*':
			print "Invalid location"
			continue
		if category != '*' and \
			category != '?':
			print "Invalid category"
			continue
		if rating != '*' and \
			rating != '?':
			print "Invalid rating"
			continue
		if price != '*' and \
			price != '?':
			print "Invalid price"
			continue

		params = (location, category, rating, price)

		if line[0] == 'cells':
			print "\nCell count in cuboid: " + line[1] + " = [" + str(countcells(params, w)) + "]\n"
		if line[0] == 'count':
			print "\nCell count with params: " + line[1] + " = [" + str(getcounts(w, params, criteria)) + "]\n"
		# print location
		# print category
		# print rating
		# print price

		# print "Option: " + line[0] 
		# print "Params: " + line[1] 
		# print line
		
		

if __name__ == '__main__':
	main('data.txt')
	# w = warehouse('data.txt')
	# for i in range(10):
		# w.printer(i)