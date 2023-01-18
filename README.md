# LeetScrape

[![Python application](https://github.com/nikhil-ravi/LeetcodeScraper/actions/workflows/python-app.yml/badge.svg)](https://github.com/nikhil-ravi/LeetcodeScraper/actions/workflows/python-app.yml) [![deploy-docs](https://github.com/nikhil-ravi/LeetScrape/actions/workflows/deploy-docs.yml/badge.svg)](https://leetscrape.chowkabhara.com) [![PYPI](https://img.shields.io/pypi/v/leetscrape)](https://pypi.org/project/leetscrape/)

Introducing the LeetScrape - a powerful and efficient Python package designed to scrape problem statements and basic test cases from LeetCode.com. With this package, you can easily download and save LeetCode problems to your local machine, making it convenient for offline practice and studying. It is perfect for software engineers and students preparing for coding interviews. The package is lightweight, easy to use and can be integrated with other tools and IDEs. With the LeetScrape, you can boost your coding skills and improve your chances of landing your dream job.

Use this package to get the list of Leetcode questions, their topic and company tags, difficulty, question body (including test cases, constraints, hints), and code stubs in any of the available programming languages.

Detailed documentation available [here](https://leetscrape.chowkabhara.com/).

## Installation

Start by installing the package from pip or conda:
```bash
pip install leetscrape
# or using conda:
conda install leetscrape
# or using poetry:
poetry add leetscrape
```


## Usage

### Command Line
Run the `leetscrape` command to get a code stub and a pytest test file for a given Leetcode question:
```bash
$ leetscrape --titleSlug two-sum --qid 1
```
At least one of the two arguments is required.
- `titleSlug` is the slug of the leetcode question that is in the url of the question, and
- `qid` is the number associated with the question.

### Other classes

Import the relevant classes from the package:

```python
from leetscrape.GetQuestionsList import GetQuestionsList
from leetscrape.GetQuestionInfo import GetQuestionInfo
from leetscrape.utils import combine_list_and_info, get_all_questions_body
```

### Scrape the list of problems
Get the list of questions, companies, topic tags, categories using the [`GetQuestionsList`](/GetQuestionsList/#getquestionslist) class:

```python
ls = GetQuestionsList()
ls.scrape() # Scrape the list of questions
ls.to_csv(directory_path="../data/") # Save the scraped tables to a directory
```

### Get Question statement and other information
Query individual question's information such as the body, test cases, constraints, hints, code stubs, and company tags using the [`GetQuestionInfo`](/GetQuestionsList/#getquestionslist) class:

```python
# This table can be generated using the previous commnd
questions_info = pd.read_csv("../data/questions.csv")

# Scrape question body
questions_body_list = get_all_questions_body(
    questions_info["titleSlug"].tolist(),
    questions_info["paidOnly"].tolist(),
    save_to="../data/questionBody.pickle",
)

# Save to a pandas dataframe
questions_body = pd.DataFrame(
    questions_body_list
).drop(columns=["titleSlug"])
questions_body["QID"] = questions_body["QID"].astype(int)
```

> **Note**
> The above code stub is time consuming (10+ minutes) since there are 2500+ questions.

Create a new dataframe with all the questions and their metadata and body information.

```python
questions = combine_list_and_info(
    info_df = questions_body, list_df=ls.questions, save_to="../data/all.json"
)
```

### Upload scraped data to a Database
Create a PostgreSQL database using the [SQL](https://github.com/nikhil-ravi/LeetScrape/blob/dcabdd8bd11b03aac0b725c0adc4881b9be9a48f/example/sql/create.sql) dump and insert data using `sqlalchemy`.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("<database_connection_string>", echo=True)
questions.to_sql(con=engine, name="questions", if_exists="append", index=False)
# Repeat the same for tables ls.topicTags, ls.categories,
# ls.companies, # ls.questionTopics, and ls.questionCategory
```

Use the [`queried_questions_list`](https://github.com/nikhil-ravi/LeetScrape/blob/dcabdd8bd11b03aac0b725c0adc4881b9be9a48f/example/sql/create.sql#L228-L240) PostgreSQL function (defined in the SQL dump) to query for questions containy query terms:

```sql
select * from queried_questions_list('<query term>');
```

Use the [`all_questions_list`](https://github.com/nikhil-ravi/LeetScrape/blob/dcabdd8bd11b03aac0b725c0adc4881b9be9a48f/example/sql/create.sql#L243-L253) PostgreSQL function (defined in the SQL dump) to query for all the questions in the database:

```sql
select * from all_questions_list();
```

Use the [`get_similar_questions`](https://github.com/nikhil-ravi/LeetScrape/blob/dcabdd8bd11b03aac0b725c0adc4881b9be9a48f/example/sql/create.sql#L255-L270) PostgreSQL function (defined in the SQL dump) to query for all questions similar to a given question:

```sql
select * from get_similar_questions(<QuestionID>);
```


### Extract solutions from a `.py` file

You may want to extract solutions from a `.py` files to upload them to a database. You can do so using the [`ExtractSolutions`](/src/leetscrape/ExtractSolutions.py) class.
```python
from leetscrape.ExtractSolutions import extract
# Returns a dict of the form {QuestionID: solutions}
solutions = extract(filename=<path_to_python_script>)
```

Use the [`upload_solutions`](/utils/#leetscrape.utils.upload_solutions) method to upload the extracted solution code stubs from your python script to the PosgreSQL database.

```python
from leetscrape.ExtractSolutions import upload_solutions
upload_solutions(engine=<sqlalchemy_engine>, row_id = <row_id_in_table>, solutions: <solutions_dict>)
```
