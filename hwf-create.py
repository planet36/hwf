#!/usr/bin/python3.2

"""
Copyright (C) 2011 Steve Ward

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import collections
import getopt
#import os
#import re
#import signal
import sys


program_name = sys.argv[0]


# default values

default_verbose = False

default_dictionary = '~/wwf.txt'


# mutable values

verbose = default_verbose

dictionary = default_dictionary



##### usage: ./hwf-create.py [--dictionary=FILE] ndyvefambuaw











def print_version():
	"""Print the version information and exit."""

	print(program_name + " 2011-06-28")

	print("Written by Steve Ward")

	exit(0)


def print_verbose(s):
	"""Print the message if verbose mode is on."""

	if verbose: print("# {}".format(s))


def print_warning(s):
	"""Print the warning message and continue."""

	print("Warning: {}".format(s), file=sys.stderr)

	#cleanup()


def print_error(s):
	"""Print the error message and exit."""

	print("Error: {}".format(s), file=sys.stderr)

	print("Try '{} --help' for more information.".format(program_name))

	#cleanup()

	exit(1)






























# Get the least common elements from the Counter object.
def get_least_common(c):

	lowest_count = c.most_common()[-1][1]

	return [key for key in c if c[key] == lowest_count]


# Remove the least common elements from the Counter object.
def remove_least_common(c):

	for key in get_least_common(c):

		del c[key]




##### parse options

for arg in sys.argv[1:]:

	#print("arg={}".format(arg))

	if len(arg) == 0:

		continue

	c = collections.Counter(list(arg))

	commands = []

	commands.append("grep --perl-regexp '^[" + ''.join(c.keys()) + "]{4,8}$' " + dictionary)

	while len(c) > 0:

		#print("c={}".format(c))

		#print("len(c)={}".format(len(c)))

		#print("c.keys={}".format(''.join(c.keys())))

		lowest_count = c.most_common()[-1][1]

		#print("lowest_count={}".format(lowest_count))

		least_common = ''.join(get_least_common(c))

		#print("least_common={}".format(least_common))

		##### looks interesting: c - collections.Counter(c.keys())

		commands.append("grep --perl-regexp --invert-match '([" + least_common + "])" + (r".*\1" * lowest_count) + "'")

		remove_least_common(c)

		#print("\n\n")


	print(' | '.join(commands))
