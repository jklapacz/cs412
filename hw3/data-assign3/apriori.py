from sys import argv
from infra import *
usage = "python apriori.py [input filename] [output filename] [min-sup (between 0 and 1)]"





def main(infile, outfile, min_sup):
	a = apriori(infile, outfile, min_sup)
	a.process_input()
	print a
	# a.generate_itemset(0)
	a.patter_mining()
if __name__ == '__main__':
	if len(argv) != 4:
		print usage
		quit()
	main(argv[1], argv[2], argv[3])

