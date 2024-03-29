front_matter = {
    "qid": 1946,
    "title": "Largest Number After Mutating Substring",
    "titleSlug": "largest-number-after-mutating-substring",
    "difficulty": "Medium",
    "tags": ["Array", "String", "Greedy"],
}


# ====================== DO NOT EDIT ABOVE THIS LINE ======================
class Solution:
    """You are given a string `num`, which represents a large integer. You are also given a **0-indexed** integer array `change` of length `10` that maps each digit `0-9` to another digit. More formally, digit `d` maps to digit `change[d]`.

    You may **choose** to **mutate a single substring** of `num`. To mutate a substring, replace each digit `num[i]` with the digit it maps to in `change` (i.e. replace `num[i]` with `change[num[i]]`).

    Return *a string representing the **largest** possible integer after **mutating** (or choosing not to) a **single substring** of* `num`.

    A **substring** is a contiguous sequence of characters within the string.



    **Example 1:**

    ```
    Input: num = "132", change = [9,8,5,0,3,6,4,2,6,8]
    Output: "832"
    Explanation: Replace the substring "1":
    - 1 maps to change[1] = 8.
    Thus, "132" becomes "832".
    "832" is the largest number that can be created, so return it.
    ```
    **Example 2:**

    ```
    Input: num = "021", change = [9,4,3,5,7,2,1,9,0,6]
    Output: "934"
    Explanation: Replace the substring "021":
    - 0 maps to change[0] = 9.
    - 2 maps to change[2] = 3.
    - 1 maps to change[1] = 4.
    Thus, "021" becomes "934".
    "934" is the largest number that can be created, so return it.
    ```
    **Example 3:**

    ```
    Input: num = "5", change = [1,4,7,5,3,2,5,6,9,4]
    Output: "5"
    Explanation: "5" is already the largest number that can be created, so return it.
    ```


    **Constraints:**

    * `1 <= num.length <= 10^{5}`
    * `num` consists of only digits `0-9`.
    * `change.length == 10`
    * `0 <= change[d] <= 9`
    """

    def maximumNumber(self, num: str, change: list[int]) -> str:  # type: ignore
        """Returns a string that is the largest possible integer after mutating a contiguos substring in the given string `num`.

        We notice that a digit at the front has more weight than those that follow it.
        So, starting from the left, we leave the digits unmutated until we a digit that has a mutation that is larger than itself (`d < change[d]`).
        Starting at this digit and going to the right, we mutate the following digits if their mutation is at least as big as themselves (`d <= change[d]`).
        As soon as we encounter a digit whose mutation is smaller than itself, we stop the mutation and continue adding the original digits.

        Args:
            num (str): The string to be mutated.
            change (list[int]): The mutations available.

        Returns:
            str: The largest mutated string.

        Time Complexity:
            `O(n)`: We iterate through the characters in the string of length `n`.

        Space Complexity:
            `O(1)`: We do not use any extra space.
        """
        num: list[str] = list(num)
        change: dict[str, str] = {
            str(i): str(d) for i, d in enumerate(change) if d >= i
        }
        mutating = False
        for i, d in enumerate(num):
            if d in change:
                num[i] = change[d]
                if change[d] > d and not mutating:
                    mutating = True
            elif mutating:
                break
        return "".join(num)

    # If you have multiple solutions, add them all here as methods of the same class.
