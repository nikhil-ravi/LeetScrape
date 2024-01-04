import pytest
from q_1946_largestNumberAfterMutatingSubstring import Solution


@pytest.mark.parametrize(
    "num, change, output",
    [
        ("132", [9, 8, 5, 0, 3, 6, 4, 2, 6, 8], "832"),
        ("021", [9, 4, 3, 5, 7, 2, 1, 9, 0, 6], "934"),
        ("5", [1, 4, 7, 5, 3, 2, 5, 6, 9, 4], "5"),
    ],
)
class TestSolution:
    def test_maximumNumber(self, num: str, change: list[int], output: str):
        sc = Solution()
        assert (
            sc.maximumNumber(
                num,
                change,
            )
            == output
        )
