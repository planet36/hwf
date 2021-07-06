<?php
// SPDX-FileCopyrightText: Steven Ward
// SPDX-License-Identifier: OSL-3.0

$words_file = './words';

header('Content-Type: application/javascript');

header('Last-Modified: ' . gmdate(DateTime::RFC2822, filemtime($words_file)));

print("words = ");
print(json_encode(file_get_contents($words_file)));
print(";\n");

?>
