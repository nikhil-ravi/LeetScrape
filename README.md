# LeetScrape

[![deploy-docs](https://github.com/nikhil-ravi/LeetScrape/actions/workflows/pytest-and-docs.yml/badge.svg)](https://leetscrape.chowkabhara.com) [![PYPI](https://img.shields.io/pypi/v/leetscrape)](https://pypi.org/project/leetscrape/) [![codecov](https://codecov.io/gh/nikhil-ravi/LeetScrape/branch/main/graph/badge.svg?token=GWOVLPYSUA)](https://codecov.io/gh/nikhil-ravi/LeetScrape)![PyPI - Downloads](https://img.shields.io/pypi/dm/leetscrape)

Introducing the LeetScrape - a powerful and efficient Python package designed to scrape problem statements and basic test cases from LeetCode.com. With this package, you can easily download and save LeetCode problems to your local machine, making it convenient for offline practice and studying. It is perfect for software engineers and students preparing for coding interviews. The package is lightweight, easy to use and can be integrated with other tools and IDEs. With the LeetScrape, you can boost your coding skills and improve your chances of landing your dream job.

Use this package to get the list of Leetcode questions, their topic and company tags, difficulty, question body (including test cases, constraints, hints), and code stubs in any of the available programming languages.

Detailed documentation available [here](https://leetscrape.chowkabhara.com/).

There is also a related Next.js web app to serve the scraped questions and your answers at [leetcode-nextjs](https://github.com/nikhil-ravi/leetscrape-ts). See the [demo](https://scuffedcode.chowkabhara.com/).

## Get Started

### Installation

Start by installing the package from pip or conda:

```bash
# Using pip
pip install leetscrape

# Using conda:
conda install leetscrape

# Using poetry:
poetry add leetscrape
```

### Usage

#### Command Line

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

#### Python API

##### Get the list of problems and their information

```python
from leetscrape import GetQuestionsList

ls = GetQuestionsList()
ls.scrape() # Scrape the list of questions
ls.questions.head() # Get the list of questions
```

|    |   QID | title                                          | titleSlug                                      | difficulty   |   acceptanceRate | paidOnly   | topicTags                              | categorySlug   |
|---:|------:|:-----------------------------------------------|:-----------------------------------------------|:-------------|-----------------:|:-----------|:---------------------------------------|:---------------|
|  0 |     1 | Two Sum                                        | two-sum                                        | Easy         |          51.4225 | False      | array,hash-table                       | algorithms     |
|  1 |     2 | Add Two Numbers                                | add-two-numbers                                | Medium       |          41.9051 | False      | linked-list,math,recursion             | algorithms     |
|  2 |     3 | Longest Substring Without Repeating Characters | longest-substring-without-repeating-characters | Medium       |          34.3169 | False      | hash-table,string,sliding-window       | algorithms     |
|  3 |     4 | Median of Two Sorted Arrays                    | median-of-two-sorted-arrays                    | Hard         |          38.8566 | False      | array,binary-search,divide-and-conquer | algorithms     |
|  4 |     5 | Longest Palindromic Substring                  | longest-palindromic-substring                  | Medium       |          33.4383 | False      | string,dynamic-programming             | algorithms     |

You can export the associated tables to a directory using the `to_csv` method:

```python
ls.to_csv(directory="<dir>")
```
This generates 6 `.csv` files in the current directory:
- `questions.csv` - List of questions with their title, difficulty, acceptance rate, paid status, topic tags, and category.
- `companies.csv` - List of companies with their name, slug, and the questions count.
- `topicsTags.csv` - List of topic tags with their name and slug.
- `categories.csv` - List of categories with their name and slug.
- `questionCategory.csv` - An edgelist of questions and their categories.
- `questionTopics.csv` - An edgelist of questions and their topic tags.

##### Get Question statement and other information

Query individual question's information such as the body, test cases, constraints, hints, code stubs, and company tags using the `GetQuestion` class:

```python
from leetscrape import GetQuestion

# Get the question body
question = GetQuestion(titleSlug="two-sum").scrape()
```

This returns a `Question` object with the following attributes:

```python
question.QID # Question ID
question.title # Question title
question.titleSlug # Question title slug
question.difficulty # Question difficulty
question.Hints # Question hints
question.Companies # Question companies
question.topics # Question topic tags
question.SimilarQuestions # Similar questions ids
question.Code # Code stubs
question.Body # Question body / problem statement
question.isPaidOnly # Whether the question is only available to premium users of Leetcode
```

##### Generate code stubs for a question

```python
from leetscrape import GenerateCodeStub

# Get the question body
fcs = GenerateCodeStub(titleSlug="two-sum")
fcs.generate(directory="<dir>")
```
This generates the following files in the given directory:
- `q_0001_twoSum.py` - Python file with the code stub for the given question with a function named `twoSum`.
- `test_q_0001_twoSum.py` - Python file with the test cases for the given question.

See [examples](./example/solutions/) for examples of the generated code stubs.

##### Generate mdx files from solutions

Once you have solved a question, you can generate an mdx file with the solution and the question statement using the `ExtractSolutions` class:

```python
from leetscrape import ExtractSolutions

# Get the question body
solutions = ExtractSolutions(filename="<path-to-solution-file>").extract()
```
This outputs a list of `Solution` objects with the following attributes:

```python
solution.id # Solution ID
solution.code # Solution code
solution.docs # Docstrings associated with the solution
solution.problem_statement # Question body / problem statement
```

Alternatively, you can use the `to_mdx` method to generate the mdx file:

```python
from leetscrape import ExtractSolutions

# Get the question body
ExtractSolutions(filename="<path-to-solution-file>").to_mdx(output_filename="<path-to-output-file>")
```

### Serving the solutions with [leetscrape-ts](https://github.com/nikhil-ravi/leetscrape-ts)

You can use the [leetscrape-ts](https://github.com/nikhil-ravi/leetscrape-ts) Next.js template to serve the solutions. See the [demo](https://scuffedcode.chowkabhara.com/). Visit the repo for more details. You can generate the project using the `leetscrape ts` command:

```bash
leetscrape ts --out <path-to-output-directory>
```
This will bootstrap the project in the given directory. Follow the instructions in the [README](https://github.com/nikhil-ravi/leetscrape-ts/blob/main/README.md) and create/modify the `.env.local` file. Then, run the following command to generate the mdx files:

```bash
leetscrape solution --out <path-to-output-directory>/src/content/solutions <path-to-your-python-solution-directory>
```

You can then run the project using the following command:

```bash
cd <path-to-output-directory>
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```