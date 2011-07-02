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
import sys


program_name = sys.argv[0]


# default values

default_verbose = False

default_dictionary = '/usr/share/dict/words'


# mutable values

verbose = default_verbose

dictionary = default_dictionary


#-------------------------------------------------------------------------------


def print_help():
	"""Print the help message and exit."""

	print('''Usage: {} [OPTIONS] WORD-PATTERN EXCLUDED-LETTERS
This script finds possible words that match WORD-PATTERN for the game "Hanging With Friends".
##### creates a command to find possible words using LETTERS for the game "Hanging With Friends".

In the word pattern, use '.' to denote an unknown letter.

#####

OPTIONS:

-V, --version
        Print the version information and exit.

-h, --help
        Print this message and exit.

-v, --verbose
        Print diagnostics.
        (default: {})

-d, --dictionary=FILE
        Use FILE as the dictionary.
        (default: {})'''.format(
        	program_name,
            default_verbose,
            default_dictionary))

	exit(0)


def print_version():
	"""Print the version information and exit."""

	print(program_name + " 2011-06-29")

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


short_options = 'Vhvd:'
long_options = ['version', 'help', 'verbose', 'dictionary=']

try: (options, remaining_args) = getopt.getopt(sys.argv[1:], short_options, long_options)

except getopt.GetoptError as err: print_error(err.msg)

for (option, value) in options:

	if   option in ('-V', '--version') : print_version()
	elif option in ('-h', '--help') : print_help()
	elif option in ('-v', '--verbose') : verbose = True
	elif option in ('-d', '--dictionary') : dictionary = value
	else : print_error("Unhandled option '{}'.".format(option))


#-------------------------------------------------------------------------------
# Validate dictionary.

print_verbose("dictionary={}".format(dictionary))


if not os.path.exists(dictionary):

	print_error("Dictionary '{}' does not exist.".format(dictionary))


if not os.path.isfile(dictionary):

	print_error("Dictionary '{}' is not a file.".format(dictionary))


if not os.access(dictionary, os.R_OK):

	print_error("Dictionary '{}' is not readable.".format(dictionary))


#-------------------------------------------------------------------------------


print_verbose("remaining_args={}".format(remaining_args))


if len(remaining_args) == 0:

	print_error("Must give at least 1 operand.")


if len(remaining_args) == 1:

	# The default value of excluded_letters is an empty string.
	remaining_args.append('')


#-------------------------------------------------------------------------------

# Read the contents of the dictionary file.

f = open(dictionary)

dictionary_words = f.readlines()

f.close()

# Strip whitespace from all lines.
dictionary_words = map(str.strip, dictionary_words)

##### move this somewhere else

#dictionary_anagrams = [''.join(sorted(dictionary_word)) for dictionary_word in dictionary_words]

#dictionary_anagrams_count = collections.Counter(dictionary_anagrams)


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
excluded_letters = ''.join(sorted(excluded_letters))

print_verbose("excluded_letters={}".format(excluded_letters))


#-------------------------------------------------------------------------------

if len(excluded_letters) != 0:

	# Replace the unknown letter pattern with the excluded letters pattern.
	word_pattern = re.sub('\.', '[^' + excluded_letters + ']', word_pattern)

	print_verbose("word_pattern={}".format(word_pattern))


word_pattern = re.compile(word_pattern)


#-------------------------------------------------------------------------------


letters_count = collections.Counter()

# Search for the word pattern in the dictionary words.
for dictionary_word in dictionary_words:

	if re.search(word_pattern, dictionary_word):

		letters_count += collections.Counter(dictionary_word)

		print(dictionary_word)

print_verbose("letters_count={}".format(letters_count))


#-------------------------------------------------------------------------------


# Remove excluded letters from the letters count.
for excluded_letter in excluded_letters:

	if excluded_letter in letters_count:

		del letters_count[excluded_letter]

print_verbose("letters_count={}".format(letters_count))


if len(letters_count) > 0:

	print("  ".join(["{}={}".format(k.upper(), v) for (k, v) in letters_count.most_common()]))
