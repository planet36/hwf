#!/usr/bin/python3.2

# hanging with friends

#import collections

#import string
import re

import signal

#import sys


def signal_handler(signal_num, execution_frame):

	print()

	exit(0)


signal.signal(signal.SIGINT, signal_handler) # Interactive attention signal. (Ctrl-C)
signal.signal(signal.SIGTERM, signal_handler) # Termination request. (kill default signal)



dictionary_file_name = 'wwf.txt'


#program_name = sys.argv[0]


#if len(sys.argv) < 2:

#	exit("must give a string")


#s = sys.argv[1].strip()


#if len(s) == 0:

#	exit('must give a non-empty string')





#letters = string.replace(s, '.', '')


unknown_letter_pattern = re.compile('\.')

sed_command = r"sed --unbuffered --regexp-extended 's/([[:alpha:]])([[:alpha:]])/\1\n\2/g'"


while True:

	commands = []

	word_pattern = input('Enter word pattern: ').strip()

	if len(word_pattern) == 0:

		print("Must give non-empty word pattern.")

		continue

	excluded_letters = input('Enter excluded letters: ').strip()

	if len(excluded_letters) == 0:

		print("Must give non-empty excluded letters.")

		continue

	excluded_letters_character_class = '[^' + excluded_letters + ']'

	# Substitute unknown letters with the excluded letters character class.
	# re.sub(pattern, repl, string)
	commands.append("grep --perl-regexp '^" + re.sub(unknown_letter_pattern, excluded_letters_character_class, word_pattern) + "$' " + dictionary_file_name)
	commands.append(sed_command)
	commands.append(sed_command)
	commands.append("grep --perl-regexp '" + excluded_letters_character_class + "'")
	commands.append("sort")
	commands.append("uniq --count")
	commands.append("sort -g")

	print()
	print(' | '.join(commands))
	print()
