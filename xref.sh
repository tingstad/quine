#!/bin/sh
set -e

if ! [ -e "$1" ]; then
    echo "Usage: $0 FILE"; exit 1
fi

file="$1"

count=$(grep '^[0-9][0-9]* 0 obj ' "$file" | wc -l)

printf 'xref\n'\
'0 %d\n'\
'0000000000 65535 f \n' $((count + 1))

for i in $(seq 1 $count); do
    offs=$(grep --byte-offset --only-matching --text "^$i 0 obj" "$file" | cut -d: -f1)
    printf "%010d 00000 n \n" $offs
done
start=$(grep --byte-offset --only-matching --text '^xref' "$file" | cut -d: -f1)
# sed '/^xref/,$d' "$file" | wc -c

printf 'trailer << /Root 1 0 R /Size %d >>\n'\
'startxref\n'\
'%d\n'\
'%%%%EOF\n' $((count + 1)) $start

