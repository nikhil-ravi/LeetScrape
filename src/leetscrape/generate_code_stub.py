import re

import marko
from black import FileMode, format_str
from markdownify import markdownify as md

from ._helper import camel_case, parse_args
from .models import Question
from .question import GetQuestion


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
        self.all_questions_stub_id = (
            GetQuestion.fetch_all_questions_id_and_stub().reset_index().set_index("QID")
        )
        self.titleSlug = titleSlug
        self.qid = qid
        if self.titleSlug is None:
            if self.qid is None:
                raise ValueError(
                    "At least one of titleSlug or qid needs to be specified."
                )
            elif self.qid in self.all_questions_stub_id.index:
                self.titleSlug = self.all_questions_stub_id.loc[self.qid].titleSlug
            else:
                raise ValueError("There is no question with the passed qid")
        else:
            if self.titleSlug in self.all_questions_stub_id.titleSlug.tolist():
                if self.qid is not None:
                    if (
                        self.titleSlug
                        != self.all_questions_stub_id.loc[self.qid].titleSlug
                    ):
                        raise ValueError(
                            f"Both titleSlug and qid were passed but they do not match.\n"
                            + f"{self.qid}: {self.all_questions_stub_id.loc[self.qid].titleSlug}"
                        )
                else:
                    self.qid = self.all_questions_stub_id[
                        self.all_questions_stub_id["titleSlug"] == self.titleSlug
                    ].index[0]
            else:
                raise ValueError("There is no question with the passed titleSlug.")
        print(f"Generating code stub for {self.qid}. {self.titleSlug}")
        self.filename = f"q_{str(self.qid).zfill(4)}_{camel_case(self.titleSlug)}.py"
        questionInfoScraper = GetQuestion(titleSlug=self.titleSlug)
        self.data: Question = questionInfoScraper.scrape()

    def generate(self, testing=False, directory: str = ".") -> None:
        """Wrapper that creates the code stub and test files after formatting them through black.

        Args:
            testing (bool, optional): Whether we are in a testing environment. In testing environment, the files are not written to the disk. Defaults to False.
            directory (str, optional): The directory where the files are to be written. Defaults to ".".
        """
        if directory.endswith("/"):
            directory = directory[:-1]
        code_to_write = self._create_code_file()
        if not self.data.isPaidOnly:
            test_to_write = self._create_test_file(code_to_write)
        if not testing:
            with open(f"{directory}/{self.filename}", "w", encoding="utf-8") as f:
                f.write(format_str(code_to_write, mode=FileMode()))
                print(f"Code stub save to {self.filename}")

            if not self.data.isPaidOnly:
                with open(
                    f"{directory}/test_{self.filename}", "w", encoding="utf-8"
                ) as f:
                    f.write(
                        format_str(test_to_write, mode=FileMode())
                    )  # ignore: unbounded
                    print(f"Test file written to test_{self.filename}.py")

    def _get_code_stub(self) -> str:
        """Extracts the python code text from Leetcode's API response.

        Returns:
            str: The python code stub.
        """
        return self.data.Code

    def _get_problem_statement(self) -> str:
        """Extracts the python problem statement from Leetcode's API response.

        Returns:
            str: Te problem statement in markdown format.
        """
        # Because sup is non-standard markdown, we need to convert them to latex
        problem_statement = re.sub(r"<sup>(.*?)</sup>", r"^{\1}", self.data.Body)
        problem_statement_rst = md(problem_statement)
        return (
            problem_statement_rst.replace("**Input:**", "Input:")
            .replace("**Output:**", "Output:")
            .replace("**Explanation:**", "Explanation:")
        )

    def _create_code_file(self) -> str:
        """Prepares the text to be written in the python file.

        Returns:
            str: The text to be written in the python file.
        """
        code_stub = self._get_code_stub()
        problem_statement = self._get_problem_statement()
        lines_to_write = []
        front_matter = {
            "qid": self.data.QID,
            "title": self.data.title,
            "titleSlug": self.data.titleSlug,
            "difficulty": self.data.difficulty,
            "tags": self.data.topics,
        }
        lines_to_write.append(f"front_matter = {front_matter}")
        lines_to_write.append(
            "# ====================== DO NOT EDIT ABOVE THIS LINE ======================"
        )
        for line in code_stub.split("\n"):
            lines_to_write.append(line)
            if line.startswith("class Solution"):
                lines_to_write.append(f'    """{problem_statement}"""')
            elif line.endswith(":") and not line.strip().startswith("#"):
                lines_to_write.append("        pass")
        lines_to_write.append(
            "    # If you have multiple solutions, add them all here as methods of the same class."
        )
        text_to_write = "\n".join(lines_to_write).replace("\n\n", "\n")
        return text_to_write

    def _extract_codeblocks_in_problem_statement(
        self, problem_statement: str
    ) -> list[str]:
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
            if isinstance(child, marko.block.FencedCode)
        ]
        return code_blocks

    def _get_parameters(self, code_blocks: list[str]) -> tuple[str, str]:
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

    def _create_test_file(self, code_text: str) -> str:
        """Generates the test file for the given question.

        Args:
            code_text (str): The text that contains the code stub. This is used to get the list of inputs arguments and the name of the method.

        Returns:
            str: The text containing the pytest test case.
        """
        problem_statement = self._get_problem_statement()
        problem_statement_code_blocks = self._extract_codeblocks_in_problem_statement(
            problem_statement
        )
        input_string, output_string = self._get_parameters(
            problem_statement_code_blocks
        )
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
