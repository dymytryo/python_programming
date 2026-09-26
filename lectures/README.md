# Lectures

Notebooks for teaching introductory Python, one per chapter of the course. Each one is
built to be run in front of a class: concepts in order of dependency, a runnable cell
after every idea, and a working program at the end that uses only what came before it.
There are no quizzes here. Question banks and graded exercises live outside this folder.

| Notebook | Covers | Ends with |
|---|---|---|
| [`02_elementary_programming.ipynb`](02_elementary_programming.ipynb) | Printing and expressions, numeric types, the seven arithmetic operators, precedence, variables and identifiers, strings against numbers, `input`, the four common errors, float precision, rounding and formatting, `//` and `%`, augmented and simultaneous assignment, named constants, scientific notation, overflow and underflow, `time.time()`, the software development process and IPO | A loan payment calculator and a distance calculator |

## Running one in class

The notebooks ship unexecuted, with no stored output, so every result appears live as you
run the cell rather than sitting on the page ahead of the explanation. Read the section,
then run its cells.

Each numbered section is stored folded. In JupyterLab and Notebook 7, the caret to the
left of a heading opens and closes the section, and closing it folds the section's code
cells away with the prose, which keeps one topic on screen at a time. Other editors
ignore the stored fold state and open everything; the headings still fold by hand.

Nothing here needs a third-party package. The standard library modules used are
`keyword`, `sys`, `time`, and `math`. One cell in `02_elementary_programming.ipynb` calls
`input()` and waits for the keyboard, so run it live rather than as part of a Run All.
