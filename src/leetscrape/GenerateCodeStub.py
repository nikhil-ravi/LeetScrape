import re

import marko
import pandas as pd
import pypandoc
import requests
from black import FileMode, format_str

from .models import Question
from .question import GetQuestion
from .utils import camel_case, parse_args


class GenerateCodeStub:
    """Class to generate the code stub and pytest test file for a Leetcode question. The class may be instantiated by either a question's QID or its titleSlug. It creates a code stub with the question's statement, constrainsts, and basic test cases in the docstring.

    It also creates a pytest test file from the basic test cases in the question body.

    Args:
        titleSlug (str, optional): The title slug of the question.
        qid (int, optional): The frontend question ID of the question.
    """

    def __init__(
        self,
        titleSlug: str | None = None,
        qid: int | None = None,
    ):
        req = requests.get("https://leetcode.com/api/problems/algorithms/").json()
        self.QUESTIONS_LIST = (
            pd.json_normalize(req["stat_status_pairs"])
            .rename(
                columns={
                    "stat.frontend_question_id": "QID",
                    "stat.question__title_slug": "titleSlug",
                }
            )[["QID", "titleSlug"]]
            .sort_values("QID")
            .set_index("QID")
        )
        self.titleSlug = titleSlug
        self.qid = qid
        if self.titleSlug is None:
            if self.qid is None:
                raise ValueError(
                    "At least one of titleSlug or qid needs to be specified."
                )
            elif self.qid in self.QUESTIONS_LIST.index:
                self.titleSlug = self.QUESTIONS_LIST.loc[self.qid].titleSlug
            else:
                raise ValueError("There is no question with the passed qid")
        else:
            if self.titleSlug in self.QUESTIONS_LIST.titleSlug.tolist():
                if self.qid is not None:
                    if self.titleSlug != self.QUESTIONS_LIST.loc[self.qid].titleSlug:
                        raise ValueError(
                            f"Both titleSlug and qid were passed but they do not match.\n{self.qid}: {self.QUESTIONS_LIST.loc[self.qid].titleSlug}"
                        )
                else:
                    self.qid = self.QUESTIONS_LIST[
                        self.QUESTIONS_LIST["titleSlug"] == self.titleSlug
                    ].index[0]
            else:
                raise ValueError("There is no question with the passed titleSlug.")
        print(f"Generating code stub for {self.qid}. {self.titleSlug}")
        self.filename = f"q_{str(self.qid).zfill(4)}_{camel_case(self.titleSlug)}.py"
        questionInfoScraper = GetQuestion(titleSlug=self.titleSlug)
        self.data: Question = questionInfoScraper.scrape()

    def fetch_code_stub(self) -> str:
        """Extracts the python code text from Leetcode's API response.

        Returns:
            str: The python code stub.
        """
        return self.data.Code

    def fetch_problem_statement(self) -> str:
        """Extracts the python problem statement from Leetcode's API response.

        Returns:
            str: Te problem statement in markdown format.
        """
        problem_statement = self.data.Body
        problem_statement_rst = pypandoc.convert_text(
            problem_statement, format="html", to="md"
        )
        return problem_statement_rst

    def create_code_file(self) -> str:
        """Prepares the text to be written in the python file.

        Returns:
            str: The text to be written in the python file.
        """
        problem_statement = self.fetch_problem_statement()
        lines_to_write = []
        code_stub = self.fetch_code_stub()
        for line in code_stub.split("\n"):
            lines_to_write.append(line)
            if line.startswith("class Solution"):
                lines_to_write.append(f'    """{problem_statement}"""')
            elif line.endswith(":") and not line.strip().startswith("#"):
                lines_to_write.append("        pass")
        text_to_write = "\n".join(lines_to_write)
        return text_to_write

    def fetch_problem_statement_codeblocks(self, problem_statement: str) -> list[str]:
        """Extract the code blocks from the given problem statement string. These codeblocks contain the basic test cases provided by Leetcode.

        Args:
            problem_statement (str): The problem statement with the code blocks

        Returns:
            list[str]: The list of code blocks. The length of list is equal to the number of basic test cases provided by Leetcode.
        """
        mk = marko.Markdown()
        markdown_text = mk.parse(problem_statement)
        code_blocks = [
            child.children[0].children
            for child in markdown_text.children
            if isinstance(child, marko.block.CodeBlock)
        ]
        return code_blocks

    def get_parameters(self, code_blocks: list[str]) -> tuple[str, str]:
        """Extract the inputs and outputs from each of the code block in the question body.

        Args:
            code_blocks (list[str]): The list of code block  in the question body.

        Returns:
            tuple[str, str]:
                - str: The input string to be added to the test file.
                - str: The output string to be added to the test file.
        """
        parameters = []
        for test in code_blocks:
            if "Input" in test:
                for line in test.split("\n"):
                    if line.startswith("Input:"):
                        inp = line.split("Input:")[1]
                parameter_dict = parse_args(inp)  # type: ignore
                parameter_dict["output"] = re.search(
                    "Output: (.*)\n",
                    test.replace("true", "True").replace(
                        "false", "False"
                    ),  # Leetcode uses true and false for True and False, respectively.
                )
                if parameter_dict["output"] is not None:
                    parameter_dict["output"] = parse_args(
                        parameter_dict["output"]
                        .group(0)
                        .replace("Output: ", "Output= ")
                        .replace("\n", "")
                    )["Output"]
                parameters.append(parameter_dict)
        output_string = ", ".join(list(parameters[0].keys()))
        input_string = ", ".join(
            f"({test_case})"
            for test_case in [
                ", ".join(
                    [
                        "'{}'".format(x) if isinstance(x, str) else str(x)
                        for x in parameter.values()
                    ]
                )
                for parameter in parameters
            ]
        )
        return input_string, output_string

    def create_test_file(self, code_text: str) -> str:
        """Generates the test file for the given question.

        Args:
            code_text (str): The text that contains the code stub. This is used to get the list of inputs arguments and the name of the method.

        Returns:
            str: The text containing the pytest test case.
        """
        problem_statement = self.fetch_problem_statement()
        problem_statement_code_blocks = self.fetch_problem_statement_codeblocks(
            problem_statement
        )
        input_string, output_string = self.get_parameters(problem_statement_code_blocks)
        pytestParameterDecorator = (
            f"""@pytest.mark.parametrize("{output_string}", [{input_string}])"""
        )
        className = "Solution"

        # //TODO: This should be used to find the classname instead of hard-coding it to "Solution"

        # # Use the `parse` function to create an AST from the file's contents
        # root = ast.parse(code_text)
        # # Iterate through the top-level nodes in the AST
        # for node in ast.walk(root):
        #     # Check if the node is a ClassDef node
        #     if isinstance(node, ast.ClassDef):
        #         # Check if the class is not commented
        #         if not node.name.startswith("#"):
        #             # Print the class name
        #             print(node.name)  # type: ignore

        methodsName = re.findall("\n    def (.*):", code_text)
        for i, methodName in enumerate(methodsName):
            a, b = methodName.split(") -> ")
            methodsName[i] = f"{a}, output: {b})"
        methods = [
            f"""
    def test_{methodName}:
        sc = {className}()
        assert sc.{methodName.split("(")[0]}({output_string[:-7]}) == output
        """
            for methodName in methodsName
        ]
        test_to_write = f"""import pytest
from {self.filename.split(".py")[0]} import Solution

{pytestParameterDecorator}
class Test{className}:""" + "".join(
            methods
        )

        return test_to_write

    def generate_code_stub_and_tests(self, test=False):
        """Wrapper that creates the code stub and test files after formatting them through black."""
        code_to_write = self.create_code_file()
        if not self.data.isPaidOnly:
            test_to_write = self.create_test_file(code_to_write)
        if not test:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(format_str(code_to_write, mode=FileMode()))
                print(f"Code stub save to {self.filename}")

            if not self.data.isPaidOnly:
                with open(f"test_{self.filename}", "w", encoding="utf-8") as f:
                    f.write(
                        format_str(test_to_write, mode=FileMode())
                    )  # ignore: unbounded
                    print(f"Test file written to test_{self.filename}.py")
