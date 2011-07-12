
README:
  These Python scripts assist playing the game Hanging With Friends.
  #####


AUTHORS:
- Steve Ward


CONTENTS:
- COPYING.txt: license
- create.py: create a word
- README.txt: this file
- solve.py: solve a word
- word-value.py: get the word value
- words: the list of words


DEPENDENCIES:
- Python3


COPYING/LICENSE: |

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


EXAMPLES:

  CREATE:

    ./create.py riurqjeidwlp

    ./create.py riurqjeidwlp | ./word-value.py | sort -g

  SOLVE:

    ./solve.py ....a..
    ./solve.py .e..a..
    ./solve.py .e..a.. s
    ./solve.py .e..a.. sr
    ./solve.py .e..a.t sr
    ./solve.py .en.ant sr

    "pendant" is the answer

