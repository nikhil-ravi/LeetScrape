# ExtractSolution

Generate mdx files from solutions

Once you have solved a question, you can generate an mdx file with the solution and the question statement using the `ExtractSolutions` class:

```python
from leetscrape import ExtractSolutions

# Get the question body
solutions = ExtractSolutions(filename="<path-to-solution-file>").extract()
```
This outputs a list of `Solution` objects with the following attributes:

```python
solution.id # Solution ID
solution.code # Solution code
solution.docs # Docstrings associated with the solution
solution.problem_statement # Question body / problem statement
```

Alternatively, you can use the `to_mdx` method to generate the mdx file:

```python
from leetscrape import ExtractSolutions

# Get the question body
ExtractSolutions(filename="<path-to-solution-file>").to_mdx(output_filename="<path-to-output-file>")
```

::: leetscrape.ExtractSolutions
    options:
      show_source: true
      heading_level: 2