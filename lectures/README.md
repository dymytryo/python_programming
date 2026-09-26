# Lectures

Notebooks for teaching introductory Python, one per chapter of the course. Each is built to
be run in front of a class, in a strict alternation: one rule stated in a sentence or two,
then one cell small enough to run and change on the spot. Concepts arrive in dependency
order, and each notebook ends with a working program that uses only what came before it.
There are no quizzes here. Question banks and graded exercises live outside this folder.

| Notebook | Parts | Runnable cells | Ends with |
|---|---|---|---|
| [`02_elementary_programming.ipynb`](02_elementary_programming.ipynb) | 15 | 86 | A loan payment calculator and a distance calculator |

Part 2 of that notebook covers printing and expressions, numeric types, the seven
arithmetic operators and precedence; parts 3 to 6 cover variables, identifiers, strings
against numbers, `input`, and the four errors students hit first; parts 7 to 12 cover float
precision, rounding and formatting, `//` and `%`, assignment shortcuts, named constants,
scientific notation, overflow and underflow, and `time.time()`; part 13 covers the software
development process, IPO, and hand tracing.

## Running one in class

The notebooks ship unexecuted, with no stored output, so every result appears live as the
cell is run rather than sitting on the page ahead of the explanation.

Each numbered part is stored folded. In JupyterLab and Notebook 7, the caret to the left of
a heading opens and closes the part, and closing it folds the part's code cells away with
the prose, which keeps one topic on screen at a time. Other editors ignore the stored fold
state and open everything; the headings still fold by hand.

Nothing here needs a third-party package. The standard library modules used are `keyword`,
`sys`, `time`, and `math`. One cell in `02_elementary_programming.ipynb` calls `input()` and
waits for the keyboard, so run it live rather than as part of a Run All.
