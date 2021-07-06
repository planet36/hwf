
README:
  These Python and javascript programs assist playing the game Hanging With Friends <http://www.hangingwithfriends.com/>.
  #####


AUTHORS:
- Steven Ward


CONTENTS:
- COPYING.txt: license
- README.txt: this file
- create.html: create a word
- create.py: create a word
- solve.html: solve a word
- solve.py: solve a word
- style.css: style sheet
- utils.javascript: javascript utilities
- word-value.py: get the word value
- words: the list of words
- words.js.php: create the list of words as a javascript string
- words.js.py: create the list of words as a javascript string


DEPENDENCIES:
- Python3
- HTML5 browser with javascript enabled


EXAMPLES:

  CREATE:

    ./create.py riurqjeidwlp

    ./create.py riurqjeidwlp | ./word-value.py | sort -g

    ./create.py riurqjeidwlp | ./word-value.py .....dl | sort -g

  SOLVE:

    ./solve.py ....a..
    ./solve.py .e..a..
    ./solve.py .e..a.. s
    ./solve.py .e..a.. sr
    ./solve.py .e..a.t sr
    ./solve.py .en.ant sr

    "pendant" is the answer

