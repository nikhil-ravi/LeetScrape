from leetscrape.GetQuestionInfo import GetQuestionInfo
import pytest
import json


def get_test_cases(n: int = 8) -> list[str]:
    tc_data = json.load(open("./tests/test_cases.json"))
    tc_cases = [case["titleSlug"] for case in tc_data]
    return tc_cases[:n]


# random_test_cases = ["edit-distance"]


@pytest.mark.parametrize("titleSlug", sorted(get_test_cases()))
class TestGetQuestionInfo:
    def test_scrape(self, titleSlug: str):
        print(titleSlug)
        gqi = GetQuestionInfo(titleSlug)
        gqi.scrape()
