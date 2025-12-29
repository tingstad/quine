# Quine

A “quine” is a _self-replicating program_ — its output is a copy of its own source code.

Here is an example I wrote in Python:

```python

c = """
c = {1}{0}{1}
print(c.format(c, '"'*3))
"""
print(c.format(c, '"'*3))

```

### Shell quine

<details>
<summary>Shell script quines without "%s"</summary>

This shell script prints an exact copy of itself. This means that `cat quine.sh` and `./quine.sh` are equivalent:

https://github.com/tingstad/quine/blob/f1a460d9660cc9f5b26a784e3415afe700750a47/quine.sh#L1-L23

It's therefore also equivalent to running e.g. `sh <(sh <(./quine.sh))`.

I did not want to use `printf %s` for this quine. The trick was to get the quoting right on the "recursion line", [#14](https://github.com/tingstad/quine/blob/7b65d19f5f9834433b14cd13a540b89acd9d44e7/quine.sh#L14) (which has to match #9), I found the solution [here](http://c2.com/wiki/remodel/?QuineProgram).

In [quine2.sh](https://github.com/tingstad/quine/blob/main/quine2.sh) I wanted to avoid variable assignments and minimize string interpretation (no `%` and `$`) and just use simple `printf` and zero-argument functions/procedures.

</details>

### PDF quine

I was curious if it was possible — it took many hours and a few hundred lines, but I present:

[quine.pdf](quine.pdf)
