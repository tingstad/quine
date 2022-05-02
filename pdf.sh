#!/bin/sh

main(){
    inplace quine.pdf sed -E '/^%BEGIN 16-/,/^%END 16-/{
        /^%/!d
        /^%END 16-/{
            i\
'"$(objectsencoded 16-21 | wordwrap | sed 's/$/\\/')"'

        }
    }
    /^%BEGIN PAGE 4/,/^%END PAGE 4/{
        /^%/!d
        /^%END PAGE 4/{
            i\
'"$((objectsencoded 22 29-40)| wordwrap | sed 's/$/\\/')"'

        }
    }
    /^%BEGIN PAGE 5a/,/^%END PAGE 5a/{
        /^%/!d
        /^%END PAGE 5a/{
            i\
'"$(objectsencoded 41-48 | wordwrap | sed 's/$/\\/')"'

        }
    }
    /^%BEGIN PAGE 5b/,/^%END PAGE 5b/{
        /^%/!d
        /^%END PAGE 5b/{
            i\
'"$(objectsencoded 50-53 | wordwrap | sed 's/$/\\/')"'

        }
    }
    /^%BEGIN PAGE 6/,/^%END PAGE 6/{
        /^%/!d
        /^%END PAGE 6/{
            i\
'"$(objectsencoded 54-66 | wordwrap | sed 's/$/\\/')"'

        }
    }
    /^%BEGIN PAGE 7/,/^%END PAGE 7/{
        /^%/!d
        /^%END PAGE 7/{
            i\
'"$(objectsencoded 67-78 | wordwrap | sed 's/$/\\/')"'

        }
    }' quine.pdf

    inplace quine.pdf sed -E '/^%START PAGE 8/,/^%FINISH PAGE/{
        /^%/!d
    }' quine.pdf
    inplace quine.pdf sed -E '/^%START PAGE 8/,/^%FINISH PAGE/{
        /^%FINISH PAGE/{
            i\
'"$(declareobjs 79 95 | sed 's/$/\\/')"'

        }
    }' quine.pdf

    inplace quine.pdf sed -E \
    '/^%BEGIN PAGE 8/,/^%END PAGE 8/{
        /^%/!d
        /^%END PAGE 8/{
            i\
'"$(objectsencoded 95-107 | wordwrap | sed 's/$/\\/')"'

        }
    }' quine.pdf

    inplace quine.pdf sed -E \
    '/^%BEGIN PAGE 9/,/^%END PAGE 9/{
        /^%/!d
        /^%END PAGE 9/{
            i\
'"$(objectsencoded 108-120 | wordwrap | sed 's/$/\\/')"'

        }
    }' quine.pdf

    inplace quine.pdf sed -E \
    '/^%BEGIN PAGE 010/,/^%END PAGE 010/{
        /^%/!d
        /^%END PAGE 010/{
            i\
'"$(objectsencoded 121-132 | wordwrap | sed 's/$/\\/')"'

        }
    }' quine.pdf

    inplace quine.pdf sed -E \
    '/^%BEGIN PAGE 011/,/^%END PAGE 011/{
        /^%/!d
        /^%END PAGE 011/{
            i\
'"$(printpageobj 79 | sed 's/$/\\/')"'

        }
    }' quine.pdf

    inplace quine.pdf sed -E '/^%START PAGE 012/,/^%FINISH PAGE/{
        /^%/!d
    }' quine.pdf
    inplace quine.pdf sed -E '/^%START PAGE 012/,/^%FINISH PAGE/{
        /^%FINISH PAGE/{
            i\
'"$(declareobjs 24 136 | sed 's/$/\\/')"'

        }
    }' quine.pdf

    inplace quine.pdf sed -E \
    '/^%BEGIN PAGE 012/,/^%END PAGE 012/{
        /^%/!d
        /^%END PAGE 012/{
            i\
'"$(objectsencoded 136-148 | wordwrap | sed 's/ *$/\\/')"'

        }
    }' quine.pdf

    createpageobj 163

    inplace quine.pdf sed '/^xref/,/^%EOF/d'
    ./xref.sh quine.pdf >> quine.pdf
}

createpageobj() ( num=$1
    inplace quine.pdf sed -E \
    '/^%BEGIN PAGEOBJ '$num'/,/^%END PAGEOBJ '$num'/{
        /^%/!d
        /^%END PAGEOBJ/{
            i\
'$num' 0 obj << /Type /Page  /Parent 12 0 R  /Resources << /Font <<\
/F1 <</Type /Font  /Subtype /Type1  /BaseFont /Courier>> >> >>\
/Contents [ 15 0 R\
'"$(objectsencoded 149-161 | wordwrap | sed 's/ *$/\\/')"'
11 0 R ] >> endobj\

        }
    }' quine.pdf
)

objectsencoded()(
    for arg; do
        case $arg in
            *-*)
                from=${arg%-*}; to=${arg#*-}
                for objnum in $(seq $from $to) ; do
                    objencoded $objnum "$(objdef $objnum)"
                done
            ;;
            *)
                objnum=$arg
                objencoded $objnum "$(objdef $objnum)"
            ;;
        esac
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

declareobjs()( num=$1; i=$2
    while read -r line; do
        len=${#line}
        if [ $len -lt 1 ]; then continue; fi
        case "$line" in
            %*) continue ;;
        esac
        decl=$(printf '%d 0 obj << /Length %d >> stream\n(%s)\nendstream endobj\n' $i $((len+2)) "$line")
        if ! printf %s "$decl" | tail -n 2 | exists quine.pdf; then
            echo "$decl"
            i=$((i+1))
        fi
    done <<-EOF
	$(sed -n '/^'$num' 0 obj << /,/] >> endobj$/p' quine.pdf)
EOF
)

printpageobj()( num=$1
    while read -r line; do
        len=${#line}
        if [ $len -lt 1 ]; then continue; fi
        case "$line" in
            %*) continue ;;
        esac
        line=$(printf %s "$line" | sed 's/\[/\\[/g')
        contentline=$(grep -m 1 -n "^($line" quine.pdf | awk -F: '{print $1}')
        objno=$(awk "NR == $((contentline - 1)) { print \$1 }" quine.pdf)
        printf '%s 0 R 4 0 R ' $objno
    done <<-EOF | wordwrap
	$(sed -n '/^'$num' 0 obj << /,/] >> endobj$/p' quine.pdf)
EOF
)

exists() (
    #sed -n '1h;2,$H;${g;s/\n/\\n/g;p;}'
    i=0
    line=''
    a=''
    while read -r line || [ -n "$line" ]; do
        a="$a
            line[$((i+=1))] = \"$line\""
    done
    awk '
        BEGIN {
            '"$a"'
            c = 1
        }
        {
            if ($0 == line[c]) {
                c++
                if (c > length(line))
                    exit 0
            } else
                c = 1
        }
        END {
            exit (c > length(line)) ? 0 : 1
        }
    ' "$1"
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

test() {
    echo Test
    decl='17 0 obj << /Length 64 >> stream
(/F1 <</Type /Font  /Subtype /Type1  /BaseFont /Courier>> >> >>)
endstream endobj'
    if ! printf %s "$decl" | exists quine.pdf; then
        echo >&2 'Expected to find string in file'
        exit 1
    else
        echo OK
    fi
    decl="$decl FOOO"
    if printf %s "$decl" | exists quine.pdf; then
        echo >&2 'Expected not to find in file'
        exit 1
    else
        echo OK
    fi
}

[ $# -eq 0 ] && main || "$@"

