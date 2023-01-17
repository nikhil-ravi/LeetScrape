import pytest
from questions.q_0003_LongestSubstringWithoutRepeatingCharacters import Solution


@pytest.mark.parametrize("s, output", [("abcabcbb", 3), ("bbbbb", 1), ("pwwkew", 3)])
class TestSolution:
    def test_lengthOfLongestSubstring(self, s: str, output: int):
        sc = Solution()
        assert (
            sc.lengthOfLongestSubstring(
                s,
            )
            == output
        )
