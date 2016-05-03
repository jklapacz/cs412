name = "data-assign3/topic-0.txt"

f = open(name)
counter = 0
alt = 0
for line in f.readlines():
	curr_line = line.split()
	if "390" in curr_line:
	# if "723" in curr_line:
		if "382" in curr_line:
			counter += 1
		else:
			alt += 1
print counter, alt