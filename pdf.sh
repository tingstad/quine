#!/bin/sh

main(){
    inplace quine.pdf sed -E '/^%BEGIN 16-/,/^%END 16-/{
        /^%/!d
        /^%END 16-/{
            i\
'"$(objectsencoded 16 21 | wordwrap | sed 's/$/\\/')"'

        }
    }
    /^%BEGIN PAGE 4/,/^%END PAGE 4/{
        /^%/!d
        /^%END PAGE 4/{
            i\
'"$((objectsencoded 22 22 && objectsencoded 29 40)| wordwrap | sed 's/$/\\/')"'

        }
    }
    /^%BEGIN PAGE 5a/,/^%END PAGE 5a/{
        /^%/!d
        /^%END PAGE 5a/{
            i\
'"$(objectsencoded 41 48 | wordwrap | sed 's/$/\\/')"'

        }
    }
    /^%BEGIN PAGE 5b/,/^%END PAGE 5b/{
        /^%/!d
        /^%END PAGE 5b/{
            i\
'"$(objectsencoded 50 53 | wordwrap | sed 's/$/\\/')"'

        }
    }
    /^%BEGIN PAGE 6/,/^%END PAGE 6/{
        /^%/!d
        /^%END PAGE 6/{
            i\
'"$(objectsencoded 54 66 | wordwrap | sed 's/$/\\/')"'

        }
    }
    /^%BEGIN PAGE 7/,/^%END PAGE 7/{
        /^%/!d
        /^%END PAGE 7/{
            i\
'"$(objectsencoded 67 78 | wordwrap | sed 's/$/\\/')"'

        }
    }' quine.pdf

    inplace quine.pdf sed -E '/^%START PAGE 8/,/^%FINISH PAGE/{
        /^%/!d
        /^%FINISH PAGE/{
            i\
'"$(declareobjs 79 | sed 's/$/\\/')"'

        }
    }' quine.pdf

    inplace quine.pdf sed -E \
    '/^%BEGIN PAGE 8/,/^%END PAGE 8/{
        /^%/!d
        /^%END PAGE 8/{
            i\
'"$(objectsencoded 95 107 | wordwrap | sed 's/$/\\/')"'

        }
    }' quine.pdf
}

objectsencoded()( from=$1; to=$2
    for objnum in $(seq $from $to) ; do
        objencoded $objnum "$(objdef $objnum)"
    done
)

objencoded()( objnum=$1 src="$2"
    printf '%s\n' "$src" | sed -E "
    /^[0-9]+ 0 /{
      s/^([0-9])([0-9])([0-9]) 0 obj/3\1 0 R  2 0 R  3\2 0 R  2 0 R  3\3 0 R  2 0 R 0 obj/
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

declareobjs()( num=$1
    i=94
    while read -r line; do
        len=${#line}
        if [ $len -lt 1 ]; then continue; fi
        case "$line" in
            %*) continue ;;
        esac
        printf '%d 0 obj << /Length %d >> stream\n(%s)\nendstream endobj\n' $((i+=1)) $((len+2)) "$line"
    done <<EOF
    $(sed -n '/^'$num' 0 obj << /,/] >> endobj$/p' quine.pdf)
EOF
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
            # R  9 0 R  152 O R
            #        ^--------^ max: 9
            i = index(substr(s, max-9), "R")
            print(substr(s, 1, i+max-9))
            s = substr(s, i+max-9)
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

