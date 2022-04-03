#!/bin/sh

main(){
    codepage3=$(objectsencoded 16 21 | wordwrap)
    codepage4=$((objectsencoded 22 22 && objectsencoded 29 40)| wordwrap)
    codepage5=$((objectsencoded 41 48)| wordwrap)
    codepage5b=$((objectsencoded 50 53)| wordwrap)
    inplace quine.pdf sed -E '/^%BEGIN 16-/,/^%END 16-/{
        /^%/!d
        /^%END 16-/{
            i\
'"$(printf "$codepage3" | sed 's/$/\\/')"'

        }
    }
    /^%BEGIN PAGE 4/,/^%END PAGE 4/{
        /^%/!d
        /^%END PAGE 4/{
            i\
'"$(printf "$codepage4" | sed 's/$/\\/')"'

        }
    }
    /^%BEGIN PAGE 5a/,/^%END PAGE 5a/{
        /^%/!d
        /^%END PAGE 5a/{
            i\
'"$(printf "$codepage5" | sed 's/$/\\/')"'

        }
    }
    /^%BEGIN PAGE 5b/,/^%END PAGE 5b/{
        /^%/!d
        /^%END PAGE 5b/{
            i\
'"$(printf "$codepage5b" | sed 's/$/\\/')"'

        }
    }' quine.pdf
}

objectsencoded()( from=$1; to=$2
    for objnum in $(seq $from $to) ; do
        objencoded $objnum
    done
)

objencoded()( nobjum=$1
    src=$(objdef $objnum)
    printf '%s\n' "$src" | sed -E "
    /^[0-9]+ 0 /{
      s/^([0-9])([0-9]) 0 obj/3\1 0 R  2 0 R  3\2 0 R  2 0 R 0 obj/
      s/^([0-9]) 0 obj/3\1 0 R  2 0 R 0 obj/
      s/ 0 obj << \/Length ([0-9])([0-9])/  6 0 R  2 0 R  3\1 0 R  2 0 R  3\2 0 R  2 0 R/
      s/ 0 obj << \/Length ([0-9])/  6 0 R  2 0 R  3\1 0 R  2 0 R/
      s/ >> stream/  7 0 R  4 0 R/
    }
    s/^\(.*/  8 0 R  2 0 R  $objnum 0 R  2 0 R  9 0 R  4 0 R/
    s/^endstream endobj/  10 0 R  4 0 R/
    "
)

objdef()( num=$1
    sed -n '/^'$num' 0 obj << /,/^endstream endobj$/p' quine.pdf
)

wordwrap(){
    sed -En 'H;${
        g
        s/\n/ /g
        s/^ //
        :loop
        s/  / /g
        t loop
        p
    }' | tr -d \\n | awk -v max=65 '{
        s = $0
        while (length(s) > max) {
            # R  9 0 R  52 O R
            #        ^-------^ max: 8
            i = index(substr(s, max-8), "R")
            print(substr(s, 1, i+max-8))
            s = substr(s, i+max-8)
            sub(/^ +/, "", s)
        }
        print s
    }'
}

inplace() { 
    ( file="$1";
    shift;
    temp=$(mktemp);
    "$@" < "$file" > "$temp" && mv "$temp" "$file" )
}

[ $# -eq 0 ] && main || "$@"

