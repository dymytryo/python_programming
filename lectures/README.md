# Lectures

Notebooks for teaching introductory Python, one per chapter of the course. Each is a strict
alternation: one rule stated in a sentence or two, then one cell small enough to run and
change on the spot. Concepts arrive in dependency order, and each notebook ends with a
working program that uses only what came before it. There are no quizzes.

| Notebook | Parts | Runnable cells | Ends with |
|---|---|---|---|
| [`02_elementary_programming.ipynb`](02_elementary_programming.ipynb) | 15 | 84 | A loan payment calculator and a distance calculator |
| [`03_selection_statements.ipynb`](03_selection_statements.ipynb) | 16 | 85 | A BMI category program and a point-location program |

Chapter 2 covers `print`, comments, numeric types, arithmetic, variables, strings, `input`,
errors, float precision, formatting, integer division, assignment, constants, scientific
notation, time, and the path from a requirement to a program.

Chapter 3 covers Boolean values, comparisons, random numbers, every `if` form, nested
selection, logical operators, precedence, short-circuit evaluation, range and location
tests, conditional expressions, `match`/`case`, and common selection errors.

The notebooks ship unexecuted and with no stored output, so every result appears live as the
cell is run. Each numbered part is stored folded through the `jp-MarkdownHeadingCollapsed`
cell metadata, which JupyterLab 4 and Notebook 7 honour; other editors open everything.

Nothing needs a third-party package. The standard library modules used are `keyword`, `sys`,
`time`, `math`, and `random`. One cell calls `input()` and waits for the keyboard, so run it
on its own rather than as part of a Run All.
