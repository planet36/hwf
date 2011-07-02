#!/usr/bin/python3

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
import sys


program_name = sys.argv[0]


# default values

default_verbose = False

default_words_file = 'words'


# mutable values

verbose = default_verbose

words_file = default_words_file


#-------------------------------------------------------------------------------


def print_help():
	"""Print the help message and exit."""

	print('''Usage: {} [OPTIONS] WORD-PATTERN [EXCLUDED-LETTERS]
This script finds possible words that match WORD-PATTERN for the game Hanging With Friends <http://www.hangingwithfriends.com/>.

In WORD-PATTERN, use the dot character ('.') to denote an unknown letter.

#####

OPTIONS:

-V, --version
        Print the version information and exit.

-h, --help
        Print this message and exit.

-v, --verbose
        Print diagnostics.
        (default: {})

-w, --words=FILE
        Use FILE as the words file.
        (default: {})'''.format(
        	program_name,
            default_verbose,
            default_words_file))

	exit(0)


def print_version():
	"""Print the version information and exit."""

	print(program_name + " 2011-06-30")

	print("Written by Steve Ward")

	exit(0)


def print_verbose(s):
	"""Print the message if verbose mode is on."""

	if verbose: print("# {}".format(s))


def print_warning(s):
	"""Print the warning message and continue."""

	print("Warning: {}".format(s), file=sys.stderr)


def print_error(s):
	"""Print the error message and exit."""

	print("Error: {}".format(s), file=sys.stderr)

	print("Try '{} --help' for more information.".format(program_name))

	exit(1)


#-------------------------------------------------------------------------------


short_options = 'Vhvw:'
long_options = ['version', 'help', 'verbose', 'words=']

try: (options, remaining_args) = getopt.getopt(sys.argv[1:], short_options, long_options)

except getopt.GetoptError as err: print_error(err.msg)

for (option, value) in options:

	if   option in ('-V', '--version') : print_version()
	elif option in ('-h', '--help') : print_help()
	elif option in ('-v', '--verbose') : verbose = True
	elif option in ('-w', '--words') : words_file = value
	else : print_error("Unhandled option '{}'.".format(option))


#-------------------------------------------------------------------------------


print_verbose("remaining_args={}".format(remaining_args))


if len(remaining_args) == 0:

	print_error("Must give at least 1 operand.")


if len(remaining_args) == 1:

	# The default value of the excluded letters is an empty string.
	remaining_args.append('')


#-------------------------------------------------------------------------------
# Validate the words file.

print_verbose("words_file={}".format(words_file))


if not os.path.exists(words_file):

	print_error("Words file '{}' does not exist.".format(words_file))


if not os.path.isfile(words_file):

	print_error("Words file '{}' is not a file.".format(words_file))


if not os.access(words_file, os.R_OK):

	print_error("Words file '{}' is not readable.".format(words_file))


#-------------------------------------------------------------------------------

# Read the contents of the words file.

f = open(words_file)

words = f.read()

f.close()

##### move this somewhere else

#words_anagrams = [''.join(sorted(word)) for word in words]

#words_anagrams_count = collections.Counter(words_anagrams)


#-------------------------------------------------------------------------------
# Validate the word pattern.

word_pattern = remaining_args[0].strip()

print_verbose("word_pattern={}".format(word_pattern))

# Convert the string to lowercase.
word_pattern = word_pattern.lower()

print_verbose("word_pattern={}".format(word_pattern))

# Remove characters not matching lowercase letters and unknown letters.
word_pattern = re.sub('[^a-z.]', '', word_pattern)

print_verbose("word_pattern={}".format(word_pattern))

if len(word_pattern) == 0:

	print_error("Must give non-empty word pattern.")

# Enclose the word pattern with anchors.
word_pattern = '^' + word_pattern + '$'

print_verbose("word_pattern={}".format(word_pattern))


#-------------------------------------------------------------------------------
# Validate the excluded letters.

excluded_letters = remaining_args[1].strip()

print_verbose("excluded_letters={}".format(excluded_letters))

# Convert the string to lowercase.
excluded_letters = excluded_letters.lower()

print_verbose("excluded_letters={}".format(excluded_letters))

# Remove characters not matching lowercase letters.
excluded_letters = re.sub('[^a-z]', '', excluded_letters)

print_verbose("excluded_letters={}".format(excluded_letters))

# Add letters in the word pattern to the excluded letters.
excluded_letters += re.sub('[^a-z]', '', word_pattern)

print_verbose("excluded_letters={}".format(excluded_letters))

# Remove duplicate letters and sort the letters.
excluded_letters = ''.join(sorted(set(excluded_letters)))

print_verbose("excluded_letters={}".format(excluded_letters))


#-------------------------------------------------------------------------------

if len(excluded_letters) != 0:

	# Replace the unknown letter pattern with the excluded letters pattern.
	##### must include newline in negative character class in multiline mode
	word_pattern = re.sub('\.', r'[^\n' + excluded_letters + ']', word_pattern)
	#word_pattern = re.sub('\.', '[a-z&&' + r'[^\n' + excluded_letters + ']]', word_pattern)
	#word_pattern = re.sub('\.', '[a-z-' + r'[\n' + excluded_letters + ']]', word_pattern)

	print_verbose("word_pattern={}".format(word_pattern))


#-------------------------------------------------------------------------------

letters_count = collections.Counter()

for word in re.findall(word_pattern, words, flags=re.MULTILINE):

	#if word.find('\n'):
	#if '\n' in word:
		#print(r"word ({}) has \n".format(word))

	#letters_count += collections.Counter(word)
	##### try this:  find the letters that occur in the most words, rather than the letters that occur most often
	##### don't count duplicate letters in a word; count only if the letters appear
	letters_count += collections.Counter(set(word))

	print(word)

print_verbose("letters_count={}".format(letters_count))

#-------------------------------------------------------------------------------

# Remove excluded letters from the letters count.
for excluded_letter in excluded_letters:

	if excluded_letter in letters_count:

		del letters_count[excluded_letter]

print_verbose("letters_count={}".format(letters_count))

"""
#letters_count_inverse = collections.defaultdict(list)

# Invert the keys and values of the letters count.
#for (k, v) in letters_count.items():

	#letters_count_inverse[v].append(k)
"""

for (k, v) in reversed(letters_count.most_common()):

	print("{}={}".format(k.upper(), v))


##### remove this later
if len(letters_count) > 0:

	"""
	#for (k,v) in letters_count_inverse.items():
		#for (k,v) in reversed(list(letters_count_inverse.items())):

		#print("{} = {}".format(k, ' '.join(sorted([x.upper() for x in v]))))
		#print("{} = {}".format(k, ' '.join(sorted(map(str.upper, v)))))

	#print("    ".join(["{} = {}".format(k, ' '.join(sorted([x.upper() for x in v]))) for (k,v) in letters_count_inverse.items()]))
	"""

	#print("  ".join(["{}={}".format(k.upper(), v) for (k, v) in letters_count.most_common()]))
	#print("\n".join(["{}={}".format(k.upper(), v) for (k, v) in letters_count.most_common()]))
	#print("\n".join(["{}={}".format(k.upper(), v) for (k, v) in reversed(letters_count.most_common())]))
	pass

##### 327 283
