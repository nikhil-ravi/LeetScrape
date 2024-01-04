import json
import os

import pytest

from leetscrape import GenerateCodeStub


def get_test_cases(n: int = 8) -> list[str]:
    tc_data = json.load(open("./tests/test_cases.json"))
    tc_cases = [case["titleSlug"] for case in tc_data]
    return tc_cases[:n]


@pytest.mark.parametrize("titleSlug", sorted(get_test_cases()))
class TestGenerateCodeStub:
    def test_generate(self, titleSlug: str):
        print(titleSlug)
        gqi = GenerateCodeStub(titleSlug=titleSlug)
        gqi.generate(testing=True)


class TestGenerateCodeStubIllegalTitleSlug:
    def test_generate_valid_titleSlug(self):
        gqi = GenerateCodeStub(titleSlug="two-sum")
        gqi.generate()
        os.remove("./q_0001_twoSum.py")
        os.remove("./test_q_0001_twoSum.py")

    def test_generate_valid_qid(self):
        GenerateCodeStub(qid=1)

    def test_generate_illegal_titleSlug(self):
        with pytest.raises(ValueError):
            GenerateCodeStub(titleSlug="no-question-like-this")

    def test_generate_illegal_qid(self):
        with pytest.raises(ValueError):
            GenerateCodeStub(qid=-1)

    def test_generate_qid_titleSlug_mismatch(self):
        with pytest.raises(ValueError):
            GenerateCodeStub(qid=1, titleSlug="string-to-integer-atoi")

    def test_generate_neither_qid_titleSlug_passed(self):
        with pytest.raises(ValueError):
            GenerateCodeStub()
