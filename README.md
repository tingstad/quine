# quine
Self-replicating program

A simple [quine](https://en.wikipedia.org/wiki/Quine_(computing)) where I did not want to use `printf %s`. The trick was to get the quoting right on the "recursion line", [#14](https://github.com/tingstad/quine/blob/7b65d19f5f9834433b14cd13a540b89acd9d44e7/quine.sh#L14) (which has to match #9), I found the solution [here](http://c2.com/wiki/remodel/?QuineProgram).
