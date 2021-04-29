# quine
Self-replicating program

This shell [quine](https://en.wikipedia.org/wiki/Quine_(computing)) prints an exact copy of itself. This means that `cat quine.sh` and `./quine.sh` are equivalent:

```shell
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

```

It's therefore also equivalent to running `sh <(sh <(./quine.sh))` or `./quine.sh > 1 ; sh 1 > 2 ; sh 2`.

I did not want to use `printf %s` for this quine. The trick was to get the quoting right on the "recursion line", [#14](https://github.com/tingstad/quine/blob/7b65d19f5f9834433b14cd13a540b89acd9d44e7/quine.sh#L14) (which has to match #9), I found the solution [here](http://c2.com/wiki/remodel/?QuineProgram).

In [quine2.sh](https://github.com/tingstad/quine/blob/main/quine2.sh) I wanted to avoid variable assignments and minimize string interpretation (no `%` and `$`) and just use simple `printf` and subroutines (parameter less functions).

