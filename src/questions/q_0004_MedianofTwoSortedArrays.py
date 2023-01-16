import sys


class Solution:
    """
    4. Median of Two Sorted Arrays

    Difficulty: Hard

    Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.

    The overall run time complexity should be `O(log (m+n))`.

    Example 1:
    ```
    Input: nums1 = [1,3]; nums2 = [2]
    Output: 2.00000
    Explanation: merged array = [1,2,3] and median is 2.
    ```
    Example 2:
    ```
    Input: nums1 = [1,2]; nums2 = [3,4]
    Output: 2.50000
    Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
    ```
    Example 3:
    ```
    Input: nums1 = []; nums2 = [1]
    Output: 1
    Explanation: merged array = [1] and median is 1.
    ```
    Example 4:
    ```
    Input: nums1 = []; nums2 = [2,3]
    Output: 2.5
    Explanation: merged array = [2,3] and median is (2 + 3) / 2 = 2.5.
    ```

    Constraints:
    - `nums1.length == m`
    - `nums2.length == n`
    - `0 <= m <= 1000`
    - `0 <= n <= 1000`
    - `1 <= m + n <= 2000`
    - `-106 <= nums1[i], nums2[i] <= 106`
    """

    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        m = len(nums1)
        n = len(nums2)
        pointer1 = 0
        pointer2 = 0
        merged_array = []
        median_indices = [(m + n) // 2] if (m + n) % 2 == 1 else [(m + n) // 2 - 1, (m + n) // 2]
        while len(nums1) > 0 or len(nums2) > 0:
            if (len(nums1) > 0 and len(nums2) > 0 and nums1[0] < nums2[0]) or len(nums2) == 0:
                merged_array.append(nums1.pop(0))
                pointer1 += 1
            elif (len(nums1) > 0 and len(nums2) > 0 and nums1[0] >= nums2[0]) or len(nums1) == 0:
                merged_array.append(nums2.pop(0))
                pointer2 += 1
            if len(merged_array) == median_indices[-1] + 1:
                if (m + n) % 2 == 1:
                    return merged_array[median_indices[0]]
                else:
                    return (merged_array[median_indices[0]] + merged_array[median_indices[1]]) / 2

    def findMedianSortedArrays_binary_search(self, nums1: list[int], nums2: list[int]) -> float:
        m = len(nums1)
        n = len(nums2)
        if m > n:
            return self.findMedianSortedArrays_binary_search(nums2, nums1)
        start = 0
        end = m

        while start <= end:
            pointer1 = (start + end) // 2
            pointer2 = (m + n + 1) // 2 - pointer1

            left1_max = nums1[pointer1 - 1] if pointer1 > 0 else -sys.maxsize - 1
            right1_min = nums1[pointer1] if pointer1 < m else sys.maxsize
            left2_max = nums2[pointer2 - 1] if pointer2 > 0 else -sys.maxsize - 1
            right2_min = nums2[pointer2] if pointer2 < n else sys.maxsize

            if left1_max <= right2_min and left2_max <= right1_min:
                if (m + n) % 2 == 1:
                    return max(left1_max, left2_max)
                else:
                    return (max(left1_max, left2_max) + min(right1_min, right2_min)) / 2
            elif left1_max > right2_min:
                end = pointer1 - 1
            elif left2_max > right1_min:
                start = pointer1 + 1
