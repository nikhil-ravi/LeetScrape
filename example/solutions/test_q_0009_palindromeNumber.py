import pytest
from q_0009_palindromeNumber import Solution


@pytest.mark.parametrize("x, output", [(121, True), (-121, False), (10, False)])
class TestSolution:
    def test_isPalindrome(self, x: int, output: bool):
        sc = Solution()
        assert (
            sc.isPalindrome(
                x,
            )
            == output
        )
