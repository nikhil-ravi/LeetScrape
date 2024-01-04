import json

import pytest

from leetscrape import GetQuestion, Question


def get_test_cases(n: int = 8) -> list[str]:
    tc_data = json.load(open("./tests/test_cases.json"))
    tc_cases = [case["titleSlug"] for case in tc_data]
    return tc_cases[:n]


# random_test_cases = ["edit-distance"]


class TestQuestionInfo:
    def test_question_info(self):
        print(
            Question(
                QID=1,
                title="Two Sum",
                titleSlug="two-sum",
                difficulty="Easy",
                Hints=["1.", "2"],
                Companies=["amazon", "google"],
                SimilarQuestions=[2, 3],
            )
        )


@pytest.mark.parametrize("titleSlug", sorted(get_test_cases()))
class TestGetQuestionInfo:
    def test_scrape(self, titleSlug: str):
        print(titleSlug)
        gqi = GetQuestion(titleSlug)
        gqi.scrape()


class TestGetQuestionInfoPaidOnly:
    def test_scrape(self):
        gqi = GetQuestion("max-consecutive-ones-ii")
        gqi.scrape()
