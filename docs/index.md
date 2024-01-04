# Welcome to LeetScrape

[![Python application](https://github.com/nikhil-ravi/LeetcodeScraper/actions/workflows/python-app.yml/badge.svg)](https://github.com/nikhil-ravi/LeetcodeScraper/actions/workflows/python-app.yml) [![deploy-docs](https://github.com/nikhil-ravi/LeetScrape/actions/workflows/deploy-docs.yml/badge.svg)](https://leetscrape.chowkabhara.com) [![PYPI](https://img.shields.io/pypi/v/leetscrape)](https://pypi.org/project/leetscrape/) [![codecov](https://codecov.io/gh/nikhil-ravi/LeetScrape/branch/main/graph/badge.svg?token=GWOVLPYSUA)](https://codecov.io/gh/nikhil-ravi/LeetScrape)![PyPI - Downloads](https://img.shields.io/pypi/dm/leetscrape)

Introducing the LeetScrape - a powerful and efficient Python package designed to scrape problem statements and basic test cases from LeetCode.com. With this package, you can easily download and save LeetCode problems to your local machine, making it convenient for offline practice and studying. It is perfect for software engineers and students preparing for coding interviews. The package is lightweight, easy to use and can be integrated with other tools and IDEs. With the LeetScrape, you can boost your coding skills and improve your chances of landing your dream job.

Use this package to get the list of Leetcode questions, their topic and company tags, difficulty, question body (including test cases, constraints, hints), and code stubs in any of the available programming languages.

## Installation

Start by installing the package from pip or conda:
```bash
pip install leetscrape
# or using conda:
conda install leetscrape
# or using poetry:
poetry add leetscrape
```

## Commands

* `leetscrape question [--out OUT] qid [qid ...]` - Generate a code stub for the given question(s).
* `leetscrape list [--out OUT]` - List all questions without generating code stub.
* `leetscrape solution [-h] [--out OUT] input` - Generate mdx files from solutions.
* `leetscrape ts [--out OUT]` - Create the leetscrape-ts Next.js project to host the solutions.