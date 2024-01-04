import ast
import os

import pytest

from leetscrape import ExtractSolutions


def test_extract_solutions():
    # Create an instance of ExtractSolutions
    extractor = ExtractSolutions("./tests/q_0009_palindromeNumber.py")

    # Test extracting solutions
    solutions = extractor.extract()
    assert len(solutions) == 2  # Update with the expected number of solutions
    assert isinstance(solutions[0].id, int)  # Update with the expected type
    assert isinstance(solutions[0].code, str)  # Update with the expected type
    assert isinstance(solutions[0].docs, dict)  # Update with the expected type
    assert isinstance(
        solutions[0].problem_statement, str
    )  # Update with the expected type


def test_to_mdx():
    # Create an instance of ExtractSolutions
    extractor = ExtractSolutions("./tests/q_0009_palindromeNumber.py")

    # Test converting to mdx
    mdx = extractor.to_mdx()
    assert isinstance(mdx, str)  # Update with the expected type


def test_to_mdx_with_filename():
    # Create an instance of ExtractSolutions
    extractor = ExtractSolutions("./tests/q_0009_palindromeNumber.py")

    # Test converting to mdx with filename
    extractor.to_mdx(filename="./tests/q_0009_palindromeNumber.mdx")
    # Add more assertions for the specific file path
    os.remove("./tests/q_0009_palindromeNumber.mdx")


def test_extract_front_matter():
    # Create an instance of ExtractSolutions
    extractor = ExtractSolutions("./tests/q_0009_palindromeNumber.py")

    # Test extracting front matter
    front_matter = extractor._extract_front_matter()
    assert isinstance(front_matter, dict)  # Update with the expected type
    # Add more assertions for the specific keys and values in the front matter dictionary


# Add more test cases as needed
def test_extract_with_custom_top_class_name():
    with pytest.raises(ValueError):
        # Create an instance of ExtractSolutions
        extractor = ExtractSolutions(
            "./tests/q_0009_palindromeNumber.py",
        )

        # Test extracting solutions with custom top class name
        solutions = extractor.extract(
            top_class_name="CustomSolution",
        )


def test_extract_code_with_invalid_node():
    # Create an instance of ExtractSolutions
    extractor = ExtractSolutions("./tests/q_0009_palindromeNumber.py")

    # Create an invalid node for testing
    node = ast.AsyncFunctionDef(
        name="test_function",
        args=ast.arguments(),
        body=[],
        lineno=None,
        end_lineno=None,
    )

    # Test extracting code with invalid node
    with pytest.raises(ValueError):
        code = extractor._extract_code(node)
        # Add more assertions or error messages for the specific error case


def test_non_dict_front_matter():
    with pytest.raises(ValueError):
        # Create an instance of ExtractSolutions
        extractor = ExtractSolutions(
            "./tests/q_0009_palindromeNumber_wo_frontmatter.py"
        )
        extractor.to_mdx()
