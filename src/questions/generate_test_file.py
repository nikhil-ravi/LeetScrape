import re
from pytest_codeblocks.main import extract_from_file
from pathlib import Path
import argparse
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--filename', type=str, required=True, help="The filename of the python script for which to create pytest cases.")


def get_parameters(f: str | bytes | Path, encoding: str | None = "utf-8", *args, **kwargs):
    tests = extract_from_file(f, encoding, *args, **kwargs)
    parameters = []
    for test in tests:
        inputs = re.search("Input: (.*)\n", test.code).group(1)
        inpDict = {}
        for inp in inputs.split(";"):
            keyVal = inp.strip().split(" = ")
            inpDict[keyVal[0]] = keyVal[1]
        inpDict['output'] = re.search("Output: (.*)\n", test.code).group(1)
        parameters.append(inpDict)
    output_string = ', '.join(list(parameters[0].keys()))
    input_string = ', '.join(f"({', '.join(list(parameter.values()))})" for parameter in parameters)
    return input_string, output_string

def write_test_file(f: str | bytes | Path, encoding: str | None = "utf-8", *args, **kwargs):
    input_string, output_string = get_parameters(f"./src/{f}.py")
    pytestParameterDecorator = f"""@pytest.mark.parametrize("{output_string}", [{input_string}])"""
    with open(f"./src/{f}.py", "r") as dataFile:
        data = dataFile.read()
    className = re.search("class (.*):", data).group(1)
    methodsName = re.findall("def (.*):", data)
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
    with open(f"./tests/test_{f}.py", 'w') as outputFile:
        outputFile.write(
            f"""import pytest
from src.{f} import Solution


{pytestParameterDecorator}
class Test{className}:""" + "".join(methods)
        ) 
    
def main():
    args = parser.parse_args()
    write_test_file(args.filename)  
    
if __name__ == "__main__":
    main()