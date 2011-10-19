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

import collections
import getopt
import os
import re
import sys


program_name = sys.argv[0]


# default values

default_verbose = False

default_last_vowel_given = True

default_words_file = "words"


# mutable values

verbose = default_verbose

last_vowel_given = default_last_vowel_given

words_file = default_words_file


#-------------------------------------------------------------------------------


def print_help():
	"""Print the help message and exit."""

	print("""Usage: {} [OPTIONS] WORD-PATTERN [EXCLUDED-LETTERS]
This program finds possible words that match WORD-PATTERN for the game Hanging With Friends <http://www.hangingwithfriends.com/>.
#####
Find words that match WORD-PATTERN but do not have EXCLUDED-LETTERS.
#####

In WORD-PATTERN, use the dot ('.') or question mark ('?') to denote an unknown letter.

OPTIONS:

-V, --version
        Print the version information and exit.

-h, --help
        Print this message and exit.

-v, --verbose
        Print diagnostics.
        (default: {})

--last-vowel
        Indicate that the last vowel is given in WORD-PATTERN.  Use '--no-last-vowel' to indicate that the last vowel is not given in WORD-PATTERN.
        ##### Hanging With Friends has a rule about always showing the last vowel when presenting a word pattern to the user to solve.
        ##### all unknown letters after the last vowel need to have all vowels [aeiou] in the negative character class
        (default: {})

-w, --words=FILE
        Use FILE as the words file.
        (default: {})""".format(
		program_name,
		default_verbose,
		default_last_vowel_given,
		default_words_file))

	exit(0)


def print_version():
	"""Print the version information and exit."""

	print(program_name + " 2011-07-011")

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
long_options = ["version", "help", "verbose", "last-vowel", "no-last-vowel", "words="]

try: (options, remaining_args) = getopt.getopt(sys.argv[1:], short_options, long_options)

except getopt.GetoptError as err: print_error(err)

for (option, value) in options:

	if   option in ("-V", "--version") : print_version()
	elif option in ("-h", "--help") : print_help()
	elif option in ("-v", "--verbose") : verbose = True
	elif option in ("--last-vowel") : last_vowel_given = True
	elif option in ("--no-last-vowel") : last_vowel_given = False
	elif option in ("-w", "--words") : words_file = value
	else : print_error("Unhandled option '{}'.".format(option))


#-------------------------------------------------------------------------------


print_verbose("remaining_args={}".format(remaining_args))


if len(remaining_args) == 0:

	print_error("Must give at least 1 operand.")


if len(remaining_args) == 1:

	# The default value of the excluded letters is an empty string.
	remaining_args.append("")


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
# Validate the word pattern.

word_pattern = remaining_args[0].strip()

print_verbose("word_pattern={}".format(word_pattern))

# Convert the string to lowercase.
word_pattern = word_pattern.lower()

print_verbose("word_pattern={}".format(word_pattern))

# Remove characters not matching lowercase letters and unknown letters.
word_pattern = re.sub("[^a-z.?]", "", word_pattern)

print_verbose("word_pattern={}".format(word_pattern))

if len(word_pattern) == 0:

	print_error("Must give non-empty word pattern.")


#-------------------------------------------------------------------------------
# Validate the excluded letters.

excluded_letters = remaining_args[1].strip()

print_verbose("excluded_letters={}".format(excluded_letters))

# Convert the string to lowercase.
excluded_letters = excluded_letters.lower()

print_verbose("excluded_letters={}".format(excluded_letters))

# Remove characters not matching lowercase letters.
excluded_letters = re.sub("[^a-z]", "", excluded_letters)

print_verbose("excluded_letters={}".format(excluded_letters))

# Add letters in the word pattern to the excluded letters.
excluded_letters += re.sub("[^a-z]", "", word_pattern)

print_verbose("excluded_letters={}".format(excluded_letters))

# Remove duplicate letters and sort the letters.
excluded_letters = "".join(sorted(set(excluded_letters)))

print_verbose("excluded_letters={}".format(excluded_letters))

# Add all the vowels to the excluded letters pattern.
# Remove duplicate letters and sort the letters.
excluded_letters_vowels = "".join(sorted(set(excluded_letters + "aeiou")))

print_verbose("excluded_letters_vowels={}".format(excluded_letters_vowels))

# In multiline mode, the newline must be included in the negative character class.
excluded_letters_pattern = "[^" + excluded_letters + r"\n]"

print_verbose("excluded_letters_pattern={}".format(excluded_letters_pattern))

# In multiline mode, the newline must be included in the negative character class.
excluded_letters_vowels_pattern = "[^" + excluded_letters_vowels + r"\n]"

print_verbose("excluded_letters_vowels_pattern={}".format(excluded_letters_vowels_pattern))


#-------------------------------------------------------------------------------


last_vowel_index = -1

last_vowel_pattern = "[aeiou][^aeiou]*$"

# Search for the last vowel in the word pattern.
last_vowel_match = re.search(last_vowel_pattern, word_pattern)

# If a vowel was found,
if last_vowel_match:

	# Store the index of the last vowel.
	last_vowel_index = last_vowel_match.start()

print_verbose("last_vowel_index={}".format(last_vowel_index))


def get_excluded_letters_pattern(match):
	"""Get the excluded letters pattern."""

	# If the last vowel was given and the match occurs after the last vowel,
	if last_vowel_given and match.start() > last_vowel_index:

		return excluded_letters_vowels_pattern

	else:

		return excluded_letters_pattern


unknown_letter_pattern = "[.?]"

# Replace all unknown letters with the excluded letters pattern.
word_pattern = re.sub(unknown_letter_pattern, get_excluded_letters_pattern, word_pattern)


# Enclose the word pattern with anchors.
word_pattern = "^" + word_pattern + "$"

print_verbose("word_pattern={}".format(word_pattern))


#-------------------------------------------------------------------------------


letters_count = collections.Counter()

for word in re.findall(word_pattern, words, flags=re.MULTILINE):

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


#-------------------------------------------------------------------------------


if len(letters_count) > 0:

	# The letter count will be right justified to the width of the largest number.
	width = str(len(str(letters_count.most_common()[0][1])))


	letters_count_inverse = collections.defaultdict(list)

	# Invert the keys and values of the letters count.
	for (k, v) in letters_count.items():

		letters_count_inverse[v].append(k)

	print_verbose("letters_count_inverse={}".format(letters_count_inverse))


	for (k, v) in sorted(letters_count_inverse.items()):

		# Pad the key with spaces on the left so it is right justified.
		k_string = ("{:" + width + "}").format(k)

		# The letters are converted to uppercase and joined together.
		v_joined = " ".join(sorted([x.upper() for x in v]))

		print("{} = {}".format(k_string, v_joined))

