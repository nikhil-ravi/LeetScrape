# GetQuestionsList

Get the list of problems and their information

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

::: leetscrape.GetQuestionsList
    options:
      show_source: true
      heading_level: 2