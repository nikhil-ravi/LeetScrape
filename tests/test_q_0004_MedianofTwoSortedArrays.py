import pytest
from questions.q_0004_MedianofTwoSortedArrays import Solution


@pytest.mark.parametrize(
    "nums1, nums2, output",
    [
        ([1, 3], [2], 2.00000),
        ([1, 2], [3, 4], 2.50000),
        ([], [1], 1),
        ([], [2, 3], 2.5),
    ],
)
class TestSolution:
    def test_findMedianSortedArrays(
        self, nums1: list[int], nums2: list[int], output: float
    ):
        sc = Solution()
        assert (
            sc.findMedianSortedArrays(
                nums1,
                nums2,
            )
            == output
        )

    def test_findMedianSortedArrays_binary_search(
        self, nums1: list[int], nums2: list[int], output: float
    ):
        sc = Solution()
        assert (
            sc.findMedianSortedArrays_binary_search(
                nums1,
                nums2,
            )
            == output
        )
