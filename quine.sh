#!/bin/sh
# https://github.com/tingstad/quine

b='\'
s=\'
top='#!/bin/sh
# https://github.com/tingstad/quine
'
src='
echo "$top
b=$s$b$s
s=$b$s
top=$s$top$s
src=$s$src$s
$src"
'

echo "$top
b=$s$b$s
s=$b$s
top=$s$top$s
src=$s$src$s
$src"

