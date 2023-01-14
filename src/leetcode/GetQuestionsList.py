import requests
import pandas as pd


class GetQuestionsList:
    def __init__(self, limit: int = 10000):
        self.limit = limit

    def scrape(self):
        self.scrape_companies()
        self.scrape_questions_list()
        self.extract_question_topics()
        self.scrape_categories_and_topicTags_lists()
        self.scrape_question_category()
        self.add_category_to_questions_list()

    def scrape_categories_and_topicTags_lists(self):
        print("Scraping Categories ... ", end="")
        data = requests.get("https://leetcode.com/_next/data/ZLa6ykIj3i3BfoQNxcfl8/problemset/all.json").json()
        # List of problem categories
        self.categories = pd.json_normalize(data["pageProps"]["problemsetCategories"]).rename(
            columns={"title": "name", "titleSlug": "slug"}
        )[["slug", "name"]]
        print("Done")
        # List of problem topic tags
        print("Scraping Topic Tags ... ", end="")
        self.topicTags = pd.json_normalize(data["pageProps"]["topicTags"]).drop(
            columns=["id", "translatedName", "questionCount"]
        )[["slug", "name"]]
        print("Done")

    def scrape_question_category(self):
        print("Extracting question category ... ", end="")
        categories_data = []
        for category in self.categories["slug"].values:
            data = {
                "query": "\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    questions: data {\n      QID: questionFrontendId\n    }\n  }\n}\n    ",
                "variables": {"categorySlug": category, "skip": 0, "limit": self.limit, "filters": {}},
            }

            r = requests.post("https://leetcode.com/graphql", json=data).json()
            categories = pd.json_normalize(r["data"]["problemsetQuestionList"]["questions"])
            categories["categorySlug"] = category
            categories_data.append(categories)
        self.questionCategory = pd.concat(categories_data, axis=0, ignore_index=True)
        print("Done")

    def scrape_questions_list(self):
        print("Scraping questions list ... ", end="")
        data = {
            "query": "\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      acceptanceRate: acRate\n      difficulty\n     QID: questionFrontendId\n      paidOnly: isPaidOnly\n      title\n      titleSlug\n    topicTags {\n        slug\n      }\n    }\n  }\n}\n    ",
            "variables": {"categorySlug": "", "skip": 0, "limit": self.limit, "filters": {}},
        }

        r = requests.post("https://leetcode.com/graphql", json=data).json()
        self.questions = pd.json_normalize(r["data"]["problemsetQuestionList"]["questions"])[
            ["QID", "title", "titleSlug", "difficulty", "acceptanceRate", "paidOnly", "topicTags"]
        ]
        self.questions["topicTags"] = self.questions["topicTags"].apply(lambda w: [tag["slug"] for tag in w])
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
            "query": "\n    query questionCompanyTags {\n  companyTags {\n    name\n    slug\n    questionCount\n  }\n}\n    ",
            "variables": {},
        }
        r = requests.post("https://leetcode.com/graphql", json=data).json()
        self.companies = pd.json_normalize(r["data"]["companyTags"])
        print("Done")

    def add_category_to_questions_list(self):
        self.questions["topicTags"] = self.questions["topicTags"].apply(lambda w: ",".join(w))
        self.questions = self.questions.join(self.questionCategory.set_index("QID"), on="QID")

    def to_csv(self, path: str):
        self.companies.to_csv(path + "companies.csv", index=False)
        self.questions.to_csv(path + "questions.csv", index=False)
        self.questionTopics.to_csv(path + "questionTopics.csv", index=True, index_label="id")
        self.categories.to_csv(path + "categories.csv", index=False)
        self.topicTags.to_csv(path + "topicTags.csv", index=False)
        self.questionCategory.to_csv(path + "questionCategory.csv", index=True, index_label="id")
