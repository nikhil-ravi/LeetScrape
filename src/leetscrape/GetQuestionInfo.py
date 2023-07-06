import warnings
import requests
import pandas as pd
import json
import time
from pydantic.dataclasses import dataclass
from pydantic import Field
import pypandoc

from .helper import camel_case


# Leetcode's graphql api endpoint
BASE_URL = "https://leetcode.com/graphql"


@dataclass
class QuestionInfo:
    QID: int
    titleSlug: str
    Hints: list[str] = Field(default_factory=list)
    Companies: list[str] | None = None
    SimilarQuestions: list[int] = Field(default_factory=list)
    Code: str = Field(default_factory=str)
    Body: str = Field(default_factory=str)
    isPaidOnly: bool = False

    def __repr__(self) -> str:
        repr = f"{self.QID}. {self.titleSlug}\n"
        repr += pypandoc.convert_text(self.Body, "md", "html")
        if len(self.Hints) > 1:
            repr += "Hints:\n"
            for idx, hint in enumerate(self.Hints):
                repr += f"    {idx}. {hint}\n"
        if self.Companies is not None:
            repr += f"Companies: {self.Companies}\n"
        if len(self.SimilarQuestions) > 0:
            repr += f"SimilarQuestions: {self.SimilarQuestions}\n"
        return repr


class GetQuestionInfo:
    """
    A class to acquire the statement, constraints, hints, basic test cases, related questions, and code stubs of the given question.

    Args:
        titleSlug (str): The title slug of the question.
    """

    def __init__(self, titleSlug: str):
        self.titleSlug = titleSlug
        self.questions_info = self.fetch_questions_stub_id()

    def fetch_questions_stub_id(self):
        endpoint_url = "https://leetcode.com/api/problems/{endpoint}/"
        # endpoints = [
        #     "algorithms",
        #     "database",
        #     "shell",
        #     "concurrency",
        #     "javascript",
        # ]
        endpoints = ["all"]  # returns all questions
        question_data = []

        for endpoint in endpoints:
            req = requests.get(endpoint_url.format(endpoint=endpoint)).json()
            question_data.append(
                pd.json_normalize(req["stat_status_pairs"]).rename(
                    columns={
                        "stat.frontend_question_id": "QID",
                        "stat.question__title_slug": "titleSlug",
                    }
                )[["QID", "titleSlug"]]
            )

        return pd.concat(question_data).sort_values("QID").set_index("titleSlug")

    def scrape(self) -> QuestionInfo:
        """This method calls the Leetcode graphql api to query for the hints, companyTags (currently returning null as this is a premium feature), code snippets, and content of the question.

        Raises:
            ValueError: When the connection to Leetcode's graphql api is not established.

        Returns:
            QuestionInfo: Contains the QID, titleSlug, Hints, Companies, Similar Questions, Code stubs, and the body of the question.
        """
        data = {
            "query": """query questionHints($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    questionFrontendId
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
                    isPaidOnly
                }
            }
        """,
            "variables": {"titleSlug": self.titleSlug},
        }
        req = requests.post(BASE_URL, json=data)
        if req.status_code == 404:
            raise ValueError("Leetcode's graphql API can't be found.")
        while req.status_code == 429 | 400:
            time.sleep(10)
            req = requests.post(BASE_URL, json=data)
            if req.status_code == 404:
                raise ValueError("Leetcode's graphql API can't be found.")
        self.req = req.json()
        return QuestionInfo(
            QID=self.req["data"]["question"]["questionFrontendId"],
            titleSlug=self.titleSlug,
            Hints=self.req["data"]["question"]["hints"],
            Companies=self.req["data"]["question"]["companyTags"],
            SimilarQuestions=self.get_similar_questions(),
            Code=self.get_code_snippet(),
            Body=self.get_question_body(),
            isPaidOnly=self.req["data"]["question"]["isPaidOnly"],
        )

    def get_question_body(self) -> str:  # type: ignore
        if not self.req["data"]["question"]["isPaidOnly"]:
            return self.req["data"]["question"]["content"]
        else:
            warnings.warn("This questions is only for paid Leetcode subscribers.")
            return "This questions is only for paid Leetcode subscribers."

    # Similar questions
    def get_similar_questions(self) -> list[int]:
        """A helper method to extract the list of similar questions of the
        given question.

        Returns:
            list[int]: The list of QIDs of the questions similar to the given question.
        """
        similar_questions = []
        for qs in json.loads(self.req["data"]["question"]["similarQuestions"]):
            similar_questions.append(self.questions_info.loc[qs["titleSlug"]].QID)
        return similar_questions

    # Code Snippet
    def get_code_snippet(self) -> str:  # type: ignore
        """A helper method to extract the code snippets from the query response.
        Currently, this method returns the Python3 code snippet if available,
        else it returns a barebones Python3 code snippet with the class name and
        method named after the titleSlug.

        Returns:
            str: Python3 code snippet
        """
        if not self.req["data"]["question"]["isPaidOnly"]:
            python_code_snippet = [
                code_snippet
                for code_snippet in self.req["data"]["question"]["codeSnippets"]
                if code_snippet["langSlug"] == "python3"
            ]
            if len(python_code_snippet) > 0:
                return python_code_snippet[0]["code"]
            else:
                return f"# This question has no Python code stub.\n# Generating a generic Python code stub\nclass Solution:\n    def {camel_case(self.titleSlug)}(self) -> Any:\n      "
        else:
            warnings.warn("This questions is only for paid Leetcode subscribers.")
            return f"# This questions is only for paid Leetcode subscribers.\n# Generating a generic Python code stub\nclass Solution:\n    def {camel_case(self.titleSlug)}(self) -> Any:\n      "
