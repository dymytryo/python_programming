# Lectures

Notebooks for teaching introductory Python, one per chapter of the course. Each is a strict
alternation: one rule stated in a sentence or two, then one cell small enough to run and
change on the spot. Concepts arrive in dependency order, and each notebook ends with a
working program that uses only what came before it. There are no quizzes.

| Notebook | Parts | Runnable cells | Ends with |
|---|---|---|---|
| [`02_elementary_programming.ipynb`](02_elementary_programming.ipynb) | 15 | 84 | A loan payment calculator and a distance calculator |

Parts 1 and 2 cover `print` and comments, numeric types, the seven arithmetic operators and
precedence. Parts 3 to 6 cover variables, identifiers, strings against numbers, `input`, and
the four errors students hit first. Parts 7 to 12 cover float precision, rounding and
formatting, `//` and `%`, assignment shortcuts, named constants, scientific notation,
overflow and underflow, and `time.time()`. Part 13 covers the software development process,
IPO, and hand tracing. Parts 14 and 15 are the two programs.

The notebooks ship unexecuted and with no stored output, so every result appears live as the
cell is run. Each numbered part is stored folded through the `jp-MarkdownHeadingCollapsed`
cell metadata, which JupyterLab 4 and Notebook 7 honour; other editors open everything.

Nothing needs a third-party package. The standard library modules used are `keyword`, `sys`,
`time`, and `math`. One cell calls `input()` and waits for the keyboard, so run it on its own
rather than as part of a Run All.
