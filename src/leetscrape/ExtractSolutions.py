import ast

import sqlalchemy
from docstring_parser.google import DEFAULT_SECTIONS, GoogleParser, Section, SectionType
from sqlalchemy import MetaData, update


class ExtractSolutions:
    def __init__(self, filename: str):
        self.filename = filename

    def extract(self, top_class_name: str = "Solution") -> list[dict]:
        """
        Extract solutions from a given python file.

        Args:
            filename (str): The path of the file to extract solutions from. This python script should have the solution method(s) in the class named in the top_class-name.
            top_class_name (str, optional): The name of the class from which to extract the solutions from. Defaults to `Solution'.

        Raises:
            ValueError: When the filename does not follow the required convention of `q_{{LEETCODE_QID}}_ {{LEETCODE_TITLE}}.py`.
            ValueError: When the provided python file does not have a class named Solution.

        Returns:
            dict: A list of dictionaries, each containing an id, code [and docs].
        """
        with open(self.filename) as fd:
            file_contents = fd.read()
        module = ast.parse(file_contents)
        class_definition = [
            node
            for node in module.body
            if isinstance(node, ast.ClassDef) and node.name == top_class_name
        ]
        if not class_definition:
            raise ValueError(
                "The provided python file should have a class named Solution."
            )
        method_definitions = [
            node
            for node in class_definition[0].body
            if isinstance(node, ast.FunctionDef)
        ]

        solutions = [
            {
                "id": idx,
                "code": self.extract_code(f),
                "docs": parse_method_docstring(ast.get_docstring(f, clean=True)),
            }
            for idx, f in enumerate(method_definitions)
        ]

        return solutions

    def extract_code(
        self,
        node: ast.AsyncFunctionDef | ast.FunctionDef,
    ) -> str:
        if node.lineno is not None and node.end_lineno is not None:
            code_lines = node.lineno, node.end_lineno + 1
        else:
            raise ValueError("Node does not contain any code.")
        doc_lines = get_doc_string_lines(node)
        with open(self.filename, "r") as f:
            data = f.readlines()
        lines_to_retain = []
        for idx, line in enumerate(data):
            if doc_lines is not None:
                if ((idx + 1) in range(*code_lines)) and (
                    (idx + 1) not in range(doc_lines[0], doc_lines[1] + 1)
                ):
                    lines_to_retain.append(line)
            else:
                if (idx + 1) in range(*code_lines):
                    lines_to_retain.append(line)

        return "".join(lines_to_retain)


def get_doc_string_lines(
    node: ast.AsyncFunctionDef | ast.FunctionDef,
) -> tuple[int, int] | None:
    """
    Return the code for the given node after removing the docstring or None
    if no code can be found.  If the node provided does not have docstrings
    a TypeError will be raised.

    If *clean* is `True`, all tabs are expanded to spaces and any whitespace
    that can be uniformly removed from the second line onwards is removed.
    """
    if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
        raise TypeError("%r can't have docstrings" % node.__class__.__name__)
    if (
        node.body
        and isinstance(node.body[0], ast.Expr)
        and node.body[0].lineno
        and node.body[0].end_lineno
    ):
        return node.body[0].lineno, node.body[0].end_lineno
    return None


def parse_method_docstring(docstring: str | None) -> dict:
    if docstring is None:
        return {}

    docs = GoogleParser(
        sections=DEFAULT_SECTIONS
        + [
            Section("Time Complexity", "time", SectionType.SINGULAR_OR_MULTIPLE),
            Section("Space Complexity", "space", SectionType.SINGULAR_OR_MULTIPLE),
        ]
    ).parse(docstring)
    time_complexity = [item for item in docs.meta if item.args[0] == "time"]
    space_complexity = [item for item in docs.meta if item.args[0] == "space"]
    return {
        "description": f"{docs.short_description}\n\n{docs.long_description}",
        "args": [vars(arg) for arg in docs.params],
        "returns": vars(docs.returns),
        "examples": [vars(example) for example in docs.examples],
        "time": vars(time_complexity[0]) if len(time_complexity) > 0 else {},
        "space": vars(space_complexity[0]) if len(space_complexity) > 0 else {},
    }


def extract(filename: str) -> list[dict]:
    """Parse the solution file into its methods and their code and docstrings.

    Args:
        filename (str): The filename that contains the solutions.

    Returns:
        list[dict]: The list of solutions.
    """
    return ExtractSolutions(filename).extract()


def upload_solutions(
    engine: sqlalchemy.engine.Engine,
    row_id: int,
    solutions: list[dict],
    table_name: str = "questions",
    col_name: str = "solutions",
) -> None:
    """Upload solutions to the corresponding row of a table in a database.

    Args:
        engine (sqlalchemy.engine.Engine): The sqlalchemy engine used to connect to the database.
        row_id (int): The id of the row that the solutions should be uploaded to.
        solutions (list[dict]): The list of solutions to be uploaded.
        table_name (str): The name of the table to upload the solutions to. Defaults to "questions".
        col_name (str): The name of the column to upload the solutions to. Defaults to "solutions".
    """
    varss = MetaData(bind=engine)
    MetaData.reflect(varss)
    questions = varss.tables[table_name]
    engine.execute(
        update(questions).where(questions.c.QID == row_id).values({col_name: solutions})
    )
