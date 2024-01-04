import pytest
from q_0485_maxConsecutiveOnes import Solution


@pytest.mark.parametrize(
    "nums, output", [([1, 1, 0, 1, 1, 1], 3), ([1, 0, 1, 1, 0, 1], 2)]
)
class TestSolution:
    def test_findMaxConsecutiveOnes(self, nums: List[int], output: int):
        sc = Solution()
        assert (
            sc.findMaxConsecutiveOnes(
                nums,
            )
            == output
        )
