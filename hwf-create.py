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

	print('''Usage: {} [OPTIONS] LETTERS [LETTERS...]
This script creates a command to find possible words using LETTERS for the game "Hanging With Friends".

LETTERS is converted to lowercase and non-lowercase characters are excluded. #####

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
        FILE is not opened.  It is only printed in the created command. #####
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


##### remove later
"""
#-------------------------------------------------------------------------------
# Validate dictionary.

if not os.path.exists(dictionary):

	print_warning("Dictionary '{}' does not exist.".format(dictionary))


if not os.path.isfile(dictionary):

	print_warning("Dictionary '{}' is not a file.".format(dictionary))


if not os.access(dictionary, os.R_OK):

	print_warning("Dictionary '{}' is not readable.".format(dictionary))
"""


#-------------------------------------------------------------------------------


print_verbose("remaining_args={}".format(remaining_args))


if len(remaining_args) == 0:

	print_error("Must give at least 1 operand.")


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


for letters in remaining_args:

	print_verbose("letters={}".format(letters))

	# Convert the string to lowercase.
	letters = letters.lower()

	print_verbose("letters={}".format(letters))

	# Remove all non-lowercase characters.
	letters = re.sub('[^a-z]', '', letters)

	print_verbose("letters={}".format(letters))

	if len(letters) == 0:

		continue

	letters_count = collections.Counter(letters)

	# Remove duplicate letters and sort the letters.
	letters = ''.join(sorted(letters))

	print_verbose("letters={}".format(letters))

	commands = []

	# Include words that are composed of only the letters.
	command = "grep --perl-regexp '^[" + ''.join(letters) + "]{4,8}$' '" + dictionary + "'"

	print_verbose("command={}".format(command))

	commands.append(command)

	while len(letters_count) > 0:

		print_verbose("letters_count={}".format(letters_count))

		least_common_letters = ''.join(sorted(get_least_common_keys(letters_count)))

		print_verbose("least_common_letters={}".format(least_common_letters))

		lowest_count = letters_count.most_common()[-1][1]

		assert lowest_count != 0

		print_verbose("lowest_count={}".format(lowest_count))

		# Exclude the least common letters that are repeated more than lowest_count times.
		command = "grep --perl-regexp --invert-match '([" + least_common_letters + "])" + (r".*?\1" * lowest_count) + "'"

		print_verbose("command={}".format(command))

		commands.append(command)

		remove_least_common_keys(letters_count)

	print(' | '.join(commands))
