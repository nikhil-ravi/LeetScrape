front_matter = {
    "qid": 485,
    "title": "Max Consecutive Ones",
    "titleSlug": "max-consecutive-ones",
    "difficulty": "Easy",
    "tags": ["Array"],
}


# ====================== DO NOT EDIT ABOVE THIS LINE ======================
class Solution:
    """Given a binary array `nums`, return *the maximum number of consecutive* `1`*'s in the array*.



    **Example 1:**

    ```
    Input: nums = [1,1,0,1,1,1]
    Output: 3
    Explanation: The first two digits or the last three digits are consecutive 1s. The maximum number of consecutive 1s is 3.
    ```
    **Example 2:**

    ```
    Input: nums = [1,0,1,1,0,1]
    Output: 2
    ```


    **Constraints:**

    * `1 <= nums.length <= 10^{5}`
    * `nums[i]` is either `0` or `1`.
    """

    def findMaxConsecutiveOnes(self, nums: list[int]) -> int:
        """Find the maximum number of consecutive ones in a given binary array.

        Keeps a count starting at the first encountered `1` and resets the count once a zero is encounterd.  Returns the maximum of such counts.

        Args:
            nums (list[int]): The binary array.

        Returns:
            int: The maximum number of consecutive ones in the array.

        Time Complexity:
            `O(n)`: We iterate through the array.

        Space Complexity:
            `O(1)`: We do not use any more space.
        """
        new_sum = 0
        max_num = 0
        for num in nums:
            if num == 1:
                new_sum += 1
                if new_sum > max_num:
                    max_num = new_sum
                continue
            new_sum = 0
        return max_num

    # If you have multiple solutions, add them all here as methods of the same class.
