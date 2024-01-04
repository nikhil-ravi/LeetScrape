# GetQuestion

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


::: leetscrape.GetQuestion
    options:
      show_source: true
      heading_level: 2