# Leetcode Questions Scraper

This package may be used to get the list of Leetcode questions and their topic and company tags, difficulty, question body (including test cases, constraints, hints), and code stubs in any of the available programming languages.

## Usage

---

Import the relevant classes from the [`leetcode`](/src/leetcode/) package:

```python
from leetcode.GetQuestionsList import GetQuestionsList
from leetcode.GetQuestionInfo import GetQuestionInfo
from leetcode.utils import combine_list_and_info, get_all_questions_body
import pandas as pd
from tqdm import tqdm
import pickle
import numpy as np
```

Get the list of questions, companies, topic tags, categories using the [`GetQuestionsList`](/src/leetcode/GetQuestionsList.py) class:

```python
ls = GetQuestionsList()
ls.scrape()
ls.questions["QID"] = ls.questions["QID"].astype(int)
ls.to_csv(directory_path="../data/") # example directory path
```

> **Warning**
> The default ALL_JSON_URL in the [`GetQuestionsList`](/src/leetcode/GetQuestionsList.py) class might be out-of-date. Please update it by going to https://leetcode.com/problemset/all/ and exploring the Networks tab for a query returning all.json.

Query individual question's information such as the body, test cases, constraints, hints, code stubs, and company tags using the [`GetQuestionInfo`](/src/leetcode/GetQuestionInfo.py) class:

```python
questions_info = pd.read_csv("../data/questions.csv")
questions_info = pd.read_csv("../data/questions.csv")
questions_info_list = get_all_questions_body(
    questions_info["titleSlug"].tolist(),
    questions_info["paidOnly"].tolist(),
    filename="../data/questionBody.pickle",
)
```

The above code stub is time consuming (10+ minutes) since there are 2500+ questions.

```python
# with open(
#     "../data/questionBody.pickle", "rb"
# ) as f:
    # questions_info_list = pickle.load(f)
questions_body = pd.DataFrame(
    questions_info_list
).drop(columns=["titleSlug"])
questions_body["QID"] = questions_body["QID"].astype(int)
```

Create a new dataframe with all the questions and their metadata and body information.

```python
questions = combine_list_and_info(info_df = questions_body, list_df=ls.questions)
```

Create a PostgreSQL database using the [SQL](/sql/create.sql) dump and insert data using `sqlalchemy`.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

config = dotenv_values("../.env")
engine = create_engine(
    f"postgresql://{config['SUPABASE_USERNAME']}:{config['SUPABASE_PASSWORD']}@{config['SUPABASE_HOSTNAME']}:{config['SUPABASE_PORT']}/{config['SUPABASE_DBNAME']}",
    echo=True,
)
questions.to_sql(
    con=engine, name="questions", if_exists="append", index=False
)
ls.topicTags.to_sql(
    con=engine, name="topic_tags", if_exists="append", index=False
)
ls.categories.to_sql(
    con=engine, name="categories", if_exists="append", index=False
)
ls.companies.to_sql(
    con=engine, name="companies", if_exists="append", index=False
)
ls.questionTopics.to_sql(
    con=engine, name="question_topics", if_exists="append", index=True, index_label="id"
)
ls.questionCategory.to_sql(
    con=engine,
    name="question_category",
    if_exists="append",
    index=True,
    index_label="id",
)
```

Using the `queried_questions_list` PostgreSQL function (defined in the SQL dump) to query for questions containy query terms:

```sql
select * from queried_questions_list('<query term>');
```

Using the `all_questions_list` PostgreSQL function (defined in the SQL dump) to query for all the questions in the database:

```sql
select * from all_questions_list();
```
