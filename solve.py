# SPDX-FileCopyrightText: Steven Ward
# SPDX-License-Identifier: OSL-3.0

import collections
import getopt
import os
import re
import sys


__author__ = 'Steven Ward'
__version__ = '2011-10-25'

program_name = os.path.basename(sys.argv[0])


def count_letters_duplicate(word):
	"""Count duplicate letters in a word."""
	return collections.Counter(word)

def count_letters_unique(word):
	"""Count unique letters in a word."""
	return collections.Counter(set(word))


# valid values
valid_count_letters_method = ['duplicate', 'unique']

# default values
default_verbose = False
default_show_command = False
default_last_vowel_given = True
default_count_letters_method = valid_count_letters_method[1]
default_words_file = 'words'

# mutable values
verbose = default_verbose
show_command = default_show_command
last_vowel_given = default_last_vowel_given
count_letters_method = default_count_letters_method
words_file = default_words_file


def print_help():
	"""Print the help message and exit."""

	print("""Usage: {} [OPTIONS] WORD-PATTERN [EXCLUDED-LETTERS]
Find possible words that match WORD-PATTERN for the game Hanging With Friends <http://www.hangingwithfriends.com/>.
#####
Find words that match WORD-PATTERN but do not have EXCLUDED-LETTERS.
#####

In WORD-PATTERN, use the dot ('.') or question mark ('?') to denote an unknown letter.

OPTIONS

-V, --version
    Print the version information and exit.

-h, --help
    Print this message and exit.

-v, --verbose
    Print diagnostics.
    (default: {})

--command
    Show the command to #####
    (default: {})

##### re-order these to be in alphabetical order

--last-vowel
    Indicate that the last vowel is given in WORD-PATTERN.  Use '--no-last-vowel' to indicate that the last vowel is not given in WORD-PATTERN.
    ##### Hanging With Friends has a rule about always showing the last vowel when presenting the initial word pattern to the user to solve.
    ##### all unknown letters after the last vowel need to have all vowels [aeiou] in the negative character class
    (default: {})

##### Count the letters that occur most often. in all the words.  All letters in a word contribute to the letter count.
##### Count the letters that occur in the most words.  Unique letters in a word contribute to the letter count.
-c, --count=METHOD #####
    Specify the method by which letters are counted in the words (word matches). #####
    If METHOD is "duplicate", count duplicate letters in a word.
    If METHOD is "unique", count unique letters in a word.
    (default: {})
    (valid: {})

-w, --words=FILE
    Use FILE as the words file.
    (default: {})""".format(
		program_name,
		default_verbose,
		default_show_command,
		default_last_vowel_given,
		default_count_letters_method,
		', '.join(valid_count_letters_method),
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


short_options = 'Vhvc:w:'
long_options = ['version', 'help', 'verbose', 'command', 'last-vowel', 'no-last-vowel', 'count=', 'words=']

try: [options, remaining_args] = getopt.getopt(sys.argv[1:], short_options, long_options)

except getopt.GetoptError as err: print_error(err)

for [option, value] in options:

	if   option in ['-V', '--version'] : print_version()
	elif option in ['-h', '--help'] : print_help()
	elif option in ['-v', '--verbose'] : verbose = True
	elif option in ['--command'] : show_command = True
	elif option in ['--last-vowel'] : last_vowel_given = True
	elif option in ['--no-last-vowel'] : last_vowel_given = False
	elif option in ['-c', '--count'] : count_letters_method = value
	elif option in ['-w', '--words'] : words_file = value
	else : print_error("Unhandled option '{}'.".format(option))


print_verbose("remaining_args={}".format(remaining_args))

if len(remaining_args) == 0:
	print_error("Must give at least 1 operand.")

if len(remaining_args) == 1:
	# The default value of the excluded letters is an empty string.
	remaining_args.append('')

# Validate the count letters method.

print_verbose("count_letters_method={}".format(count_letters_method))

if count_letters_method not in valid_count_letters_method:
	print_error("'{}' is not a valid count_letters_method.".format(count_letters_method))

# Assign the appropriate function to count_letters_func.

if count_letters_method == 'duplicate':
	count_letters_func = count_letters_duplicate
else:
	assert count_letters_method == 'unique'
	count_letters_func = count_letters_unique

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

# Validate the word pattern.

word_pattern = remaining_args[0].strip()
print_verbose("word_pattern={}".format(word_pattern))

# Convert the string to lowercase.
word_pattern = word_pattern.lower()
print_verbose("word_pattern={}".format(word_pattern))

# Remove characters not matching lowercase letters and unknown letters.
word_pattern = re.sub("[^a-z.?]", '', word_pattern)
print_verbose("word_pattern={}".format(word_pattern))

if len(word_pattern) == 0:
	print_error("Must give non-empty word pattern.")

# Validate the excluded letters.

excluded_letters = remaining_args[1].strip()
print_verbose("excluded_letters={}".format(excluded_letters))

# Convert the string to lowercase.
excluded_letters = excluded_letters.lower()
print_verbose("excluded_letters={}".format(excluded_letters))

# Remove characters not matching lowercase letters.
excluded_letters = re.sub("[^a-z]", '', excluded_letters)
print_verbose("excluded_letters={}".format(excluded_letters))

# Add letters in the word pattern to the excluded letters.
excluded_letters += re.sub("[^a-z]", '', word_pattern)
print_verbose("excluded_letters={}".format(excluded_letters))

# Remove duplicate letters and sort the letters.
excluded_letters = ''.join(sorted(set(excluded_letters)))
print_verbose("excluded_letters={}".format(excluded_letters))

# Add all the vowels to the excluded letters pattern.
# Remove duplicate letters and sort the letters.
excluded_letters_vowels = ''.join(sorted(set(excluded_letters + "aeiou")))
print_verbose("excluded_letters_vowels={}".format(excluded_letters_vowels))

# In multiline mode, the newline must be included in the negative character class.
excluded_letters_pattern = "[^" + excluded_letters + r"\n]"
print_verbose("excluded_letters_pattern={}".format(excluded_letters_pattern))

# In multiline mode, the newline must be included in the negative character class.
excluded_letters_vowels_pattern = "[^" + excluded_letters_vowels + r"\n]"
print_verbose("excluded_letters_vowels_pattern={}".format(excluded_letters_vowels_pattern))


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


letters_count = collections.Counter()

for word in re.findall(word_pattern, words, flags=re.MULTILINE):
	letters_count += count_letters_func(word)
	print(word)

print_verbose("letters_count={}".format(letters_count))


# Remove excluded letters from the letters count.
for excluded_letter in excluded_letters:
	if excluded_letter in letters_count:
		del letters_count[excluded_letter]

print_verbose("letters_count={}".format(letters_count))


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
		k_string = ('{:' + width + '}').format(k)

		# The letters are converted to uppercase and joined together.
		v_joined = ' '.join(sorted([x.upper() for x in v]))

		print('{} = {}'.format(k_string, v_joined))
