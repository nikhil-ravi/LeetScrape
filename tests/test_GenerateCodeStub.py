import pytest
import json
from leetscrape.GenerateCodeStub import GenerateCodeStub


def get_test_cases(n: int = 8) -> list[str]:
    tc_data = json.load(open("./tests/test_cases.json"))
    tc_cases = [case["titleSlug"] for case in tc_data]
    return tc_cases[:n]


@pytest.mark.parametrize("titleSlug", sorted(get_test_cases()))
class TestGenerateCodeStub:
    def test_generate_code_stub_and_tests(self, titleSlug: str):
        print(titleSlug)
        gqi = GenerateCodeStub(titleSlug=titleSlug)
        gqi.generate_code_stub_and_tests(test=True)
