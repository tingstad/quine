#!/bin/sh
# https://github.com/tingstad/quine

b(){ printf '\134'; }
s(){ printf '\047'; }
n(){ printf '\012'; }

src(){
printf '
printf "#!/bin/sh
# https://github.com/tingstad/quine

b(){ printf "; s; b; printf "134"; s; printf "; }
s(){ printf "; s; b; printf "047"; s; printf "; }
n(){ printf "; s; b; printf "012"; s; printf "; }

src(){
printf "
s
src
s
n
printf "}"
n
src
'
}

printf "#!/bin/sh
# https://github.com/tingstad/quine

b(){ printf "; s; b; printf "134"; s; printf "; }
s(){ printf "; s; b; printf "047"; s; printf "; }
n(){ printf "; s; b; printf "012"; s; printf "; }

src(){
printf "
s
src
s
n
printf "}"
n
src
