# Lectures

Notebooks for teaching introductory Python, one per chapter of the course. Each one is
built to be run in front of a class: concepts in order of dependency, a runnable cell
after every idea, and a working program at the end that uses only what came before it.
There are no quizzes here. Question banks and graded exercises live outside this folder.

| Notebook | Covers | Ends with |
|---|---|---|
| [`02_elementary_programming.ipynb`](02_elementary_programming.ipynb) | Printing and expressions, numeric types, the seven arithmetic operators, precedence, variables and identifiers, strings against numbers, `input`, the four common errors, float precision, rounding and formatting, `//` and `%`, augmented and simultaneous assignment, named constants, scientific notation, overflow and underflow, `time.time()`, the software development process and IPO | A loan payment calculator and a distance calculator |

Every cell is executed and its output committed, so the notebook reads correctly on
GitHub without being run. One cell in `02_elementary_programming.ipynb` calls `input()`
and is deliberately left unexecuted, to be run live.

Nothing here needs a third-party package. The standard library modules used are
`keyword`, `sys`, `time`, and `math`.
