# GenerateCodeStubs

Generate code stubs for a question

```python
from leetscrape import GenerateCodeStub

# Get the question body
fcs = GenerateCodeStub(titleSlug="two-sum")
fcs.generate(directory="<dir>")
```
This generates the following files in the given directory:
- `q_0001_twoSum.py` - Python file with the code stub for the given question with a function named `twoSum`.
- `test_q_0001_twoSum.py` - Python file with the test cases for the given question.

See [examples](https://github.com/nikhil-ravi/LeetScrape/tree/main/example/solutions) for examples of the generated code stubs.

::: leetscrape.GenerateCodeStub
    options:
      show_source: true
      heading_level: 2