# Lectures

Notebooks for teaching introductory Python, one per chapter of the course. Rules are stated
in a sentence or two, and code is kept small enough to run and change on the spot. Chapter 4
uses strict pairs: one explanation cell followed by one single-line code cell, so each result
appears directly beneath the explanation for that line. Concepts arrive in dependency order,
and each notebook ends with a working program that uses only what came before it. There are
no quizzes.

| Notebook | Parts | Code cells | Ends with |
|---|---|---|---|
| [`02_elementary_programming.ipynb`](02_elementary_programming.ipynb) | 15 | 84 | A loan payment calculator and a distance calculator |
| [`03_selection_statements.ipynb`](03_selection_statements.ipynb) | 6 | 76 | Common selection errors |
| [`04_math_functions_characters_strings.ipynb`](04_math_functions_characters_strings.ipynb) | 9 | 162 | A course-section report |

Chapter 2 covers `print`, comments, numeric types, arithmetic, variables, strings, `input`,
errors, float precision, formatting, integer division, assignment, constants, scientific
notation, time, and the path from a requirement to a program.

Chapter 3 covers Boolean values, comparisons, random numbers, every `if` form, nested
selection, logical operators, precedence, short-circuit evaluation, range and boundary
tests, conditional expressions, `match`/`case`, and common selection errors.

Chapter 4 covers built-in numeric functions, the `math` module, Unicode characters, string
literals and escape sequences, printing controls, string operators and comparisons, indexes,
slices, string methods, output formatting, and f-strings.

The notebooks ship unexecuted and with no stored output, so every result appears live as the
cell is run. Each numbered part is stored folded through the `jp-MarkdownHeadingCollapsed`
cell metadata, which JupyterLab 4 and Notebook 7 honour; other editors open everything.

Nothing needs a third-party package. The standard library modules used are `keyword`, `sys`,
`time`, `math`, and `random`. One cell calls `input()` and waits for the keyboard, so run it
on its own rather than as part of a Run All.
