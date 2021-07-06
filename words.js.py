# SPDX-FileCopyrightText: Steven Ward
# SPDX-License-Identifier: OSL-3.0

import json

words_file = './words'

with open(words_file, 'r') as f:
	print("words = {};".format(json.dumps(f.read())));
