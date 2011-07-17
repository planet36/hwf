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

default_min_length = 4

default_max_length = 8

default_words_file = "words"


# mutable values

verbose = default_verbose

min_length = default_min_length

max_length = default_max_length

words_file = default_words_file


#-------------------------------------------------------------------------------


def get_least_common_keys(c):
	"""Get the keys of the least common elements from the Counter object."""

	lowest_count = c.most_common()[-1][1]

	return [key for key in c if c[key] == lowest_count]


def remove_least_common_keys(c):
	"""Remove the keys of the least common elements from the Counter object."""

	for key in get_least_common_keys(c):

		del c[key]


#-------------------------------------------------------------------------------


def matches_any(string, regexes):
	"""Determine if the string matches any of the regular expressions."""

	for regex in regexes:

		if re.search(regex, string):

			return True

	return False


def matches_none(string, regexes):
	"""Determine if the string matches none of the regular expressions."""

	return not matches_any(string, regexes)


def matches_all(string, regexes):
	"""Determine if the string matches all of the regular expressions."""

	for regex in regexes:

		if not re.search(regex, string):

			return False

	return True


#-------------------------------------------------------------------------------


def print_help():
	"""Print the help message and exit."""

	print("""Usage: {} [OPTIONS] LETTERS
Create a word using LETTERS.
#####
This script uses LETTERS to find words that may be used in the game Hanging With Friends <http://www.hangingwithfriends.com/>.
#####
Find words composed of a subset of LETTERS.  The words may be used in the game Hanging With Friends <http://www.hangingwithfriends.com/>.


The LETTERS string is converted to lowercase and non-lowercase characters are excluded.
#####
Non-alphabetical characters in LETTERS are ignored.

OPTIONS:

-V, --version
        Print the version information and exit.

-h, --help
        Print this message and exit.

-v, --verbose
        Print diagnostics.
        (default: {})

--min=N
        Set the minimum length of the matched words.  It must be at least 1.
        (default: {})

--max=N
        Set the maximum length of the matched words.  It must be at least the minimum length.
        (default: {})

-w, --words=FILE
        Use FILE as the words file.
        (default: {})""".format(
        	program_name,
            default_verbose,
            default_min_length,
            default_max_length,
            default_words_file))

	exit(0)


def print_version():
	"""Print the version information and exit."""

	print(program_name + " 2011-07-11")

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


short_options = "Vhvw:"
long_options = ["version", "help", "verbose", "min=", "max=", "words="]

try: (options, remaining_args) = getopt.getopt(sys.argv[1:], short_options, long_options)

except getopt.GetoptError as err: print_error(err.msg)

for (option, value) in options:

	if   option in ("-V", "--version") : print_version()
	elif option in ("-h", "--help") : print_help()
	elif option in ("-v", "--verbose") : verbose = True
	elif option in ("--min") : min_length = int(value)
	elif option in ("--max") : max_length = int(value)
	elif option in ("-w", "--words") : words_file = value
	else : print_error("Unhandled option '{}'.".format(option))


#-------------------------------------------------------------------------------


print_verbose("remaining_args={}".format(remaining_args))


if len(remaining_args) == 0:

	print_error("Must give 1 operand.")


#-------------------------------------------------------------------------------
# Validate the minimum length.

print_verbose("min_length={}".format(min_length))

if min_length < 1:

	print_error("Minimum length ({}) must be at least 1.".format(min_length))


#-------------------------------------------------------------------------------
# Validate the maximum length.

print_verbose("max_length={}".format(max_length))

if max_length < min_length:

	print_error("Maximum length ({}) must be at least the minimum length ({}).".format(max_length, min_length))


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


#-------------------------------------------------------------------------------


letters = remaining_args[0]

print_verbose("letters={}".format(letters))

# Convert the string to lowercase.
letters = letters.lower()

print_verbose("letters={}".format(letters))

# Remove all non-lowercase characters.
letters = re.sub("[^a-z]", "", letters)

print_verbose("letters={}".format(letters))

if len(letters) == 0:

	print_error("Must give a string that contains letters.")

# Remove duplicate letters and sort the letters.
# Include words that are composed of only the letters.
positive_regex = "^[" + "".join(sorted(set(letters))) + "]{" + str(min_length) + "," + str(max_length) + "}$"

print_verbose("positive_regex={}".format(positive_regex))

##### these are shell commands that could be executed to get the same results as this script.
# An array of shell commands that could be executed to get the same results as this script.
commands = []

command = "grep --perl-regexp '" + positive_regex + "' '" + words_file + "'"

print_verbose("command={}".format(command))

commands.append(command)

negative_regexes = []

letters_count = collections.Counter(letters)

while len(letters_count) > 0:

	print_verbose("letters_count={}".format(letters_count))

	least_common_letters = "".join(sorted(get_least_common_keys(letters_count)))

	print_verbose("least_common_letters={}".format(least_common_letters))

	lowest_count = letters_count.most_common()[-1][1]

	print_verbose("lowest_count={}".format(lowest_count))

	assert lowest_count != 0

	# Exclude the least common letters that are repeated more than lowest_count times.
	negative_regex = "([" + least_common_letters + "])" + (r".*?\1" * lowest_count)

	print_verbose("negative_regex={}".format(negative_regex))

	negative_regexes.append(negative_regex)

	command = "grep --perl-regexp --invert-match '" + negative_regex + "'"

	print_verbose("command={}".format(command))

	commands.append(command)

	remove_least_common_keys(letters_count)

print_verbose(" | ".join(commands))

print_verbose("negative_regexes={}".format(negative_regexes))


#-------------------------------------------------------------------------------


# For each word that matches the positive regex,
for word in re.findall(positive_regex, words, flags=re.MULTILINE):

	# If the word matches none of the negative regexes,
	if matches_none(word, negative_regexes):

		print(word)

