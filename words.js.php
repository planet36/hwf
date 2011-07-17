<?php

/*
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
*/


$words_file = './words';

header('Content-Type: application/javascript');

header('Last-Modified: ' . gmdate(DateTime::RFC2822, filemtime($words_file)));

print("words = ");
print(json_encode(file_get_contents($words_file)));
print(";\n");

?>
