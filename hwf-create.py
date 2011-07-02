#!/usr/bin/python3.2

# hanging with friends

import collections

import sys



program_name = sys.argv[0]



# Remove the least common elements from the Counter object.
def remove_least_common(c):

	result = c.copy()

	if len(c) == 0:

		return result

	lowest_count = c.most_common()[-1][1]

	for (k, v) in c.items():
		#for key in c.keys():

		#val = c[key]
		#print("k,v : {},{}".format(k, v))

		if v == lowest_count:
			#if v > lowest_count:

			#result.append(k)
			#result[k] = v

			#del c[k]
			del result[k]
			#del c[key]

	return result




# Get the least common elements from the Counter object.
def get_least_common(c):

	result = []

	if len(c) == 0:

		return result

	lowest_count = c.most_common()[-1][1]

	for (k, v) in c.items():

		#print("k,v : {},{}".format(k, v))

		if v == lowest_count:

			result.append(k)
			#result[k] = v

	return result







if len(sys.argv) < 2:

	exit("must give a string")


s = sys.argv[1].strip()



if len(s) == 0:

	exit('must give a non-empty string')



c0 = collections.Counter(list(s))

##### read input

#chars = str(input()).strip()
#s = input().strip()

print("s={}".format(s))


print("c0.keys={}".format(''.join(c0.keys())))




commands = []

commands.append(r"grep --perl-regexp '^[" + ''.join(c0.keys()) + r"]{4,8}$' wwf.txt")










#i2 = list(s)

#i2.sort()

#print("i2={}".format(''.join(i2)))


print("\n\n")



lowest_count = 0




while len(c0) > 0:
	print("c0={}".format(c0))

	print("len(c0)={}".format(len(c0)))

	print("c0.keys={}".format(''.join(c0.keys())))

	lowest_count = c0.most_common()[-1][1]

	print("lowest_count={}".format(lowest_count))

	least_common = ''.join(get_least_common(c0))

	print("least_common={}".format(least_common))


	##### looks interesting: c0 - collections.Counter(c0.keys())

	commands.append(r"grep --perl-regexp -v '([" + least_common + r"])" + (r".*\1" * lowest_count) + "'")

	c0 = remove_least_common(c0)

	print("\n\n")



print("c0={}".format(c0))

print("lowest_count={}".format(lowest_count))

print("\n\n")




print(' | '.join(commands))




"""

print("len(c1)={}".format(len(c1)))

print("c1.keys={}".format(''.join(c1.keys())))

lowest_count = c1.most_common()[-1][1]

print("lowest_count={}".format(lowest_count))

least_common = get_least_common(c1)

print("least_common={}".format(least_common))

c2 = c1.copy()

remove_least_common(c2)

print("c2={}".format(c2))

print("\n\n")

"""
