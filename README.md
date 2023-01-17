# Leetcode Questions Scraper

[![Python application](https://github.com/nikhil-ravi/LeetcodeScraper/actions/workflows/python-app.yml/badge.svg)](https://github.com/nikhil-ravi/LeetcodeScraper/actions/workflows/python-app.yml)

Introducing the LeetScrape - a powerful and efficient Python package designed to scrape problem statements and basic test cases from LeetCode.com. With this package, you can easily download and save LeetCode problems to your local machine, making it convenient for offline practice and studying. It is perfect for software engineers and students preparing for coding interviews. The package is lightweight, easy to use and can be integrated with other tools and IDEs. With the LeetScrape, you can boost your coding skills and improve your chances of landing your dream job.

Use this package to get the list of Leetcode questions, their topic and company tags, difficulty, question body (including test cases, constraints, hints), and code stubs in any of the available programming languages.

## Usage

Import the relevant classes from the [`leetcode`](/src/leetcode/) package:

```python
from leetscrape.GetQuestionsList import GetQuestionsList
from leetscrape.GetQuestionInfo import GetQuestionInfo
from leetscrape.utils import combine_list_and_info, get_all_questions_body
```

Get the list of questions, companies, topic tags, categories using the [`GetQuestionsList`](/src/leetcode/GetQuestionsList.py) class:

```python
ls = GetQuestionsList()
ls.scrape() # Scrape the list of questions
ls.to_csv(directory_path="../data/") # Save the scraped tables to a directory
```

> **Warning**
> The default ALL_JSON_URL in the [`GetQuestionsList`](/src/leetcode/GetQuestionsList.py) class might be out-of-date. Please update it by going to https://leetcode.com/problemset/all/ and exploring the Networks tab for a query returning all.json.

Query individual question's information such as the body, test cases, constraints, hints, code stubs, and company tags using the [`GetQuestionInfo`](/src/leetcode/GetQuestionInfo.py) class:

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

Create a PostgreSQL database using the [SQL](/example/sql/create.sql) dump and insert data using `sqlalchemy`.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("<database_connection_string>", echo=True)
questions.to_sql(con=engine, name="questions", if_exists="append", index=False)
# Repeat the same for tables ls.topicTags, ls.categories,
# ls.companies, # ls.questionTopics, and ls.questionCategory
```

Use the `queried_questions_list` PostgreSQL function (defined in the SQL dump) to query for questions containy query terms:

```sql
select * from queried_questions_list('<query term>');
```

Use the `all_questions_list` PostgreSQL function (defined in the SQL dump) to query for all the questions in the database:

```sql
select * from all_questions_list();
```

Use the `get_similar_questions` PostgreSQL function (defined in the SQL dump) to query for all questions similar to a given question:

```sql
select * from get_similar_questions(<QuestionID>);
```

Use the [`extract_solutions`](/src/leetcode/utils.py:) method to extract solution code stubs from your python script. Note that the solution method should be a part of a class named `Solution` (see [here](/example/solutions/q_0001_TwoSum.py) for an example):

```python
# Returns a dict of the form {QuestionID: solutions}
solutions = extract_solutions(filename=<path_to_python_script>)
```

Use the [`upload_solutions`](/src/leetcode/utils.py:) method to upload the extracted solution code stubs from your python script to the PosgreSQL database.

```python
upload_solutions(engine=<sqlalchemy_engine>, row_id = <row_id_in_table>, solutions: <solutions_dict>)
```
