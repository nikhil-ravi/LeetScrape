import pytest
from questions.q_0001_TwoSum import Solution


@pytest.mark.parametrize(
    "nums, target, output",
    [([2, 7, 11, 15], 9, [0, 1]), ([3, 2, 4], 6, [1, 2]), ([3, 3], 6, [0, 1])],
)
class TestSolution:
    def test_twoSum_bruteforce(self, nums: list[int], target: int, output: list[int]):
        sc = Solution()
        assert (
            sc.twoSum_bruteforce(
                nums,
                target,
            )
            == output
        )

    def test_twoSum(self, nums: list[int], target: int, output: list[int]):
        sc = Solution()
        assert (
            sc.twoSum(
                nums,
                target,
            )
            == output
        )
