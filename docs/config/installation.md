# Getting Started

## Installation

Start by installing the package from pip or conda:
=== "pip"
    ```bash
    pip install leetscrape
    ```
=== "conda"
    ```bash
    conda install leetscrape
    ```
=== "poetry"
    ```bash
    poetry add leetscrape
    ```

## Commands

* <code>leetscrape <i><b>list</b></i> [--out OUT]</code> - List all questions without generating code stub.

```
options:
-h, --help         show a help message and exit
--out OUT, -o OUT  Specify the output file name to store the list of questions.
```

* <code>leetscrape <i><b>question</b></i> [--out OUT] qid [qid ...]</code> - Generate a code stub for the given question(s).

```
positional arguments:
qid                Enter Leetcode question ID(s)

options:
-h, --help         show this help message and exit
--out OUT, -o OUT  Enter the path to the output directory
```

* <code>leetscrape <i><b>solution</b></i> [-h] [--out OUT] input</code> - Generate mdx files from solutions.

```
positional arguments:
input              Enter the path to the solution directory with solution files or to a single
                    solution file

options:
-h, --help         show this help message and exit
--out OUT, -o OUT  Enter the path to the output directory to save solutions mdx files
```

* <code>leetscrape <i><b>ts</b></i> [--out OUT]</code> - Create the leetscrape-ts Next.js project to host the solutions.

```
options:
-h, --help         show this help message and exit
--out OUT, -o OUT  Enter the path to the output directory to save the project
```