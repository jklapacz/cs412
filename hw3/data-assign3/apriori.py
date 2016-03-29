from sys import argv
from infra import *
usage = "python apriori.py [input filename] [output filename] [min-sup (between 0 and 1)]"
from time import clock




def main(infile, outfile, min_sup):
	a = apriori(infile, outfile, min_sup)
	a.process_input()
	# a.generate_itemset(0)
	a.pattern_mining()
	a.closed_mining()
if __name__ == '__main__':
	if len(argv) != 4:
		print usage
		quit()
	now = clock()
	main(argv[1], argv[2], argv[3])
	elapsed = clock() - now
	print "Apriori ran in [" + str(elapsed) + "] seconds"
