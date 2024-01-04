import ast

from docstring_parser.google import DEFAULT_SECTIONS, GoogleParser, Section, SectionType

from .models import Solution


class ExtractSolutions:
    def __init__(self, filename: str):
        self.filename = filename
        with open(self.filename) as fd:
            file_contents = fd.read()
        self.module = ast.parse(file_contents)
        self.solutions = None

    def extract(self, top_class_name: str = "Solution") -> list[Solution]:
        """
        Extract solutions from a given python file.

        Args:
            filename (str): The path of the file to extract solutions from. This python script should have the solution method(s) in the class named in the top_class-name.
            top_class_name (str, optional): The name of the class from which to extract the solutions from. Defaults to `Solution'.

        Raises:
            ValueError: When the filename does not follow the required convention of `q_{{LEETCODE_QID}}_ {{LEETCODE_TITLE}}.py`.
            ValueError: When the provided python file does not have a class named Solution.

        Returns:
            list[Solution]: A list of solutions, each containing an id, code [and docs].
        """

        class_definition = [
            node
            for node in self.module.body
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

        self.solutions = [
            Solution(
                id=idx + 1,
                code=self._extract_code(f),
                docs=parse_method_docstring(ast.get_docstring(f, clean=True)),
                problem_statement=ast.get_docstring(class_definition[0], clean=True),
            )
            for idx, f in enumerate(method_definitions)
        ]

        return self.solutions

    def to_mdx(self, output_filename: str | None = None) -> str:
        if self.solutions is None:
            self.extract()
        front_matter = self._extract_front_matter()
        # Add frontmatter
        mdx = "---\n"
        for key, value in front_matter.items():
            if isinstance(value, list):
                mdx += f"{key}: {', '.join(value)}\n"
            else:
                mdx += f"{key}: {value}\n"
        mdx += "---\n\n"
        mdx += f"{self.solutions[0].problem_statement}\n\n"
        mdx += "## Solutions\n\n"
        for solution in self.solutions:
            if len(self.solutions) > 1:
                mdx += f"### Method {solution.id}\n\n"
            mdx += f"```python\nclass Solution:\n{solution.code}```\n\n"
            if "description" in solution.docs:
                mdx += f"{solution.docs['description']}\n\n"
            if "time" in solution.docs and "args" in solution.docs["time"]:
                mdx += f"**Time Complexity**: {solution.docs['time']['args'][1]}, {solution.docs['time']['description']}  \n"
            if "space" in solution.docs and "args" in solution.docs["space"]:
                mdx += f"**Space Complexity**: {solution.docs['space']['args'][1]}, {solution.docs['space']['description']}  \n"
            mdx += "\n"
        if output_filename:
            with open(output_filename, "w") as f:
                f.write(mdx)
        else:
            return mdx

    def _extract_code(
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

    def _extract_front_matter(
        self, front_matter_name: str = "front_matter"
    ) -> dict[str, str | list[str]]:
        """
        Extracts the front matter from the given AST module.

        Args:
            front_matter_name (str): The name of the variable containing the front matter. Defaults to "front_matter".

        Returns:
            dict[str, str | list[str]]: The extracted front matter as a dictionary.

        Raises:
            ValueError: If the front_matter is not a dictionary.
        """
        front_matter = {}

        for item in self.module.body:
            if isinstance(item, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == front_matter_name
                for target in item.targets
            ):
                if not isinstance(item.value, ast.Dict):
                    raise ValueError("front_matter must be a dict")

                for key, value in zip(item.value.keys, item.value.values):
                    if isinstance(value, ast.Constant):
                        front_matter[key.s] = value.s
                    elif isinstance(value, ast.List):
                        front_matter[key.s] = [el.s for el in value.elts]

        return front_matter


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
