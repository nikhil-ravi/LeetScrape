import requests
import pandas as pd
from ._constants import CATEGORIES, TOPIC_TAGS

## This will need replacing since Leetcode seems to change it everyday (?)

ALL_JSON_URL = (
    "https://leetcode.com/_next/data/qXCWR3-qAAkAx8vGwcmGo/problemset/all.json?slug=all"
)


class GetQuestionsList:
    def __init__(self, limit: int = 10000, all_json_url: str = ALL_JSON_URL):
        self.limit = limit
        self.all_json_url = all_json_url
        print(
            "Note: The default ALL_JSON_URL might be out-of-date. Please update it by going to https://leetcode.com/problemset/all/ and exploring the Networks tab for a query returning all.json."
        )

    def scrape(self):
        self.scrape_companies()
        self.scrape_questions_list()
        self.extract_question_topics()
        self.get_categories_and_topicTags_lists()
        self.scrape_question_category()
        self.add_category_to_questions_list()

    def get_categories_and_topicTags_lists(self):
        print("Getting Categories ... ", end="")
        # List of problem categories
        self.categories = pd.DataFrame.from_records(CATEGORIES)
        print("Done")
        # List of problem topic tags
        print("Scraping Topic Tags ... ", end="")
        self.topicTags = pd.DataFrame.from_records(TOPIC_TAGS)
        print("Done")

    def scrape_question_category(self):
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

    def scrape_questions_list(self):
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

    def extract_question_topics(self):
        print("Extracting question topics ... ", end="")
        self.questionTopics = (
            self.questions[["QID", "topicTags"]]
            .rename(columns={"topicTags": "tagSlug"})
            .explode("tagSlug", ignore_index=True)
        ).dropna()
        print("Done")

    def scrape_companies(self):
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

    def add_category_to_questions_list(self):
        self.questions["topicTags"] = self.questions["topicTags"].apply(
            lambda w: ",".join(w)
        )
        self.questions = self.questions.join(
            self.questionCategory.set_index("QID"), on="QID"
        )

    def to_csv(self, directory_path: str):
        self.companies.to_csv(directory_path + "companies.csv", index=False)
        self.questions["QID"] = self.questions["QID"].astype(int)
        self.questions.to_csv(directory_path + "questions.csv", index=False)
        self.questionTopics.to_csv(
            directory_path + "questionTopics.csv", index=True, index_label="id"
        )
        self.categories.to_csv(directory_path + "categories.csv", index=False)
        self.topicTags.to_csv(directory_path + "topicTags.csv", index=False)
        self.questionCategory.to_csv(
            directory_path + "questionCategory.csv", index=True, index_label="id"
        )
