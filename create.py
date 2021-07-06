# SPDX-FileCopyrightText: Steven Ward
# SPDX-License-Identifier: OSL-3.0

import collections
import getopt
import os
import re
import sys


__author__ = 'Steven Ward'
__version__ = '2012-12-10'

program_name = os.path.basename(sys.argv[0])


# default values
default_verbose = False
default_show_command = False
default_max_length = 8
default_min_length = 4
default_words_file = 'words'

# mutable values
verbose = default_verbose
show_command = default_show_command
max_length = default_max_length
min_length = default_min_length
words_file = default_words_file


def get_least_common_keys(c):
	"""Get the keys of the least common elements from the Counter object."""

	lowest_count = c.most_common()[-1][1]

	return [key for key in c if c[key] == lowest_count]


def remove_least_common_keys(c):
	"""Remove the keys of the least common elements from the Counter object."""

	for key in get_least_common_keys(c):
		del c[key]


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


def print_help():
	"""Print the help message and exit."""

	print("""Usage: {} [OPTIONS] LETTERS
Create a word using LETTERS.
#####
This program finds words using LETTERS that may be used in the game Hanging With Friends <http://www.hangingwithfriends.com/>.
#####
Find words composed of a subset of LETTERS.  The words may be used in the game Hanging With Friends <http://www.hangingwithfriends.com/>.


The LETTERS string is converted to lowercase and non-lowercase characters are excluded.
#####
Non-alphabetical characters in LETTERS are ignored.

OPTIONS

-V, --version
    Print the version information and exit.

-h, --help
    Print this message and exit.

-v, --verbose
    Print diagnostics.
    (default: {})

--show-command
    Print the command to #####
    (default: {})

--max=N
    Set the maximum length of the matched words.  It must be at least the minimum length.
    (default: {})

--min=N
    Set the minimum length of the matched words.  It must be at least 1.
    (default: {})

-w, --words=FILE
    Use FILE as the words file.
    (default: {})""".format(
		program_name,
		default_verbose,
		default_show_command,
		default_max_length,
		default_min_length,
		default_words_file))

	exit(0)


def print_version():
	"""Print the version information and exit."""
	print("{} {}".format(program_name, __version__))
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


short_options = 'Vhvw:'
long_options = ['version', 'help', 'verbose', 'show-command', 'hide-command', 'max=', 'min=', 'words=']

try: [options, remaining_args] = getopt.getopt(sys.argv[1:], short_options, long_options)

except getopt.GetoptError as err: print_error(err)

for [option, value] in options:

	if   option in ['-V', '--version'] : print_version()
	elif option in ['-h', '--help'] : print_help()
	elif option in ['-v', '--verbose'] : verbose = True

	##### work on the best option names
	elif option in ['--command'] : show_command = True
	elif option in ['--show-command'] : show_command = True
	elif option in ['--hide-command'] : show_command = False
	elif option in ['--no-command'] : show_command = True
	#####

	elif option in ['--max'] : max_length = int(value)
	elif option in ['--min'] : min_length = int(value)
	elif option in ['-w', '--words'] : words_file = value
	else : print_error("Unhandled option '{}'.".format(option))


print_verbose("remaining_args={}".format(remaining_args))

if len(remaining_args) == 0:
	print_error("Must give 1 operand.")

# Validate the maximum length.

print_verbose("max_length={}".format(max_length))

if max_length < min_length:
	print_error("Maximum length ({}) must be at least the minimum length ({}).".format(max_length, min_length))

# Validate the minimum length.

print_verbose("min_length={}".format(min_length))

if min_length < 1:
	print_error("Minimum length ({}) must be at least 1.".format(min_length))

# Validate the words file.

print_verbose("words_file={}".format(words_file))

if not os.path.exists(words_file):
	print_error("Words file '{}' does not exist.".format(words_file))

if not os.path.isfile(words_file):
	print_error("Words file '{}' is not a file.".format(words_file))

if not os.access(words_file, os.R_OK):
	print_error("Words file '{}' is not readable.".format(words_file))

# Read the contents of the words file.

with open(words_file) as f:
	words = f.read()


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

# An array of shell commands that could be executed to get the same results as this script.
commands = []

# Exclude words that have too many letters. #####
negative_regexes = []

# Remove duplicate letters and sort the letters.
# Include words that are composed of only the letters.
positive_regex = '^[' + ''.join(sorted(set(letters))) + ']{' + str(min_length) + ',' + str(max_length) + '}$'
print_verbose("positive_regex={}".format(positive_regex))

command = "grep --perl-regexp '" + positive_regex + "' '" + words_file + "'"
commands.append(command)

letters_count = collections.Counter(letters)
print_verbose("letters_count={}".format(letters_count))

while len(letters_count) > 0:

	least_common_letters = ''.join(sorted(get_least_common_keys(letters_count)))
	print_verbose("least_common_letters={}".format(least_common_letters))

	lowest_count = letters_count.most_common()[-1][1]
	print_verbose("lowest_count={}".format(lowest_count))

	assert lowest_count != 0

	# Exclude the least common letters that are repeated more than lowest_count times.
	negative_regex = "([" + least_common_letters + "])" + (r".*?\1" * lowest_count)
	print_verbose("negative_regex={}".format(negative_regex))
	negative_regexes.append(negative_regex)

	command = "grep --perl-regexp --invert-match '" + negative_regex + "'"
	commands.append(command)

	remove_least_common_keys(letters_count)
	print_verbose("letters_count={}".format(letters_count))

if show_command:
	print(" | ".join(commands))


# For each word that matches the positive regex,
for word in re.findall(positive_regex, words, flags=re.MULTILINE):

	# If the word matches none of the negative regexes,
	if matches_none(word, negative_regexes):
		print(word)
