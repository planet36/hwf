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


import signal
import sys


def signal_handler(signal_num, execution_frame):

	print()

	exit(0)


signal.signal(signal.SIGINT, signal_handler) # Interactive attention signal. (Ctrl-C)
signal.signal(signal.SIGTERM, signal_handler) # Termination request. (kill default signal)


# These are the values of the letters in some word games.
letter_values = {
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


def get_word_value(word):
	"""Get the value of the word."""

	return sum([letter_values.get(letter.upper(), 0) for letter in word])


for line in sys.stdin:

	line = line.strip()

	if len(line) == 0:

		continue

	print("{}\t{}".format(get_word_value(line), line))
