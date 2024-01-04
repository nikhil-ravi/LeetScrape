front_matter = [1, 2, 3]


# ====================== DO NOT EDIT ABOVE THIS LINE ======================
class Solution:
    """Given an integer `x`, return `true` *if* `x` *is a* ***palindrome****, and* `false` *otherwise*.



    **Example 1:**

    ```
    Input: x = 121
    Output: true
    Explanation: 121 reads as 121 from left to right and from right to left.
    ```
    **Example 2:**

    ```
    Input: x = -121
    Output: false
    Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
    ```
    **Example 3:**

    ```
    Input: x = 10
    Output: false
    Explanation: Reads 01 from right to left. Therefore it is not a palindrome.
    ```


    **Constraints:**

    * `-2^{31} <= x <= 2^{31} - 1`



    **Follow up:** Could you solve it without converting the integer to a string?"""

    def isPalindrome(self, x: int) -> bool:
        """
        The question asks us to solve this without converting to a string. One way to do it then is to reverse the integer similar to Problem 7 and compare the two results. However, while reversing the integer, we might run into overflow errors.

        Thus, in this method, we only reverse half the digits (say, the latter half) and check if the first half is equal to the reversed second half. To figure out where in the number is the middle digit, we note that we have reversed enough digits when the reversed number is larger than the first half.

        Args:
            x (int): The number that is to be tested for a palindrome.

        Returns:
            bool: True if the number is a palindrome, False otherwise. Negative numbers are not considered as palindromes.

        Time Complexity:
            `O(log10(x))`: In each iteration of our while loop, we are dividing x by 10.

        Space Complexity:
            `O(1)`: We are not using any extra space other than to create the result.
        """
        if x < 0 or (x % 10 == 0 and x != 0):
            return False

        reversed = 0
        while x > reversed:
            reversed = reversed * 10 + x % 10
            x //= 10
        return (x == reversed) | (x == reversed // 10)

    # If you have multiple solutions, add them all here as methods of the same class.
    def isPalindrome_with_str_conversion(self, x: int) -> bool:
        return str(x) == str(x)[::-1]
