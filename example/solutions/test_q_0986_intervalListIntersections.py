import pytest
from q_0986_intervalListIntersections import Solution


@pytest.mark.parametrize(
    "firstList, secondList, output",
    [
        (
            [[0, 2], [5, 10], [13, 23], [24, 25]],
            [[1, 5], [8, 12], [15, 24], [25, 26]],
            [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]],
        ),
        ([[1, 3], [5, 9]], [], []),
    ],
)
class TestSolution:
    def test_intervalIntersection(
        self,
        firstList: list[list[int]],
        secondList: list[list[int]],
        output: list[list[int]],
    ):
        sc = Solution()
        assert (
            sc.intervalIntersection(
                firstList,
                secondList,
            )
            == output
        )
