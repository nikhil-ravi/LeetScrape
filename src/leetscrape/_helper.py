import ast
import re


def camel_case(s: str) -> str:
    """
    Convert a string to camel case.

    Args:
        s (str): The input string.

    Returns:
        str: The camel case version of the input string.
    """
    s = re.sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


def parse_args(args: str) -> dict:
    """A method to parse the arguments of a python method given in string format.

    Args:
        args (str): The arguments of a method in string format.

    Returns:
        dict: A dictionary of argument value pairs.
    """
    args = "f({})".format(args)
    tree = ast.parse(args)
    funccall = tree.body[0].value  # type: ignore
    args = {arg.arg: ast.literal_eval(arg.value) for arg in funccall.keywords}  # type: ignore
    return args  # type: ignore
