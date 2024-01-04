import pandas as pd
import requests

from ._constants import CATEGORIES, TOPIC_TAGS


class GetQuestionsList:
    """A class to scrape the list of questions, their topic tags, and company tags.

    Args:
        limit (int, optional): The maximum number of questions to query for from Leetcode's graphql API. Defaults to 10,000.
    """

    def __init__(self, limit: int = 10_000):
        self.limit = limit

    def scrape(self):
        """Scrapes LeetCode data including company tags, questions, question topics,
        and categories.
        """
        self._scrape_companies()
        self._scrape_questions_list()
        self._extract_question_topics()
        self._get_categories_and_topicTags_lists()
        self._scrape_question_category()
        self._add_category_to_questions_list()

    def to_csv(self, directory: str) -> None:
        """A method to export the scraped data into csv files in preparation for
        injection into a database.

        Args:
            directory (str): The directory path to export the scraped data into.
        """
        self.companies.to_csv(directory + "companies.csv", index=False)
        self.questions["QID"] = self.questions["QID"].astype(int)
        self.questions.to_csv(directory + "questions.csv", index=False)
        self.questionTopics.to_csv(
            directory + "questionTopics.csv", index=True, index_label="id"
        )
        self.categories.to_csv(directory + "categories.csv", index=False)
        self.topicTags.to_csv(directory + "topicTags.csv", index=False)
        self.questionCategory.to_csv(
            directory + "questionCategory.csv", index=True, index_label="id"
        )

    def _scrape_companies(self):
        """Scrape the company tags of each question. This always returns an empty
        dataframe as this is a paid only feature."""
        print("Scraping companies ... ", end="")
        data = {
            "query": """query questionCompanyTags {
                    companyTags {
                        name
                        slug
                        questionCount
                    }
                }
            """,
            "variables": {},
        }
        r = requests.post("https://leetcode.com/graphql", json=data).json()
        self.companies = pd.json_normalize(r["data"]["companyTags"])
        print("Done")

    def _scrape_questions_list(self):
        """
        Scrapes the list of questions from leetcode.com and store them in the 'questions' dataframe. The columns include the question QID, acceptance rate, difficulty, title, titleSlug, and topic tags. It also has a column indicating whether the question is available only to Leetcode's paying customers.
        """
        print("Scraping questions list ... ", end="")
        data = {
            "query": """query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                    problemsetQuestionList: questionList(
                        categorySlug: $categorySlug
                        limit: $limit
                        skip: $skip
                        filters: $filters
                    ) {
                        total: totalNum
                        questions: data {
                            acceptanceRate: acRate
                            difficulty
                            QID: questionFrontendId
                            paidOnly: isPaidOnly
                            title
                            titleSlug
                            topicTags {
                                slug
                            }
                        }
                    }
                }
            """,
            "variables": {
                "categorySlug": "",
                "skip": 0,
                "limit": self.limit,
                "filters": {},
            },
        }

        r = requests.post("https://leetcode.com/graphql", json=data).json()
        self.questions = pd.json_normalize(
            r["data"]["problemsetQuestionList"]["questions"]
        )[
            [
                "QID",
                "title",
                "titleSlug",
                "difficulty",
                "acceptanceRate",
                "paidOnly",
                "topicTags",
            ]
        ]
        self.questions["topicTags"] = self.questions["topicTags"].apply(
            lambda w: [tag["slug"] for tag in w]
        )
        print("Done")

    def _extract_question_topics(self):
        """Create a table with the edge list of questions and topic tags."""
        print("Extracting question topics ... ", end="")
        self.questionTopics = (
            self.questions[["QID", "topicTags"]]
            .rename(columns={"topicTags": "tagSlug"})
            .explode("tagSlug", ignore_index=True)
        ).dropna()
        print("Done")

    def _get_categories_and_topicTags_lists(self):
        """Get the categories and topic tags of LeetCode problems and store them in the
        'categories' and 'topicTags' attribute respectively."""
        print("Getting Categories ... ", end="")
        # List of problem categories
        self.categories = pd.DataFrame.from_records(CATEGORIES)
        print("Done")
        # List of problem topic tags
        print("Scraping Topic Tags ... ", end="")
        self.topicTags = pd.DataFrame.from_records(TOPIC_TAGS)
        print("Done")

    def _scrape_question_category(self):
        """Scrape the category of each question and store it in the 'questionCategory' dataframe."""
        print("Extracting question category ... ", end="")
        categories_data = []
        for category in self.categories["slug"].values:
            data = {
                "query": """query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                        problemsetQuestionList: questionList(
                            categorySlug: $categorySlug
                            limit: $limit
                            skip: $skip
                            filters: $filters
                        ) {
                            questions: data {
                                QID: questionFrontendId
                            }
                        }
                    }
                """,
                "variables": {
                    "categorySlug": category,
                    "skip": 0,
                    "limit": self.limit,
                    "filters": {},
                },
            }

            r = requests.post("https://leetcode.com/graphql", json=data).json()
            categories = pd.json_normalize(
                r["data"]["problemsetQuestionList"]["questions"]
            )
            categories["categorySlug"] = category
            categories_data.append(categories)
        self.questionCategory = pd.concat(categories_data, axis=0, ignore_index=True)
        print("Done")

    def _add_category_to_questions_list(self):
        """Adds the `topicTags` column containing the comma-separated string of
        the list of topic tags relevant to the given questions and the `category`
        column that includes the category relevant to the given question"""
        self.questions["topicTags"] = self.questions["topicTags"].apply(
            lambda w: ",".join(w)
        )
        self.questions = self.questions.join(
            self.questionCategory.set_index("QID"), on="QID"
        )
