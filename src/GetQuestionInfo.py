import requests
import pandas as pd
import json
import time

BASE_URL = "https://leetcode.com/graphql"

class GetQuestionInfo:
    def __init__(self, titleSlug: str, questions_info_path: str = "../example/data/questions.csv"):
        self.titleSlug = titleSlug        
        self.questions_info = pd.read_csv(questions_info_path, usecols=["QID", "titleSlug"], index_col="titleSlug")

    def scrape(self):
        data = {
            "query": """query questionHints($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    hints
                    companyTags {
                        name
                        slug
                        imgUrl
                    }
                    similarQuestions
                    codeSnippets {
                        lang
                        langSlug
                        code
                    }
                    content
                }
            }
        """,
            "variables": {"titleSlug": self.titleSlug},
        }
        req = requests.post(BASE_URL, json=data)
        if req.status_code == 404:
            raise ValueError(self.titleSlug)
        while req.status_code == 429:
            time.sleep(10)
            req = requests.post(BASE_URL, json=data)
            if req.status_code == 404:
                raise ValueError(self.titleSlug)
        self.req = req.json()
        return {
            "QID": self.questions_info.loc[self.titleSlug].QID, 
            "titleSlug": self.titleSlug,
            "Hints": self.req["data"]["question"]["hints"],
            "Companies": self.req["data"]["question"]["companyTags"],
            "SimilarQuestions": self.get_similar_questions(),
            "Code": self.get_code_snippet(),
            "Body": self.req["data"]["question"]["content"],
        }
    
    # Similar questions
    def get_similar_questions(self) -> list[str]:
        similar_questions = []
        for qs in json.loads(self.req["data"]["question"]["similarQuestions"]):
            similar_questions.append(self.questions_info.loc[qs["titleSlug"]].QID)
        return similar_questions

    # Code Snippet
    def get_code_snippet(self) -> str:
        python_code_snippet = [
            code_snippet
            for code_snippet in self.req["data"]["question"]["codeSnippets"]
            if code_snippet["langSlug"] == "python3"
        ]
        if len(python_code_snippet) > 0:
            return python_code_snippet[0]["code"]
        else:
            return f"class Solution:\n    def {self.titleSlug}(self) -> Any:\n      "

        