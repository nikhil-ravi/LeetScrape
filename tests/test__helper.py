from leetscrape._helper import camel_case, parse_args


def test_camel_case():
    assert camel_case("hello_world") == "helloWorld"
    assert camel_case("leet_code") == "leetCode"
    assert camel_case("python_programming") == "pythonProgramming"
    assert camel_case("a_b_c") == "aBC"
    assert camel_case("x_y_z") == "xYZ"


def test_parse_args():
    args = "x=10, y='hello', z=[1, 2, 3]"
    expected_result = {"x": 10, "y": "hello", "z": [1, 2, 3]}
    assert parse_args(args) == expected_result
