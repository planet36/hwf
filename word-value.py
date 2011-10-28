#!/usr/bin/env python3

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


import getopt
import os
import re
import signal
import sys

#-------------------------------------------------------------------------------

__version__ = '2011-10-23'

program_name = os.path.basename(sys.argv[0])

#-------------------------------------------------------------------------------

# default values
default_verbose = False

# mutable values
verbose = default_verbose

#-------------------------------------------------------------------------------

# These are the values of the letters in some Zynga word games.
zynga_letter_values = {
	"A" : 1,
	"B" : 4,
	"C" : 4,
	"D" : 2,
	"E" : 1,
	"F" : 4,
	"G" : 3,
	"H" : 3,
	"I" : 1,
	"J" : 10,
	"K" : 5,
	"L" : 2,
	"M" : 4,
	"N" : 2,
	"O" : 1,
	"P" : 4,
	"Q" : 10,
	"R" : 1,
	"S" : 1,
	"T" : 1,
	"U" : 2,
	"V" : 5,
	"W" : 4,
	"X" : 8,
	"Y" : 3,
	"Z" : 10,
}


def letters_to_letter_values(letters):
	"""Get the letter values of the letters."""
	return [zynga_letter_values.get(letter.upper(), 0) for letter in letters]


def split_bonus_string(bonus_string):
	"""Split the bonus string into an array of bonuses."""
	return re.sub("(DL|TL|DW|TW|.)", r"\1 ", bonus_string).split()


def apply_bonuses(letter_values, bonuses):
	"""Apply the bonuses to the letter values."""

	bonuses_len = len(bonuses)

	word_multiplier = 1

	for i in range(len(letter_values)):

		if i == bonuses_len:
			# There are no more bonuses to apply.
			break

		if bonuses[i] == "DL":
			letter_values[i] *= 2
		elif bonuses[i] == "TL":
			letter_values[i] *= 3
		elif bonuses[i] == "DW":
			word_multiplier *= 2
		elif bonuses[i] == "TW":
			word_multiplier *= 3

	print_verbose("word_multiplier={}".format(word_multiplier))

	if word_multiplier != 1:

		# Apply a word multiplier.
		for i in range(len(letter_values)):

			letter_values[i] *= word_multiplier

#-------------------------------------------------------------------------------

def print_help():
	"""Print the help message and exit."""

	print("""Usage: {} [OPTIONS] [BONUS]

This script calculates the values of words for the game Hanging With Friends <http://www.hangingwithfriends.com/>.

##### BONUS is a string

Use the following convention in the BONUS string.
"Name" = "Bonus"
<any> =  None
DL = Double Letter
TL = Triple Letter
DW = Double Word
TW = Triple Word


Example:
"..TL"
means the first 2 tiles have no bonus and the third tile has a triple letter bonus.
tiles after the end of the bonus string have no bonus applied to them

#####In BONUS, use any character (except 'd', 't', 'l', and 'w') to denote no bonus.  It should be simple like '.', '?', or '_'.


EXAMPLE:
./word-value.py </usr/share/dict/words


cat <<EOT | ./word-value.py
hello
world

electroencephalographically
EOT



OPTIONS

-V, --version
    Print the version information and exit.

-h, --help
    Print this message and exit.

-v, --verbose
    Print diagnostics.
    (default: {})""".format(
		program_name,
		default_verbose))

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

#-------------------------------------------------------------------------------

short_options = 'Vhv'
long_options = ['version', 'help', 'verbose']

try: [options, remaining_args] = getopt.getopt(sys.argv[1:], short_options, long_options)

except getopt.GetoptError as err: print_error(err)

for [option, value] in options:
	if   option in ['-V', '--version'] : print_version()
	elif option in ['-h', '--help'] : print_help()
	elif option in ['-v', '--verbose'] : verbose = True
	else : print_error("Unhandled option '{}'.".format(option))

#-------------------------------------------------------------------------------

def signal_handler(signal_num, execution_frame):
	print()
	exit(0)

signal.signal(signal.SIGINT, signal_handler) # Interactive attention signal. (Ctrl-C)
signal.signal(signal.SIGTERM, signal_handler) # Termination request. (kill default signal)

#-------------------------------------------------------------------------------

print_verbose("remaining_args={}".format(remaining_args))

if len(remaining_args) == 0:

	# The default value of the bonus string is an empty string.
	remaining_args.append('')

#-------------------------------------------------------------------------------

bonus_string = remaining_args[0].strip().upper()
print_verbose("bonus_string={}".format(bonus_string))

bonuses = split_bonus_string(bonus_string)
print_verbose("bonuses={}".format(bonuses))

#-------------------------------------------------------------------------------

for line in sys.stdin:

	line = line.rstrip(os.linesep)

	if len(line) == 0:
		continue

	letter_values = letters_to_letter_values(line)

	if bonus_string != '':
		apply_bonuses(letter_values, bonuses)

	print_verbose("letter_values={}".format(letter_values))

	print("{}\t{}".format(sum(letter_values), line))
