# Software development with Python

Software development with Python combines the language, standard library, project
structure, dependency management, tests, observability, and distribution tools needed
to turn source code into maintainable software. Python syntax is only one layer. A
working application also needs predictable resource cleanup, explicit errors,
repeatable environments, documented interfaces, and a controlled delivery process.

Core Python is the default in this guide. IPython and Jupyter features, pandas
operations, command-line tools, and third-party packages are labeled where they
appear.

```text
source code
    |
    v
isolated environment + declared dependencies
    |
    v
format and static checks -> automated tests
    |
    v
build an application or distribution package
    |
    v
run or publish -> logs, errors, timing, and profiling
```

| Concern | What it controls |
|---|---|
| Resource safety | Files, locks, connections, and processes are released even when work fails. |
| Interfaces | Functions, classes, modules, and application programming interfaces expose clear contracts. |
| Correctness | Exceptions, type annotations, tests, and static checks catch failures close to their source. |
| Reproducibility | Environments and dependency declarations make execution repeatable. |
| Observability | Logging, tracebacks, timing, and profiling explain runtime behavior. |
| Distribution | Build metadata and artifacts let other environments install the software. |

## Contents

- [Development vocabulary and flow](#development-vocabulary-and-flow)
- [Functions, documentation, and typing](#functions-documentation-and-typing)
- [Context managers and resource cleanup](#context-managers-and-resource-cleanup)
- [Exceptions and tracebacks](#exceptions-and-tracebacks)
- [Paths, files, text, and binary data](#paths-files-text-and-binary-data)
- [Collections, iteration, and core expressions](#collections-iteration-and-core-expressions)
- [Functions as objects and decorators](#functions-as-objects-and-decorators)
- [Object-oriented design](#object-oriented-design)
- [Modules, imports, and executable packages](#modules-imports-and-executable-packages)
- [Standard-library runtime tools](#standard-library-runtime-tools)
- [Environments and dependency installation](#environments-and-dependency-installation)
- [Packaging and distribution](#packaging-and-distribution)
- [Testing and code quality](#testing-and-code-quality)
- [Timing, profiling, and memory inspection](#timing-profiling-and-memory-inspection)
- [Data processing with pandas](#data-processing-with-pandas)
- [Web APIs and application configuration](#web-apis-and-application-configuration)

## Development vocabulary and flow

Python uses related terms for source code and installable software. Keeping them
separate makes imports, builds, and command execution easier to reason about.

| Term | Meaning |
|---|---|
| Script | A Python file intended to be executed, such as `python report.py`. |
| Module | A single importable Python file, such as `report.py`. |
| Package | An importable directory of modules and subpackages. Most regular packages contain `__init__.py`; namespace packages can omit it. |
| Subpackage | A package contained inside another package. |
| Library | A general term for reusable code. A library can contain one or more packages. |
| Distribution package | The installable project delivered as a source distribution or wheel. Its project name does not have to equal its import-package name. |
| Application | Software run for its behavior, such as a command-line tool, web service, or data pipeline. |

A Python Enhancement Proposal (PEP) proposes or documents language, process, or
ecosystem standards. PEP 8 describes Python code style. PEP numbers identify distinct
documents, so `PEP` by itself does not mean the style guide.

Python also includes its design aphorisms in the interpreter:

```python
import this
```

The output is known as the Zen of Python. It is guidance, not an executable standard.

### A practical development loop

1. Select an interpreter and create an isolated environment.
2. Declare runtime and development dependencies.
3. Write small functions and explicit public interfaces.
4. Format, lint, type-check where useful, and run tests.
5. Run the program from the same entry point used in production.
6. Inspect logs, exceptions, timing, and memory before optimizing.
7. Build a distribution only when the code needs to be installed elsewhere.

Refactoring improves internal structure without intentionally changing external
behavior. Small, verified changes reduce the chance that cleanup work introduces a
new defect.

## Functions, documentation, and typing

A function is a named unit of behavior. A focused function is easier to test, reuse,
and replace. The Single Responsibility Principle (SRP) applies the same idea at a
larger design level: a function or class should have one cohesive reason to change.

```python
def standardize(column):
    """Return the values in a pandas Series as z-scores."""
    return (column - column.mean()) / column.std()
```

```python
df["year_1_z"] = standardize(df["year_1_gpa"])
df["year_2_z"] = standardize(df["year_2_gpa"])
df["year_3_z"] = standardize(df["year_3_gpa"])
df["year_4_z"] = standardize(df["year_4_gpa"])
```

The function performs one transformation. The calling code decides which columns to
transform and where to store them.

### Docstrings

A docstring is the first string literal in a module, class, or function. It becomes
runtime documentation through the object's `__doc__` attribute. A consistent style,
such as NumPy-style docstrings, makes generated documentation predictable.

`numpydoc` is the documentation convention and Sphinx extension associated with the
NumPy-style structure used below.

```python
def validate_age(age: int) -> int:
    """Validate and return an age.

    Parameters
    ----------
    age
        Age in whole years.

    Returns
    -------
    int
        The validated age.

    Raises
    ------
    ValueError
        If age is outside the accepted range.
    """
    if not 0 <= age <= 100:
        raise ValueError("age must be between 0 and 100")

    return age
```

Inspect documentation and attributes interactively:

```python
import inspect

print(validate_age.__doc__)
print(inspect.getdoc(validate_age))
help(validate_age)
dir(validate_age)
```

`inspect.getdoc()` cleans indentation. `help()` formats documentation for a reader.
`dir()` lists available names but does not distinguish the stable public interface
from implementation details.

`pyment` can generate or convert docstring formats, but generated text still needs
review. Public modules, functions, classes, and methods should explain their contract,
not repeat their names.

### Type annotations

Type annotations document intended values and support static analysis. Python does not
normally enforce them at runtime.

```python
from collections.abc import Iterable
from typing import Any, TypeAlias

Vector: TypeAlias = list[float]


def scale(values: Iterable[float], factor: float) -> Vector:
    return [value * factor for value in values]


def emit(value: Any, verbose: bool | None = None) -> None:
    if verbose:
        print(value)
```

Modern annotations use built-in generics such as `list[int]`, `dict[str, str]`, and
`set[str]`. `Any` disables useful checking at that point, so use it only when the value
is genuinely unrestricted. Tools such as mypy analyze annotations without executing
the program.

Older code commonly uses `typing.List`, `typing.Dict`, `typing.Set`, and
`typing.Optional`. `Optional[bool]` means `bool | None`; it does not merely mean that
callers may omit an argument. Built-in generics and union syntax are clearer for code
that supports them.

### Default arguments and mutability

Default values are evaluated once when Python defines the function. A mutable default
therefore persists across calls. Use an immutable sentinel such as `None` and create
the object inside the function.

```python
import pandas as pd


def add_column(values, frame=None):
    """Return a DataFrame with values added as the next numbered column."""
    if frame is None:
        frame = pd.DataFrame()

    result = frame.copy()
    result[f"col_{len(result.columns)}"] = values
    return result
```

Copying the supplied DataFrame also makes the mutation policy explicit: this function
returns a new object instead of modifying its caller's object in place.

## Context managers and resource cleanup

A context manager defines setup and teardown around a block of code. It implements the
context-management protocol through `__enter__()` and `__exit__()`. After
`__enter__()` succeeds, the `with` statement guarantees that exit handling runs when
the block completes, including when the block raises an exception. `__exit__()` is not
called when `__enter__()` itself raises.

```text
call context manager
        |
        v
__enter__() -> bind value after "as"
        |
        v
run the with block
        |
        v
__exit__(exception details) -> release or restore the resource
```

Files already implement the protocol:

```python
with open("example.txt", "r", encoding="utf-8") as input_file:
    content = input_file.read()

print(input_file.closed)
```

```text
True
```

The general shape is:

```python
with context_manager(arguments) as value:
    use(value)

# Teardown has completed here.
```

Context managers are appropriate for files, locks, temporary state, transactions,
connections, and other resources with a defined lifetime.

### Class-based context manager

`__enter__()` returns the value bound after `as`. `__exit__()` receives the exception
type, value, and traceback when the block fails. Returning `False` or `None` allows the
exception to propagate; returning `True` suppresses it.

```python
from time import perf_counter


class Timer:
    def __enter__(self):
        self.started_at = perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.elapsed = perf_counter() - self.started_at
        print(f"Elapsed: {self.elapsed:.2f}s")
        return False


with Timer() as timer:
    total = sum(range(1_000_000))
```

### Function-based context manager

`contextlib.contextmanager` converts a generator function that yields exactly once
into a context manager. Put teardown in `finally` so it runs if the context block
raises.

```python
from contextlib import contextmanager


@contextmanager
def database(url):
    connection = connect(url)
    try:
        yield connection
    finally:
        connection.close()


with database("postgresql://localhost/app") as connection:
    process_courses(connection)
```

In this example, `connect()` represents the client library's connection function. The
code before `yield` is setup; the value yielded becomes `connection`; and the `finally`
block is teardown.

A reusable read-only file context follows the same rule, although direct use of
`open()` is simpler when no extra behavior is needed:

```python
from contextlib import contextmanager


@contextmanager
def open_read_only(filename):
    input_file = open(filename, mode="r", encoding="utf-8")
    try:
        yield input_file
    finally:
        input_file.close()


with open_read_only("example.txt") as input_file:
    print(input_file.read())
```

### Nested contexts

Multiple context managers can share one `with` statement. They exit in reverse order.

```python
def copy_text(source, destination):
    """Copy a UTF-8 text file one line at a time."""
    with (
        open(source, "r", encoding="utf-8") as source_file,
        open(destination, "w", encoding="utf-8") as destination_file,
    ):
        for line in source_file:
            destination_file.write(line)
```

## Exceptions and tracebacks

An exception interrupts normal control flow and carries information about a failure.
Catch an exception only where the program can recover, translate it into a clearer
domain error, or add useful diagnostic context.

```python
import json
from pathlib import Path

load_attempts = 0

try:
    content = Path("settings.json").read_text(encoding="utf-8")
except FileNotFoundError:
    settings = {}
else:
    settings = json.loads(content)
finally:
    load_attempts += 1
```

| Clause | When it runs |
|---|---|
| `try` | Around code that can fail. |
| `except` | When a matching exception is raised. |
| `else` | When the `try` block completes without an exception. |
| `finally` | Whether the operation succeeds or fails. |

Avoid a bare `except:` because it also catches process-level exceptions such as
`KeyboardInterrupt` and `SystemExit`. Catch the narrowest exception that the code can
handle. A file context manager is safer than calling `close()` in `finally` on a
variable that may never have been assigned.

### Raise an appropriate exception

`ValueError` means the argument has an acceptable type but an unacceptable value.

```python
def validate_age(age):
    if not 0 <= age <= 100:
        raise ValueError("age must be between 0 and 100")

    return age
```

Create a domain-specific exception by inheriting from the closest meaningful built-in
exception:

```python
class SalaryError(ValueError):
    pass


class BonusError(SalaryError):
    pass
```

Another domain exception can protect an object's invariant:

```python
class TooManyPagesReadError(ValueError):
    pass


class ReadingProgress:
    def __init__(self, page_count):
        if page_count < 0:
            raise ValueError("page count cannot be negative")
        self.page_count = page_count
        self.pages_read = 0

    def read(self, pages):
        if pages < 0:
            raise ValueError("pages read cannot be negative")
        proposed_total = self.pages_read + pages
        if proposed_total > self.page_count:
            raise TooManyPagesReadError(
                f"cannot read {proposed_total} of {self.page_count} pages"
            )
        self.pages_read = proposed_total
```

Order handlers from the most specific exception to the most general. Otherwise the
parent handler catches the child first.

```python
try:
    employee.give_bonus(7_000)
except BonusError as error:
    logger.warning("bonus rejected: %s", error)
except SalaryError as error:
    logger.warning("salary rejected: %s", error)
```

Use a bare `raise` inside an exception handler to preserve and re-raise the current
exception. `raise NewError(...) from error` translates it while retaining the cause.

```python
try:
    payload = json.loads(raw_payload)
except json.JSONDecodeError as error:
    raise ValueError("payload cannot be decoded") from error
```

### Format a traceback

The `traceback` module can print or format the active stack trace.

```python
import logging
import traceback

logger = logging.getLogger(__name__)

try:
    result = 10 / 0
except ZeroDivisionError as error:
    logger.error("calculation failed: %s\n%s", error, traceback.format_exc())
    raise
```

For normal logging, `logger.exception("calculation failed")` inside the handler is a
shorter way to log the message and active traceback.

`pass` satisfies Python's requirement for a statement in a block and performs no
action. It is useful for a deliberate placeholder, but silently discarding exceptions
with `except Exception: pass` usually hides defects.

## Paths, files, text, and binary data

`pathlib.Path` represents filesystem paths as objects. It avoids manual string
concatenation and provides operations for inspection, traversal, reading, and writing.

```python
from pathlib import Path

program_directory = Path("/usr/bin")
current_directory = Path.cwd()

print(program_directory.resolve())
print(program_directory.is_dir())
print(program_directory.is_file())

for child in sorted(program_directory.iterdir()):
    print(child)

python_path = program_directory / "python3"
print(python_path.exists())
print(python_path.parent)
print(python_path.name)
```

`resolve()` returns an absolute path with symbolic links and `..` components resolved.
Whether it raises for a missing path depends on its `strict` argument.

### Locate the running script

`__file__` identifies the module file when that execution environment defines it. It
is normally available in a script or imported module, but not in every interactive
session.

```python
from pathlib import Path

module_path = Path(__file__).resolve()
module_directory = module_path.parent
```

The process working directory is separate from the script directory:

```python
import os
from pathlib import Path

print(os.getcwd())
print(Path.cwd())
```

Relative paths are interpreted from the working directory unless code anchors them to
another path deliberately.

### File name and stem

```python
from pathlib import Path

query_file = Path("/home/user/data/example_file.sql")

print(query_file.name)
print(query_file.stem)
```

```text
example_file.sql
example_file
```

### Text, bytes, and encodings

`str` contains Unicode text. `bytes` contains raw byte values. Decoding converts bytes
to text using a named encoding; encoding performs the reverse operation.

```python
payload = b"Hello\nWorld\n"
text = payload.decode("utf-8")
lines = text.splitlines()

print(lines)
```

```text
['Hello', 'World']
```

Specify an encoding when reading text whose format defines one:

```python
from pathlib import Path

text = Path("message.txt").read_text(encoding="utf-8")
```

A `UnicodeDecodeError` means the selected decoder cannot interpret the byte sequence.
Trying likely encodings can be an investigation technique, but a successful decode
does not prove that the chosen encoding is correct. Prefer source metadata, a byte
order mark, or a documented contract.

### String formatting and escapes

```python
days = 20
print(f"{days} days are {days * 24 * 60 * 60} seconds")
print("Insert {number} here".format(number=15))
print("Insert {0} here".format(15))
print("Insert {} here".format(15))
```

```text
20 days are 1728000 seconds
Insert 15 here
Insert 15 here
Insert 15 here
```

A backslash introduces escapes inside a string literal:

```python
print("One\nTwo\nThree")
print("\tIndented")
print("He's a valid contraction")
print('He\'s also valid')
```

### JSON and safe literal parsing

JavaScript Object Notation (JSON) is a text format. `json.loads()` deserializes a JSON
string into Python dictionaries, lists, strings, numbers, Boolean values, and `None`.

```python
import json

raw_payload = '{"name": "Ava", "active": true}'
payload = json.loads(raw_payload)
print(payload["name"])
```

```text
Ava
```

`ast.literal_eval()` parses strings containing Python literal structures without
executing arbitrary Python expressions. It is suitable for trusted-size input that is
known to use Python literal syntax, not JSON.

```python
import ast

value = ast.literal_eval("{'team': 'blue', 'scores': [4, 7]}")
```

Do not replace `literal_eval()` with `eval()` for data parsing. `eval()` executes code.

### File-pattern matching

`Path.glob()` keeps matched paths as `Path` objects:

```python
from pathlib import Path

python_files = list(Path.cwd().glob("**/*.py"))
```

The standard-library `glob` module provides a string-based alternative:

```python
import glob

python_files = glob.glob("**/*.py", recursive=True)
```

## Collections, iteration, and core expressions

Python's built-in collections cover sequences, mappings, and sets. The `collections`
and `itertools` modules provide specialized behavior without requiring a custom data
structure.

### Specialized containers from `collections`

| Type | Primary use |
|---|---|
| `namedtuple` | An immutable tuple subclass with named fields. |
| `deque` | Fast appends and pops at both ends. |
| `Counter` | Counts hashable values. |
| `defaultdict` | Creates a missing value through a factory function. |
| `OrderedDict` | Ordered mapping with order-sensitive equality and explicit reordering operations. |

Normal dictionaries preserve insertion order. `OrderedDict` remains useful for its
special reordering operations. Equality between two `OrderedDict` instances is
order-sensitive; equality with another mapping follows ordinary mapping semantics.

```python
from collections import Counter

creature_types = ["Grass", "Dark", "Fire", "Fire", "Grass"]
type_counts = Counter(creature_types)

print(type_counts)
```

```text
Counter({'Grass': 2, 'Fire': 2, 'Dark': 1})
```

### Iterator building blocks from `itertools`

`itertools` functions return lazy iterators.

| Family | Examples |
|---|---|
| Infinite iterators | `count`, `cycle`, `repeat` |
| Finite iterator tools | `accumulate`, `chain`, `zip_longest` |
| Combinatoric iterators | `product`, `permutations`, `combinations` |

```python
from itertools import combinations

creature_types = ["Bug", "Fire", "Ghost", "Grass", "Water"]
pair_iterator = combinations(creature_types, 2)
pairs = list(pair_iterator)

print(pairs[:5])
```

```text
[('Bug', 'Fire'), ('Bug', 'Ghost'), ('Bug', 'Grass'), ('Bug', 'Water'), ('Fire', 'Ghost')]
```

Materializing an infinite iterator with `list()` never completes. Bound it with a
consumer such as `itertools.islice()`.

### Sets and membership

A set stores unique hashable elements and supports mathematical set operations.

| Operation | Method | Operator |
|---|---|---|
| Values in either set | `union()` | `\|` |
| Values in both sets | `intersection()` | `&` |
| Values in the left set only | `difference()` | `-` |
| Values in exactly one set | `symmetric_difference()` | `^` |

```python
names_a = {"Bulbasaur", "Charmander", "Squirtle"}
names_b = {"Caterpie", "Pidgey", "Squirtle"}

print(names_a | names_b)
print(names_a & names_b)
print(names_a - names_b)
print(names_a ^ names_b)
print("Squirtle" in names_a)
```

`in` tests membership for sets, dictionaries, lists, tuples, strings, and other
containers. A set normally provides faster membership checks than a list when order
and duplicates are not needed.

### Lists and sorting

```python
values = [3, 1, 2, 1]

print(values.count(1))
print(values.index(2))

values.remove(1)
values.reverse()

print(sorted(values))
print(sorted(values, reverse=True))
```

`list.remove()` removes the first equal value and raises `ValueError` if it is absent.
`list.reverse()` mutates the list and returns `None`; `sorted()` returns a new list.

```python
words = ["banana", "apple", "pear"]
print(sorted(words, key=len))

counts = {"banana": 3, "apple": 1, "pear": 2}
print(sorted(counts.items(), key=lambda item: item[1]))
```

Strings compare lexicographically by Unicode code point sequence:

```python
print("Annie" > "Andy")
```

```text
True
```

### Dictionaries

A dictionary comprehension constructs a mapping from an iterable:

```python
users = [
    (0, "Bob", "password"),
    (1, "Rolf", "bob123"),
    (2, "Jose", "longPassword"),
]

users_by_name = {user[1]: user for user in users}
print(users_by_name["Bob"])
```

`get()` returns a default instead of raising `KeyError` for a missing key:

```python
profile = {"name": "Alice", "email": "alice@example.com", "age": 28}

name = profile.get("name")
location = profile.get("location", "Unknown")
```

Without a unique sentinel, `get()` cannot distinguish a missing key from a key whose
stored value is `None`.

`setdefault()` returns an existing value. If the key is absent, it first inserts the
provided default and returns it.

```python
groups = {}
members = groups.setdefault("engineering", [])
members.append("Ava")
```

Do not use `setdefault()` when constructing its default is expensive on every call;
`defaultdict` or an explicit branch can be clearer.

### Packing and unpacking arguments

`*args` packs extra positional arguments into a tuple. `**kwargs` packs extra keyword
arguments into a dictionary. The same operators unpack an existing iterable or
mapping at a call site.

```python
def multiply(*values):
    total = 1
    for value in values:
        total *= value
    return total


def add(x, y):
    return x + y


numbers = [3, 5]
coordinates = {"x": 15, "y": 25}

print(add(*numbers))
print(add(**coordinates))
```

Parameters after `*args` are keyword-only:

```python
def apply(*values, operator):
    if operator == "*":
        return multiply(*values)
    if operator == "+":
        return sum(values)
    raise ValueError(f"unsupported operator: {operator}")


print(apply(1, 3, 6, 7, operator="+"))
```

```python
def show_arguments(*args, **kwargs):
    print(args)
    print(kwargs)


show_arguments(1, 3, 5, name="Bob", age=25)
```

### Assignment, references, and mutability

Python evaluates the right side of an assignment before binding the result to the name
on the left.

```python
x = 15
```

Names refer to objects; variables are not boxes that contain independent copies.

```python
first = [1, 2]
second = first
second.append(3)

print(first)
```

```text
[1, 2, 3]
```

Lists, dictionaries, and sets are mutable. Integers, floats, Booleans, strings,
tuples, bytes, and frozensets are immutable. Immutability applies to the container
itself: an immutable tuple can still refer to a mutable object.

Use `isinstance()` for a runtime type relationship:

```python
number = 5
print(isinstance(number, int))
```

Use `is` for identity, most commonly `value is None`. Use `==` for value equality.

### Compact expressions and loop control

A conditional expression has three parts:

```python
label = "adult" if age >= 18 else "minor"
```

The assignment expression operator `:=`, sometimes called the walrus operator, binds
a value inside a larger expression. Use it only when it avoids duplicated work without
making the condition harder to read.

```python
if (line := input_file.readline()):
    process(line)
```

Augmented assignment updates a target with an operation:

```python
total += 3
remainder %= 10
flags |= new_flags
```

For integers, `|=` applies bitwise OR. For sets, it updates the left set with the union:

```python
left = {1, 2, 3}
right = {3, 4, 5}
left |= right

print(sorted(left))
```

```text
[1, 2, 3, 4, 5]
```

`continue` skips the rest of the current loop iteration. `break` exits the nearest
loop.

```python
for number in range(1, 6):
    if number == 3:
        continue
    print(number)
```

```text
1
2
4
5
```

```python
number = 0

while True:
    print(number)
    number += 1
    if number >= 5:
        break
```

## Functions as objects and decorators

Functions are first-class objects. Code can assign them to names, place them in
collections, pass them as arguments, and return them from other functions.

```python
def add(x, y):
    return x + y


def divide(x, y):
    return x / y


def calculate(*values, operator):
    return operator(*values)


result = calculate(20, 4, operator=divide)
```

A decorator accepts a callable and returns a replacement callable. The replacement
usually delegates to the original while adding behavior before or after it.

```python
def announce(function):
    def wrapper():
        print("before")
        result = function()
        print("after")
        return result

    return wrapper


def say_hello():
    print("hello")


say_hello = announce(say_hello)
say_hello()
```

The `@` syntax performs the same assignment at definition time:

```python
@announce
def say_hello():
    print("hello")
```

### Preserve metadata and accept arbitrary arguments

Without help, the wrapper hides the original function's name and docstring.
`functools.wraps()` copies that metadata and exposes the wrapped callable.

```python
from functools import wraps


def trace_call(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"calling {function.__name__}")
        return function(*args, **kwargs)

    return wrapper


@trace_call
def greet(name, punctuation="!"):
    """Return a greeting."""
    return f"Hello, {name}{punctuation}"
```

### Decorator factory with parameters

A decorator factory adds another function layer so configuration can be supplied
before the target function is known.

```python
from functools import wraps


def requires_access(required_level):
    def decorator(function):
        @wraps(function)
        def wrapper(user, *args, **kwargs):
            if user.get("access_level") != required_level:
                raise PermissionError(
                    f"{required_level} access is required"
                )
            return function(user, *args, **kwargs)

        return wrapper

    return decorator


@requires_access("admin")
def read_admin_panel(user, panel_name):
    return f"panel: {panel_name}"
```

This demonstrates decorator mechanics, not a production authorization design. Real
authorization should use authenticated identities, centrally defined policy, and
auditable decisions rather than a caller-supplied dictionary.

## Object-oriented design

An object combines state and behavior. An attribute is a value reached through dot
notation; a method is a function stored on a class and bound through an instance or
class.

```text
object
  |-- attributes: employee.name, employee.salary
  `-- methods:    employee.give_raise(), employee.monthly_salary()
```

### Define and instantiate a class

`__init__()` initializes a newly created instance. `self` is the instance receiving an
instance-method call.

```python
class Employee:
    MIN_SALARY = 30_000

    def __init__(self, name, salary):
        self.name = name
        self.salary = max(salary, self.MIN_SALARY)

    def give_raise(self, amount):
        if amount < 0:
            raise ValueError("raise amount cannot be negative")
        self.salary += amount

    def monthly_salary(self):
        return self.salary / 12


employee = Employee("Korel Rossi", 40_000)
employee.give_raise(2_000)

print(employee.name)
print(employee.salary)
print(employee.monthly_salary())
```

`MIN_SALARY` is a class attribute shared through the class. Assigning the same name on
an instance creates or replaces an instance attribute; it does not update the class
attribute for every object.

### Instance, class, and static methods

| Kind | First implicit argument | Typical use |
|---|---|---|
| Instance method | `self`, the instance | Reads or changes instance state. |
| Class method | `cls`, the receiving class | Alternate constructors or class-wide behavior. |
| Static method | None | Related utility that needs neither instance nor class state. |

```python
class Book:
    TYPES = ("hardcover", "paperback")

    def __init__(self, name, book_type, weight):
        self.name = name
        self.book_type = book_type
        self.weight = weight

    @classmethod
    def hardcover(cls, name, page_weight):
        return cls(name, cls.TYPES[0], page_weight + 100)

    @classmethod
    def paperback(cls, name, page_weight):
        return cls(name, cls.TYPES[1], page_weight)

    @staticmethod
    def grams_to_kilograms(grams):
        return grams / 1_000


heavy = Book.hardcover("Python 101", 1_500)
light = Book.paperback("Python 101", 600)
```

A function defined in a class body still participates in method binding when accessed
through an instance. If it intentionally accepts neither `self` nor `cls`, mark it
`@staticmethod` or keep it as a module-level function.

### String representations

`__str__()` supplies a readable representation for users. `__repr__()` supplies an
unambiguous developer representation and should be useful for debugging. The `!r`
conversion in an f-string calls `repr()`.

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}, {self.age} years old"

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age!r})"


person = Person("Bob", 35)
print(person)
print(repr(person))
```

```text
Bob, 35 years old
Person(name='Bob', age=35)
```

Names such as `__init__`, `__str__`, `__repr__`, and `__eq__` are special methods,
sometimes called dunder methods. Python's data model invokes them for defined language
operations. Implementing these hooks customizes or overloads the related language
operation for the class.

### Identity and equality

Two variables can refer to different objects with equal data. User-defined objects use
identity-based equality unless the class defines value equality.

```python
class BankAccount:
    def __init__(self, number, balance=0):
        self.number = number
        self.balance = balance

    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.number == other.number


first = BankAccount(123, 1_000)
second = BankAccount(123, 1_000)

print(first is second)
print(first == second)
```

```text
False
True
```

Returning `NotImplemented` lets Python try the reflected comparison or conclude that
the objects are unequal. A mutable class that defines `__eq__()` normally remains
unhashable unless it can also define a stable, compatible `__hash__()`.

### Inheritance and customized behavior

Inheritance represents an "is a" relationship. A subclass inherits behavior and can
extend or override it. `super()` delegates according to the class method resolution
order.

```python
class BankAccount:
    def __init__(self, balance=0):
        if balance < 0:
            raise ValueError("opening balance cannot be negative")
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount


class SavingsAccount(BankAccount):
    def __init__(self, balance, interest_rate):
        super().__init__(balance)
        self.interest_rate = interest_rate

    def compute_interest(self, periods=1):
        return self.balance * (
            (1 + self.interest_rate) ** periods - 1
        )


class CheckingAccount(BankAccount):
    def __init__(self, balance, fee_limit):
        if fee_limit < 0:
            raise ValueError("fee limit cannot be negative")
        super().__init__(balance)
        self.fee_limit = fee_limit

    def withdraw(self, amount, fee=0):
        if fee < 0:
            raise ValueError("fee cannot be negative")
        charged_fee = min(fee, self.fee_limit)
        super().withdraw(amount + charged_fee)
```

The Liskov Substitution Principle (LSP) says callers using a base-class contract should
also work correctly with a subtype. A subclass that unexpectedly strengthens
preconditions, weakens guarantees, or changes the meaning of inherited operations is
usually modeling the wrong relationship.

```python
class Device:
    def __init__(self, name, connected_by):
        self.name = name
        self.connected_by = connected_by
        self.connected = True

    def disconnect(self):
        self.connected = False


class Printer(Device):
    def __init__(self, name, connected_by, capacity):
        if capacity < 0:
            raise ValueError("capacity cannot be negative")
        super().__init__(name, connected_by)
        self.remaining_pages = capacity

    def print_pages(self, pages):
        if pages <= 0:
            raise ValueError("page count must be positive")
        if not self.connected:
            raise RuntimeError("printer is disconnected")
        if pages > self.remaining_pages:
            raise ValueError("not enough paper")
        self.remaining_pages -= pages
```

### Composition instead of inheritance

Composition represents a "has a" relationship. A bookshelf has books; it is not a
specialized kind of book.

```python
class Book:
    def __init__(self, name):
        self.name = name


class BookShelf:
    def __init__(self, *books):
        self.books = list(books)

    def __str__(self):
        return f"BookShelf with {len(self.books)} books"


shelf = BookShelf(Book("Python 101"), Book("Data Systems"))
```

Composition is often easier to change because it avoids coupling behavior through a
class hierarchy.

### Cooperative multiple inheritance

Multiple inheritance follows the method resolution order (MRO). Cooperative classes
use `super()` consistently and accept compatible arguments so each initializer runs
once.

```python
class Vehicle:
    def __init__(self, *, wheels, **kwargs):
        super().__init__(**kwargs)
        self.wheels = wheels


class BatteryPowered:
    def __init__(self, *, battery_capacity, **kwargs):
        super().__init__(**kwargs)
        self.battery_capacity = battery_capacity


class ElectricCar(Vehicle, BatteryPowered):
    def __init__(self, *, wheels, battery_capacity, doors):
        super().__init__(
            wheels=wheels,
            battery_capacity=battery_capacity,
        )
        self.doors = doors


car = ElectricCar(wheels=4, battery_capacity=75, doors=4)
print(ElectricCar.mro())
```

Directly calling each parent initializer can duplicate work or bypass another class in
the MRO. Use multiple inheritance deliberately; composition is simpler when the
relationship does not require substitutable base types.

### Internal attributes and properties

A single leading underscore, such as `_cache`, marks a name as non-public by
convention. A double leading underscore, such as `__version`, triggers name mangling to
reduce accidental name collisions in subclasses. It does not provide access control
or make the attribute truly private.

A property exposes method-backed behavior with attribute syntax.

```python
class Account:
    def __init__(self, balance=0):
        self.balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("balance cannot be negative")
        self._balance = value

    @balance.deleter
    def balance(self):
        raise AttributeError("balance cannot be deleted")
```

Omit the setter to make assignment through the property unavailable. Use properties
when validation or computation belongs behind an attribute-like interface, not merely
to wrap every public attribute. `@name.getter` can replace a getter on an existing
property, but `@property` normally defines the initial getter.

For a method returning its own class, a quoted forward reference is portable across
many supported Python environments:

```python
from typing import Self


class Book:
    def __init__(self, name: str, book_type: str, weight: int):
        self.name = name
        self.book_type = book_type
        self.weight = weight

    @classmethod
    def hardcover(cls, name: str, page_weight: int) -> Self:
        return cls(name, "hardcover", page_weight + 100)
```

## Modules, imports, and executable packages

The import system finds a module, creates its module object, executes its top-level
code during a successful import, and caches the object in `sys.modules`. Later imports
under the same name normally reuse that object. Reloading, removing the cache entry, or
loading the file under another name can execute its top-level code again.

A regular package can be arranged like this:

```text
project/
|-- pyproject.toml
|-- README.md
|-- src/
|   `-- reporting/
|       |-- __init__.py
|       |-- __main__.py
|       |-- cli.py
|       `-- preprocessing/
|           |-- __init__.py
|           `-- clean.py
`-- tests/
    `-- test_clean.py
```

`__init__.py` defines a regular package and can initialize or re-export its public
interface. It does not need to be empty. Namespace packages can span locations and can
omit `__init__.py`, so not every importable package directory contains the file.

### Absolute and relative imports

An absolute import starts from an importable top-level package:

```python
from reporting.preprocessing import clean
```

An explicit relative import starts from the current package. One dot means the current
package; two dots mean its parent:

```python
from . import clean
from ..cli import main
```

Absolute imports are usually clearer across a project. Relative imports can keep
internal package references concise. Importing `reporting` does not automatically
execute imports for every subpackage unless `reporting/__init__.py` deliberately
imports them. Code can still import `reporting.preprocessing` directly.

### Control wildcard exports

`__all__` defines the names exported by `from module import *`:

```python
__all__ = ["clean_records", "validate_records"]
```

It documents an intended public surface but does not enforce privacy. Explicit imports
can still reach other names.

### Inspect loaded modules and execution names

```python
import sys

print(sys.modules)
print(__name__)
```

An imported module normally sees its qualified import name in `__name__`. The module
selected as the program entry point sees `__main__`.

```python
def main() -> int:
    print("run application")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The guard lets the file expose reusable functions without running application behavior
when another module imports it.

### Run a package with `-m`

`package/__main__.py` runs when the package is executed as a module:

```bash
python -m reporting
```

```python
# reporting/__main__.py
from reporting.cli import main

raise SystemExit(main())
```

### Import paths

Python searches locations recorded in `sys.path`. The `PYTHONPATH` environment
variable can add search locations, but a broad permanent value can hide packaging
errors and make behavior depend on a developer's machine. Prefer installing the
project into its environment during development:

```bash
python -m pip install -e .
```

If `PYTHONPATH` is unavoidable for a temporary command, add only the exact source
directory and preserve any existing value.

### Command-line arguments

`sys.argv` contains the script name followed by raw argument strings:

```python
import sys

script_name = sys.argv[0]
file_arguments = sys.argv[1:]
argument_count = len(sys.argv)
```

For validation, help text, flags, and typed values, use `argparse` instead of manually
indexing the list:

```python
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    return parser.parse_args()


def main():
    arguments = parse_arguments()
    for file_name in arguments.files:
        check_file(file_name)


if __name__ == "__main__":
    main()
```

```bash
python check_owner_email.py models/staging/schema.yml models/marts/schema.yml
```

## Standard-library runtime tools

### Run external processes

`subprocess.run()` starts a child process, waits for it, and returns a
`CompletedProcess`. Pass arguments as a list so Python handles argument boundaries
without invoking a shell.

```python
import subprocess

completed = subprocess.run(
    ["git", "status", "--short"],
    check=True,
    capture_output=True,
    text=True,
)

print(completed.stdout)
```

`check=True` raises `subprocess.CalledProcessError` for a nonzero exit status.
`capture_output=True` captures both output streams. `text=True` decodes them as text
using the selected or default encoding.

`cwd=` sets the working directory for the child process without changing the parent
Python process:

```python
import subprocess


def configure_repository(repository, user_name):
    subprocess.run(
        ["git", "config", "user.name", user_name],
        cwd=repository,
        check=True,
    )
```

Avoid `shell=True` for ordinary commands. A shell is needed only for shell syntax or
built-ins, and untrusted text inserted into a shell command can become command
injection. Argument lists avoid shell parsing, but the called program can still assign
special meaning to untrusted arguments.

Older convenience functions map to `run()`:

```python
subprocess.run(arguments, check=True)
subprocess.run(
    arguments,
    check=True,
    stdout=subprocess.PIPE,
).stdout
```

These correspond to the common behavior of `check_call()` and `check_output()`.
Without text mode or an encoding, captured output is bytes.

For a pipeline that genuinely requires direct process control, connect `Popen`
instances and close the parent's copy of the first output pipe. This example uses
Portable Operating System Interface (POSIX) command-line utilities:

```python
from subprocess import PIPE, Popen

producer = Popen(["printf", "hello world\n"], stdout=PIPE)
consumer = Popen(
    ["grep", "hello"],
    stdin=producer.stdout,
    stdout=PIPE,
    text=True,
)

if producer.stdout is not None:
    producer.stdout.close()

output, _ = consumer.communicate()
producer_return_code = producer.wait()

if producer_return_code != 0 or consumer.returncode != 0:
    raise RuntimeError("pipeline failed")

print(output)
```

### Standard output and standard error

`sys.stdout` is the normal output stream. `sys.stderr` is the diagnostic stream.

```python
import sys

try:
    result = 10 / 0
except ZeroDivisionError as error:
    print(f"calculation failed: {error}", file=sys.stderr)
```

Separate streams let callers redirect results and diagnostics independently.

### Logging

Logging records runtime events with a name, severity, timestamp, and optional exception
context. Configure handlers and thresholds once at the application entry point.
Libraries should create a named logger but should not call `basicConfig()`.

| Level | Use |
|---|---|
| `DEBUG` | Detailed diagnostic data useful during investigation. |
| `INFO` | Expected lifecycle events and successful milestones. |
| `WARNING` | Unexpected or degraded behavior that did not stop the operation. |
| `ERROR` | A requested operation failed. |
| `CRITICAL` | The process or a critical subsystem may be unable to continue. |

```python
import logging

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    logger.info("application started")
```

Inside an exception handler, `logger.exception()` includes the active traceback:

```python
try:
    run_pipeline()
except PipelineError:
    logger.exception("pipeline failed")
    raise
```

Do not log secrets, tokens, passwords, or unrestricted payloads.

### Unique identifiers

A universally unique identifier (UUID) is a 128-bit identifier. `uuid4()` generates a
random UUID suitable for correlation IDs where no central sequence is required.

```python
import uuid

query_id = str(uuid.uuid4())
logger.debug("starting query %s", query_id)
```

Random UUIDs are not ordered and do not guarantee that a collision is mathematically
impossible. Their space makes accidental collisions impractical for normal use.

### Measure elapsed time

Wall-clock time can move because of clock corrections. Use a monotonic clock for
deadlines and elapsed durations; use the higher-resolution performance counter for
benchmarks.

```python
import time

started_at = time.monotonic()
run_operation()
elapsed = time.monotonic() - started_at

logger.info("operation completed in %.2f seconds", elapsed)
```

Only differences between monotonic or performance-counter readings are meaningful.

## Environments and dependency installation

Interpreter selection and package isolation solve different problems:

```text
pyenv                     selects a Python interpreter
  |
venv or pyenv-virtualenv  isolates installed packages
  |
pip or Poetry             installs and resolves dependencies
  |
ipykernel                 exposes that environment to Jupyter
```

Check which interpreter a shell command will use:

```bash
python --version
python -c "import sys; print(sys.executable)"
```

Use `python -m pip` rather than a bare `pip` command when interpreter selection
matters. It runs the installer attached to that `python` executable.

### Create a virtual environment with `venv`

`venv` is part of the standard library and creates an isolated package environment for
the interpreter that runs it.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

On Windows PowerShell, activation uses `.venv\Scripts\Activate.ps1`. Activation mainly
adjusts shell paths; invoking `.venv/bin/python` or the Windows equivalent directly
also selects the environment. Run `deactivate` to undo activation in the current
shell.

### Select interpreters with `pyenv`

`pyenv` installs and selects Python versions through shims. It does not by itself
isolate project packages.

```bash
brew install pyenv
PYTHON_VERSION=3.x.y
pyenv install "$PYTHON_VERSION"
pyenv versions
pyenv local "$PYTHON_VERSION"
python --version
```

Replace `3.x.y` with an interpreter version allowed by the project.

`pyenv local` writes `.python-version` in the current directory. Remove the selection
without manually deleting the file:

```bash
pyenv local --unset
```

Uninstall an interpreter only after confirming that no project depends on it:

```bash
pyenv uninstall "$PYTHON_VERSION"
```

The exact shell initialization depends on how `pyenv` was installed. For a standard
Z shell setup, add the required initialization once to `~/.zshrc`:

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - zsh)"
```

Then reload the configuration in the current shell:

```bash
source ~/.zshrc
```

`.zshrc` is a configuration file loaded by interactive Z shell sessions. Inspect it
before appending configuration so repeated setup does not create duplicate entries.

### Compare environment tools

| Tool | Responsibility |
|---|---|
| `pyenv` | Installs and selects Python interpreters. |
| `venv` | Creates an isolated environment from the selected interpreter. |
| `virtualenv` | Third-party environment creator with additional features and interpreter discovery. |
| `pyenv-virtualenv` | Adds virtual-environment management and activation to `pyenv`. |

With the `pyenv-virtualenv` plugin:

```bash
brew install pyenv-virtualenv
eval "$(pyenv virtualenv-init -)"
PYTHON_VERSION=3.x.y
pyenv virtualenv "$PYTHON_VERSION" analytics-guide
pyenv local analytics-guide
pyenv deactivate
pyenv local --unset
```

Add the initialization command once to the shell configuration when the installation
instructions require it. Automatic activation can then change as the shell enters or
leaves a directory that contains `.python-version`.

Advanced Package Tool (APT) is the operating-system package manager used by Debian and
related Linux distributions. It installs system packages; it is not a Python package
manager.

### Install packages with pip

`pip` is a Python package installer. The Python Package Index (PyPI) is the default
public index from which pip can resolve distributions.

```bash
python -m pip install requests
python -m pip install --upgrade requests
python -m pip uninstall requests
```

Requirement specifier shapes include:

```text
package-name==exact-version
package-name>=minimum-version
package-name>=minimum-version,<incompatible-version
```

Inspect the current environment:

```bash
python -m pip list
python -m pip list --outdated
python -m pip show pandas
```

Install a local wheel or the current project in editable mode:

```bash
python -m pip install dist/example_project-1.2.0-py3-none-any.whl
python -m pip install -e .
python -m pip install -e ".[dev]"
```

An editable installation points the environment at the working source so most code
changes are visible without rebuilding. The project still needs valid build metadata.

### Private package indexes

`--index-url` replaces the default index for the complete resolution operation. This
means dependencies are also sought from that index.

```bash
python -m pip install \
  --index-url https://packages.example.com/simple \
  internal-package
```

Do not place credentials in commands, source files, or shell history. Configure the
installer's supported credential store or environment integration. `--extra-index-url`
adds another source but can create dependency-confusion risk if private and public
projects share names; use an index design that prevents ambiguous resolution.

### Requirements and constraints files

A requirements file describes an install operation or environment. Each line can be a
requirement specifier, an option, a local project, an editable project, another
requirements file, a constraints file, or a direct archive or version-control Uniform
Resource Locator (URL).

```text
# requirements.txt
numpy
pandas
requests[socks]
pytest
-r reporting-requirements.txt
-c constraints.txt
```

```bash
python -m pip install -r requirements.txt
```

A constraints file limits versions selected for packages requested elsewhere. It does
not cause those packages to be installed.

```text
# constraints.txt
# The application has been verified only with urllib3 major version 2.
urllib3>=2,<3
```

```bash
python -m pip install \
  -r requirements.txt \
  -c constraints.txt
```

Direct URLs are valid requirements, but reproducible environments should pin immutable
artifacts and use hashes where the workflow supports them.

`pip freeze` records every installed distribution, including transitive dependencies:

```bash
python -m pip freeze > requirements-frozen.txt
```

That output is an environment snapshot. It is not automatically the right declaration
of the minimal runtime requirements for a reusable library.

### Use Poetry for a managed project environment

Poetry is a third-party dependency, environment, build, and publishing workflow. Its
commands should be run separately; `>` in a shell redirects output and does not mean
"then run the next command."

```bash
poetry install
poetry add pandas
poetry run pytest
poetry build
poetry version patch
```

To add a caret constraint through the command line, use
`poetry add "package-name@^X.Y"`; legacy `[tool.poetry.dependencies]` configuration
uses `package-name = "^X.Y"`. `poetry version patch` updates the declared project
version. Verifying a built wheel in a fresh environment is separate from installing
development dependencies:

```bash
python -m pip install dist/example_project-1.2.1-py3-none-any.whl
```

### Register an environment as a Jupyter kernel

Install `ipykernel` inside the selected environment, then register a distinct kernel
name and readable display name:

```bash
python -m pip install ipykernel
python -m ipykernel install \
  --user \
  --name analytics-guide \
  --display-name "Python (analytics-guide)"
jupyter kernelspec list
```

The listed kernel directory contains `kernel.json`, which records how Jupyter starts
the interpreter. Inspect it when a notebook appears to use the wrong environment.

### Inspect an installed distribution version

An imported package may expose `__version__`, but that attribute is only a convention.
The standard metadata interface reads the installed distribution version:

```python
from importlib.metadata import version

print(version("pandas"))
```

The distribution name passed to `version()` may differ from the import name.

### Repeatable coding workflow

```text
clone repository
      |
create or select feature branch
      |
select interpreter and create environment
      |
install project and development dependencies
      |
register a Jupyter kernel only when needed
      |
edit -> format/lint -> test
      |
build and verify an artifact only when distributing
```

Example commands:

```bash
git clone repository-url
git switch -c feature-name
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
python -m build
deactivate
```

## Packaging and distribution

Packaging turns a source tree into artifacts that another environment can install.
The import package, distribution project, build backend, installer, and package index
are separate parts of that flow.

```text
source code + pyproject.toml
             |
             | python -m build
             v
wheel + source distribution
             |
             | python -m twine upload
             v
PyPI, TestPyPI, or a private index
             |
             | python -m pip install
             v
installed environment
```

### Project configuration with `pyproject.toml`

`pyproject.toml` is the standard configuration entry point for Python builds. It uses
Tom's Obvious, Minimal Language (TOML) and can declare the build backend, project
metadata, dependencies, command entry points, and tool-specific settings.

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "example-reporting"
version = "1.2.0"
description = "Reporting utilities"
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"
license-files = ["LICENSE*"]
dependencies = [
  "httpx>=0.27",
]
classifiers = [
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  "Programming Language :: Python :: 3",
]

[project.optional-dependencies]
dev = [
  "build",
  "pytest",
  "black",
  "flake8",
  "twine",
]

[project.scripts]
example-report = "example_reporting.cli:main"
```

The three main table families are:

| Table | Responsibility |
|---|---|
| `[build-system]` | Selects the build backend and its build-time requirements. |
| `[project]` | Declares standardized project metadata and runtime dependencies. |
| `[tool.<name>]` | Stores configuration defined by an individual tool. |

A build frontend, such as `build` or pip, invokes the selected build backend. The
backend, such as Hatchling or setuptools, reads the configuration and creates the
artifact.

Dependencies in `[project]` state what an installed project needs to run. Requirements
files describe an installation or environment. Constraints limit resolution. They
serve related but different purposes.

### Source layout

A small distributable project can use this shape:

```text
example-reporting/
|-- pyproject.toml
|-- README.md
|-- LICENSE
|-- CHANGELOG.md
|-- src/
|   `-- example_reporting/
|       |-- __init__.py
|       |-- __main__.py
|       `-- cli.py
`-- tests/
    `-- test_cli.py
```

The `src/` layout makes tests exercise an installed package rather than accidentally
importing directly from the repository root. It is a useful packaging pattern, not a
requirement for every script or portfolio example.

README content explains installation and use. License metadata communicates the
project's licensing terms. Classifiers help users discover a project, but
`requires-python` is what constrains supported interpreter versions during
installation.

### Source distributions and wheels

| Artifact | Typical extension | Contents and install behavior |
|---|---|---|
| Source distribution | `.tar.gz` | Source files and build metadata. An installer normally builds a wheel before installation. |
| Wheel | `.whl` | A ZIP-format built distribution arranged for installation without running the project's build step. |

Pure-Python wheels usually contain `.py` source files and can be platform independent.
Wheels with compiled extensions can target a particular operating system, processor,
and Python application binary interface. A wheel is not generally a bundle of `.pyc`
bytecode files.

Build both standard artifact types through the configured backend:

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
```

Build artifacts conventionally appear in `dist/`. `bin/` and `target/` have no
standard Python packaging meaning, although an individual project may define them for
its own scripts or generated output.

### Include non-code files

Modern backends define package-data rules through their own `pyproject.toml`
configuration. The standardized `license-files` field identifies license files.

`MANIFEST.in` is a setuptools-specific mechanism used primarily to control additional
files in a source distribution:

```text
include README.md
recursive-include src/example_reporting/templates *.html
```

Do not assume that one manifest automatically governs every backend or that source
distribution rules always equal wheel-content rules. Inspect both built artifacts.

### Publish to an index

PyPI is the public Python Package Index. TestPyPI is a separate index for testing the
release flow.

```bash
python -m twine upload --repository testpypi dist/*
python -m twine upload dist/*
```

Use scoped upload tokens or a supported trusted-publishing workflow. Do not put tokens
in source control or commands stored in shell history. After publication, consumers
install the distribution project name:

```bash
python -m pip install example-reporting
```

The import can use a normalized Python identifier even when the distribution uses
hyphens:

```python
import example_reporting
```

### Versions and change history

`major.minor.patch` is the common Semantic Versioning shape:

| Change | Example meaning |
|---|---|
| Major | An incompatible public-interface change. |
| Minor | Backward-compatible functionality. |
| Patch | A backward-compatible fix. |

Python distributions follow the broader PEP 440 version rules, which also cover
development, pre-release, post-release, and local version identifiers.

Version-bumping tools can update declared versions and create commits or tags. Review
the proposed files and version transition rather than treating automation as the
source of release policy. Older projects may use `bumpversion`; maintained successors
and other release tools provide the same general automation around configured files.

A changelog or `HISTORY.md` commonly groups entries under labels such as Added,
Changed, Fixed, and Deprecated. A slug is a short machine-friendly identifier made
from characters such as letters, numbers, hyphens, or underscores. Project and package
names have their own normalization rules, so a generic URL slug is not automatically a
valid import name.

### Project generators and task runners

Cookiecutter is a third-party project generator. It renders a directory tree from a
template and prompted values:

```bash
cookiecutter template-url
```

The generated output can include `pyproject.toml`, a package directory, tests, and
automation files. Inspect the template first; generation does not guarantee that its
dependencies or practices match the project.

A Makefile is an optional task runner, not a catalog of the package's Python functions:

```makefile
.PHONY: clean test build

clean:
	rm -rf build dist

test:
	python -m pytest

build:
	python -m build
```

Targets such as `make clean`, `make test`, and `make build` provide stable project
commands while their implementation remains in one file.

### Legacy packaging concepts

`setup.py` and `setup.cfg` remain valid configuration inputs for compatible projects,
but direct command execution through `setup.py` is deprecated. Historical commands
such as these should be replaced by standards-based frontends:

```text
python setup.py sdist
python setup.py bdist_wheel
```

Current equivalent:

```bash
python -m build
```

Eggs are obsolete distribution artifacts. Wheels are the current built-distribution
format. When maintaining an older project, migrate behavior carefully rather than
deleting legacy configuration before the modern build produces equivalent artifacts.

## Testing and code quality

Tests execute behavior and assert outcomes. Linters inspect code for likely errors and
style violations. Formatters rewrite presentation into a consistent form. Type
checkers compare annotations and inferred types. These tools overlap, but none replaces
the others.

### Write tests with pytest

pytest is a third-party test runner. It normally discovers files named `test_*.py` or
`*_test.py`, then functions and methods whose names begin with `test_`.

```text
project/
|-- pyproject.toml
|-- src/
|   `-- reporting/
|       `-- statistics.py
`-- tests/
    `-- test_statistics.py
```

Install the project in editable mode and use an absolute import from the test:

```python
from reporting.statistics import standardize
```

A basic test follows Arrange, Act, Assert:

```python
def add(x, y):
    return x + y


def test_adds_two_numbers():
    # Arrange
    left = 2
    right = 3

    # Act
    result = add(left, right)

    # Assert
    assert result == 5
```

Run the suite from the project root:

```bash
python -m pytest
```

The `tests/` directory is conventional, not mandatory. Tests that import the installed
project through absolute imports do not require `tests/__init__.py`. Explicit relative
imports among test modules generally require the test directory to be imported as a
package.

Fixtures provide reusable setup. Parametrization runs one test contract against
multiple cases:

```python
import pytest


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, 0),
        (1, 1),
        (-1, 1),
    ],
)
def test_absolute_value(value, expected):
    assert abs(value) == expected
```

### Replace collaborators with `unittest.mock`

`unittest.mock` is part of the standard library. It creates test doubles and can
temporarily replace a name used by the code under test.

```python
from unittest.mock import patch

from reporting.delivery import send_report


def test_sends_rendered_report():
    with patch(
        "reporting.delivery.email_client.send",
        autospec=True,
    ) as send:
        send_report("finance@example.com")

    send.assert_called_once()
```

Patch where the code looks up the name, which is not always where the dependency was
originally defined. `autospec=True` gives the mock a signature derived from the real
object and catches some invalid calls.

### Test across isolated environments with tox

tox creates isolated environments, installs the project and declared dependencies,
and runs commands for each configured target.

```toml
# tox.toml
env_list = ["py312", "py313"]

[env_run_base]
deps = ["pytest"]
commands = [["python", "-m", "pytest"]]
```

```bash
tox
```

The target interpreters must exist or be provisioned by the surrounding workflow.
Choose targets that match the project's declared support policy rather than copying a
stale environment list.

### Lint with Flake8

Flake8 is a third-party linter that combines several style and error checks. It is not
a complete verifier for every PEP 8 recommendation.

```bash
python -m pip install flake8
flake8 src tests
flake8 --select F401,F841 src tests
flake8 --extend-ignore E203 src tests
```

`# noqa` suppresses a diagnostic on one line. Prefer a specific code and an explanatory
reason:

```python
from reporting.api import exported_name  # noqa: F401 - public re-export
```

Use the narrowest suppression that reflects the intent:

1. Fix the code when the warning identifies a defect.
2. Suppress a specific code on one justified line.
3. Use a specific per-file ignore for generated or special-purpose files.
4. Use project-wide ignores or exclusions only when the rule conflicts with a
   deliberate project convention.

Legacy projects often store tool configuration in `setup.cfg`:

```ini
[flake8]
max-line-length = 88
per-file-ignores =
    src/reporting/__init__.py:F401
```

Use `pyproject.toml` when the selected tool supports it. Configuration location is a
tool capability, not a universal rule.

### Format code and docstrings

Black is a third-party Python formatter:

```bash
python -m pip install black
black src tests
black --check src tests
```

Formatting can move code and comments to satisfy its layout rules. Review the diff,
especially when formatting an established file whose history depends on a small
change.

`docformatter` can format docstring layout:

```bash
python -m pip install docformatter
docformatter --in-place --recursive src
```

Formatting tools do not validate that documentation is accurate. Generated or
reformatted text still needs technical review.

## Timing, profiling, and memory inspection

Measure before optimizing. Timing compares elapsed duration. Profiling attributes work
to functions or lines. Memory tools inspect allocation and retention. A benchmark that
does not resemble the real workload can optimize the wrong behavior.

### Time expressions in IPython or Jupyter

`%timeit` and `%%timeit` are IPython magic commands, not Python syntax. The line form
times one expression; the cell form times a block.

```ipython
import numpy as np

%timeit np.random.rand(1_000)
%timeit -r 2 -n 10 np.random.rand(1_000)
```

`-n` sets the loops per repeat. `-r` sets the number of repeats.

```ipython
%%timeit
numbers = []
for number in range(10):
    numbers.append(number)
```

`-o` returns an IPython `TimeitResult` for further inspection:

```ipython
times = %timeit -o np.random.rand(1_000)
times.timings
times.best
times.worst
```

Compare results produced by the same timing method and environment. IPython namespace
access and automatic loop selection can differ from the standard-library `timeit`
module.

### Find whole-program hotspots

The standard-library `cProfile` profiler records call counts and cumulative execution
time:

```bash
python -m cProfile -s cumulative application.py
```

Use the result to identify functions worth examining rather than line-profiling every
function in advance.

### Profile selected lines

`line_profiler` is a third-party tool. Its IPython extension exposes `%lprun`:

```python
def sum_using_loop(n):
    total = 0
    for number in range(1, n + 1):
        total += number
    return total


def sum_using_formula(n):
    return n * (n + 1) // 2
```

```ipython
%load_ext line_profiler
%lprun -f sum_using_loop sum_using_loop(100_000)
%lprun -f sum_using_formula sum_using_formula(100_000)
```

The formula changes the algorithm from linear work to constant work. Profiling can
show where time goes; it does not decide whether a rewrite preserves correctness,
clarity, and numeric behavior.

### Inspect object size

`sys.getsizeof()` reports memory directly owned by one object plus interpreter
overhead. It does not recursively include objects referenced from a container.

```python
import sys

numbers = list(range(1_000))
shallow_size = sys.getsizeof(numbers)
print(shallow_size)
```

Treat the result as a shallow implementation measurement, not the total memory cost of
the data structure.

### Trace Python allocations

`tracemalloc` is a standard-library tool for tracing Python memory allocations and
comparing snapshots.

```python
import tracemalloc

tracemalloc.start()

before = tracemalloc.take_snapshot()
result = build_report()
after = tracemalloc.take_snapshot()

for statistic in after.compare_to(before, "lineno")[:10]:
    print(statistic)
```

It traces Python-managed allocations, not every byte allocated by native libraries or
the operating system.

### Legacy `memory_profiler` recipe

`memory_profiler` is a third-party project that is no longer actively maintained, but
existing notebooks may still use its `%mprun` IPython magic. The target function must
be defined in an importable source file for line-by-line reporting.

```ipython
from my_package import my_function

%load_ext memory_profiler
%mprun -f my_function my_function(argument)
```

Prefer maintained tools and representative process-level monitoring for new systems.

## Data processing with pandas

pandas is a third-party data-analysis library. A DataFrame has labeled rows and columns,
and many operations align values by those labels. Prefer column-oriented or vectorized
operations over Python row loops when the operation can be expressed that way.

### Iterate over rows only when needed

`iterrows()` yields an index label and a Series for each row:

```python
for index, row in teams_df.iterrows():
    print(index)
    print(row["team"])
```

Because each row becomes a Series, row values can be coerced to a common dtype. Do not
modify the yielded row and expect the DataFrame to change; it may be a copy.

`itertuples()` is generally faster and preserves values more faithfully when row-wise
iteration is unavoidable:

```python
for row in rangers_df.itertuples(index=True):
    print(row.Index, row.year, row.wins)
```

Column names that are invalid Python identifiers can be renamed in returned tuples.
Use positional access or normalize column names when stable attribute names matter.

### Prefer vectorized expressions to row-wise `apply`

`DataFrame.apply(..., axis=1)` calls a function for each row:

```python
def text_playoffs(value):
    return "made playoffs" if value == 1 else "missed playoffs"


textual_playoffs = rays_df.apply(
    lambda row: text_playoffs(row["playoffs"]),
    axis=1,
)
```

For the same "one means made it, everything else means missed it" rule, a vectorized
expression is clearer and usually faster:

```python
textual_playoffs = rays_df["playoffs"].eq(1).map(
    {True: "made playoffs", False: "missed playoffs"}
)
```

`Series.apply()` and row-wise `DataFrame.apply()` remain useful when the function
cannot be expressed through pandas or NumPy operations. They should not be the default
for simple arithmetic or mapping.

### Label-aware arithmetic versus NumPy arrays

pandas aligns Series by index label:

```python
difference = frame["a"] - frame["b"]
```

Convert explicitly when positional NumPy behavior is intended:

```python
difference = (
    frame["a"].to_numpy()
    - frame["b"].to_numpy()
)
```

`to_numpy()` replaces the older habit of relying on `.values`. Conversion removes
labels and can coerce mixed column types to a common NumPy dtype or `object`. The term
"broadcasting" describes NumPy shape rules; it does not describe label alignment.

### Standardize numeric columns

```python
def standardize(series):
    """Return values as sample z-scores."""
    return (series - series.mean()) / series.std()


score_columns = ["year_1_gpa", "year_2_gpa", "year_3_gpa", "year_4_gpa"]

for column in score_columns:
    df[f"{column}_z"] = standardize(df[column])
```

The default `Series.std()` uses sample standard deviation. Specify a different degrees
of freedom only when the statistical definition requires it. A constant column has a
zero standard deviation and produces missing or non-finite results unless handled.

### Parse and flatten JSON

`json.loads()` expects JSON text. A Series may also contain missing values or already
parsed objects, so guard the input:

```python
import json


def parse_json_if_needed(value):
    if isinstance(value, str):
        return json.loads(value)
    return value


df["payload"] = df["payload"].apply(parse_json_if_needed)
```

Inspect a nested Python object normally:

```python
transaction_keys = df.loc[0, "payload"]["transactions"][0].keys()
```

`pandas.json_normalize()` flattens records into columns:

```python
import pandas as pd

records = [
    {
        "name": "Alice",
        "address": {"city": "Chicago", "state": "IL"},
    }
]

flat = pd.json_normalize(records)
```

| `name` | `address.city` | `address.state` |
|---|---|---|
| Alice | Chicago | IL |

### Parse stringified Python literals

If a DataFrame column contains Python literal syntax rather than JSON, parse it with
`ast.literal_eval()` after validating that a string is expected:

```python
import ast

df["cluster"] = df["cluster"].apply(
    lambda value: ast.literal_eval(value)
    if isinstance(value, str)
    else value
)
```

`literal_eval()` avoids arbitrary code execution but can still consume excessive
memory or parser resources on hostile input. Bound input size and do not treat it as a
general untrusted-data parser.

### Read an encoded CSV file

Comma-separated values (CSV) files are text files, so their encoding is part of the
input contract.

```python
import pandas as pd

df = pd.read_csv("data.csv", encoding="utf-8")
```

If UTF-8 decoding fails, determine the source encoding from its producer or metadata.
Encodings such as Latin-1 or Windows-1252 can decode many byte sequences while still
producing incorrect characters, so blindly retrying them can hide corruption.

### Build a nested dictionary by group

```python
profiles_by_group = {
    group_name: dict(
        zip(group["profile_id"], group["profile_name"])
    )
    for group_name, group in groups_df.groupby("group_name")
}
```

This avoids a version-sensitive `groupby.apply()` shape and makes duplicate-key
behavior visible: later values for the same `profile_id` replace earlier ones.

### Canonicalize unordered pairs

If `(A, B)` and `(B, A)` represent the same pair, sort the two values in every row so
the pair has one representation:

```python
import numpy as np

conflict_df[["element_low", "element_high"]] = np.sort(
    conflict_df[["Element1", "Element2"]].to_numpy(),
    axis=1,
)
```

This is positional NumPy sorting. Decide how missing values and mixed types should be
handled before applying it to production data.

## Web APIs and application configuration

An application programming interface (API) is a defined way for one software
component to use another. It can be a function, class, package, operating-system
interface, internal service, or public service. An API does not have to be reachable
from the public internet.

A web API exposes an interface over a network protocol, commonly Hypertext Transfer
Protocol (HTTP). A Uniform Resource Identifier (URI) identifies the requested resource:

```text
client
  |
  | HTTP method + URI + headers + optional body
  v
web application -> validation -> domain operation -> data store
  |
  | status + headers + optional response body
  v
client
```

The client can be a browser, command-line program, server, mobile application, or
another Python process.

### REST constraints

Representational State Transfer (REST) is an architectural style with these
constraints:

| Constraint | Meaning |
|---|---|
| Client-server | User-interface concerns and server data concerns can evolve independently. |
| Stateless | Each request carries the context needed to process it; the server does not depend on a prior request's conversational state. |
| Cacheable | Responses declare whether intermediaries or clients can reuse them. |
| Uniform interface | Resources are addressed and manipulated through consistent interface semantics. |
| Layered system | A client does not need to know whether gateways, caches, or other layers sit between it and the origin service. |
| Code on demand | The server can optionally provide executable code to extend a client. |

REST does not require JSON and is not formally limited to HTTP, although HTTP with
JavaScript Object Notation (JSON) representations is the common web implementation.
REST statelessness does not forbid server-side resource data. It means each request
carries the application-session context needed to process it instead of depending on a
stored conversation from earlier requests. Moving session context to a shared store
can help process scaling, but does not by itself satisfy the REST constraint.

### Resources, methods, and payloads

A URI identifies a resource. Common HTTP method semantics are:

| Method | Typical meaning |
|---|---|
| `GET` | Retrieve a resource representation. |
| `POST` | Submit data for processing or create according to the resource's semantics. |
| `PUT` | Replace the target resource representation. |
| `PATCH` | Partially modify the target resource. |
| `DELETE` | Remove the target resource. |

The same method should have consistent semantics across resources. HTTP defines safe
methods such as `GET` as idempotent, and also defines `PUT` and `DELETE` as idempotent.
Implementations need to preserve those semantics. Retry behavior for operations such
as `POST` often needs an application-level idempotency key. Authentication,
authorization, validation, caching, and error representation remain explicit design
decisions.

JSON is a common request or response payload format:

```json
{
  "customer_id": 42,
  "status": "active"
}
```

A query string follows `?` in a URI. Parameters are separated with `&` and their names
and values must be URL-encoded:

```text
https://api.example.com/customers?status=active&limit=25
```

Query parameters commonly express filtering, sorting, pagination, or optional search
criteria. They should not carry secrets because URLs are frequently logged.

### Develop a Flask service

Flask is a third-party Python web framework.

```bash
python -m pip install flask
flask --app app run --debug
```

```python
# app.py
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok")
```

Flask's built-in server and interactive debugger are for development, not production.
A production deployment uses an appropriate server, process model, timeouts, logging,
and proxy configuration.

### Validate and document APIs with `flask-smorest`

`flask-smorest` is a third-party extension built around Flask, Marshmallow, webargs,
and apispec. Schemas deserialize and validate request data, serialize responses, and
contribute to generated OpenAPI documentation. Central error handling can keep error
responses consistent.

```python
from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields


class CustomerSchema(Schema):
    customer_id = fields.Int(required=True)
    status = fields.Str(required=True)


blueprint = Blueprint(
    "customers",
    __name__,
    url_prefix="/customers",
)

customers = []


@blueprint.route("/")
class Customers(MethodView):
    @blueprint.response(200, CustomerSchema(many=True))
    def get(self):
        return customers

    @blueprint.arguments(CustomerSchema)
    @blueprint.response(201, CustomerSchema)
    def post(self, customer):
        customers.append(customer)
        return customer


app = Flask(__name__)
app.config["API_TITLE"] = "Customer API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
api = Api(app)
api.register_blueprint(blueprint)
```

The in-memory list keeps the example self-contained. A production service needs a
durable store and explicit concurrency behavior.

Generated documentation follows the schemas and route metadata only when the code
keeps them aligned with actual behavior.

### Twelve-factor configuration

The twelve-factor application methodology separates configuration that varies between
deployments from source code. Independent environment variables are a common
interface. Processes should also be stateless, with durable data stored in backing
services.

```python
import os

database_url = os.environ["DATABASE_URL"]
log_level = os.getenv("LOG_LEVEL", "INFO")
```

`python-dotenv` is a third-party local-development convenience that loads key-value
pairs from a file into the process environment:

```bash
python -m pip install python-dotenv
```

```python
from dotenv import load_dotenv

load_dotenv()
```

By default, `load_dotenv()` does not replace environment variables that already exist.
It can load an explicitly selected file, but it does not automatically manage a family
of `.env.development`, `.env.testing`, and `.env.production` files.

Do not commit `.env` files containing secrets. Production secrets should come from the
deployment platform's supported secret-management path, not from a file bundled with
the application.
