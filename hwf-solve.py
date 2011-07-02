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
import os
import re
#import signal
import sys


program_name = sys.argv[0]


##### usage: ./hwf-solve.py ~/wwf.txt ..i.a. iaste
##### usage: ./hwf-solve.py [--dictionary=FILE] ..i.a. iaste



















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





















"""
def signal_handler(signal_num, execution_frame):

	print()

	exit(0)


signal.signal(signal.SIGINT, signal_handler) # Interactive attention signal. (Ctrl-C)
signal.signal(signal.SIGTERM, signal_handler) # Termination request. (kill default signal)
"""


if len(sys.argv) < 4:

	exit("must give 3 strings")



##### this should be an option later
dictionary = sys.argv[1].strip()


if not os.path.exists(dictionary):

	exit("file does not exist")


if not os.path.isfile(dictionary):

	exit("file is not a file")


if not os.access(dictionary, os.R_OK):

	exit("file is not readable")


f = open(dictionary, mode='r')

dictionary_words = f.readlines()

f.close()

dictionary_words = map(str.strip, dictionary_words)

#dictionary_anagrams = [''.join(sorted(dictionary_word)) for dictionary_word in dictionary_words]

#dictionary_anagrams_count = collections.Counter(dictionary_anagrams)


unknown_letter_pattern = re.compile('\.')


sed_command = r"sed --unbuffered --regexp-extended 's/([[:alpha:]])([[:alpha:]])/\1\n\2/g'"


#while True:

#word_pattern = raw_input('Enter word_pattern: ').strip()
word_pattern = sys.argv[2].strip()

#print("word_pattern={}".format(word_pattern))

if len(word_pattern) == 0:

	exit("Must give non-empty word pattern.")

	#continue

#excluded_letters = raw_input('Enter excluded letters: ').strip()
excluded_letters = sys.argv[3].strip()

#print("excluded_letters={}".format(excluded_letters))

if len(excluded_letters) == 0:

	exit("Must give non-empty excluded letters.")

	#continue

#excluded_letters_character_class = '[^' + excluded_letters + ']'

#print()

pattern = '^' + re.sub(unknown_letter_pattern, '[^' + excluded_letters + ']', word_pattern) + '$'




pattern = re.compile(pattern)

word_matches = []

for dictionary_word in dictionary_words:

	# re.search(pattern, string, flags=0)
	if re.search(pattern, dictionary_word):

		word_matches.append(dictionary_word)

		print(dictionary_word)

#print()

letters_count = collections.Counter(list(''.join(word_matches)))

#print("letters_count={}".format(letters_count))

for excluded_letter in list(excluded_letters):

	if excluded_letter in letters_count:

		del letters_count[excluded_letter]



##### print this in a better way
#print("letters_count={}".format(letters_count))
#print("letters_count={}".format(dict(letters_count)))

#print(letters_count)
##### casting to dict loses order
#print(dict(letters_count))

#print(letters_count.most_common())


#for (k, v) in letters_count.most_common():

	#print("{}={}".format(string.upper(k), v), end="  ")
	#print("{}={}".format(k.upper(), v), end="  ")


#print()
#import pprint



#print("  ".join(["{}={}".format(string.upper(k), v) for (k, v) in letters_count.most_common()]))
print("  ".join(
			["{}={}".format(k.upper(), v) for (k, v) in letters_count.most_common()]
		)
	)

#pprint.pprint(letters_count)
#pprint.pprint(dict(letters_count))


#print()

#exit()
#continue


"""

commands = []
# Substitute unknown letters with the excluded letters character class.
# re.sub(pattern, repl, string)
commands.append("grep --perl-regexp '{}' {}".format(pattern, dictionary))
commands.append(sed_command)
commands.append(sed_command)
commands.append("grep --perl-regexp '[^{}]'".format(excluded_letters))
commands.append("sort")
commands.append("uniq --count")
commands.append("sort -g")

print()
print(' | '.join(commands))
print()


"""

