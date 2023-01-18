import ast
import pickle
import re

import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy import MetaData, update
from tqdm import tqdm

from .GetQuestionInfo import GetQuestionInfo

"""A set of helper functions to transform and query the scraped data."""


def combine_list_and_info(
    list_df: pd.DataFrame, info_df: pd.DataFrame, save_to: str = ""
) -> pd.DataFrame:
    """
    Combines the questions list dataframe with the questions info dataframe by QID
    and return the combined dataframe where each record contains the QID, title,
    titleSlug, hints, difficulty, acceptance rate, similar questions, topic tags,
    category, code stubs, body, and companies.

    Args:
        list_df (pd.DataFrame): Dataframe that contains the list of questions.
        info_df (pd.DataFrame): Dataframe that contains the additional information of questions.
        save_to (str): If provided, saves the resulting dataframe to a json file with the given name. Defaults to "".

    Returns:
        pd.DataFrame: The combined dataframe.
    """
    questions = pd.concat(
        [list_df.set_index("QID"), info_df.set_index("QID")], axis=1
    ).reset_index()
    questions["Hints"] = questions["Hints"].fillna("").apply(list)
    questions["SimilarQuestions"] = questions["SimilarQuestions"].fillna("").apply(list)
    questions["SimilarQuestions"] = questions["SimilarQuestions"].apply(
        lambda w: [int(q) for q in w]
    )
    questions["Code"] = questions["Code"].fillna("")
    questions["Body"] = questions["Body"].fillna("")
    questions["Companies"] = (
        questions["Companies"].fillna(np.nan).replace([np.nan], [None])
    )
    if len(save_to) > 0:
        questions.to_json(save_to, orient="records")
    return questions


def get_all_questions_body(
    titleSlugs, isPaidOnlyList, save_to: str = "../example/data/dump.pickle"
) -> list[dict[str, str | int]]:
    """
    Get the body of all questions in the list and save it to a file.

    Args:
        titleSlugs (List[str]): A list of titleSlugs of questions.
        isPaidOnlyList (List[bool]): A list of isPaidOnly property of questions, indicating whether the question is subscriber only.
        save_to (str):  The path to save the scraped data.

    Returns:
        list[dict[str, str|int]]: A list of dictionaries containing the question information
    """
    questions_info_list = []
    for i, (titleSlug, paidOnly) in enumerate(tqdm(zip(titleSlugs, isPaidOnlyList))):
        if not paidOnly:
            questions_info_list.append(GetQuestionInfo(titleSlug).scrape())
        if i % 10 == 0:
            with open(save_to, "wb") as f:
                pickle.dump(questions_info_list, f)

    with open(save_to, "wb") as f:
        pickle.dump(questions_info_list, f)
    return questions_info_list


def extract_solutions(filename: str) -> dict:
    """
    Extract solutions from a given python file.

    Args:
        filename (str): The path of the file to extract solutions from. It should be of the following form `q_{{LEETCODE_QID}}_{{LEETCODE_TITLE}}.py`. Furthermore, the python script file should have the solution method in a class named `Solution`.

    Raises:
        ValueError: When the filename does not follow the required convention of `q_{{LEETCODE_QID}}_ {{LEETCODE_TITLE}}.py`.
        ValueError: When the provided python file does not have a class named Solution.

    Returns:
        dict: A dictionary containing the question id and a list of solutions, each solution contains an id, code [and docs].
    """
    qid = re.search("q_(.*)_", filename)
    if qid is not None:
        qid = int(qid.group(1))
    else:
        raise ValueError(
            f"""Invalid filename. Filename should be of the form `q_{{LEETCODE_QID}}_{{LEETCODE_TITLE}}.py`. Received `{filename}` instead."""
        )
    with open(filename) as fd:
        file_contents = fd.read()
    module = ast.parse(file_contents)
    class_definition = [
        node
        for node in module.body
        if isinstance(node, ast.ClassDef) and node.name == "Solution"
    ]
    if not class_definition:
        raise ValueError("The provided python file should have a class named Solution.")
    method_definitions = [
        node for node in class_definition[0].body if isinstance(node, ast.FunctionDef)
    ]

    solutions = [
        {
            "id": idx,
            "code": ast.get_source_segment(file_contents, f, padded=True),
            "docs": ast.get_docstring(f, clean=True),
        }
        for idx, f in enumerate(method_definitions)
    ]

    return {qid: solutions}


def upload_solutions(
    engine: sqlalchemy.engine.Engine,
    row_id: int,
    solutions: dict,
    table_name: str = "questions",
    col_name: str = "solutions",
) -> None:
    """Upload solutions to the corresponding row of a table in a database.

    Args:
        engine (sqlalchemy.engine.Engine): The sqlalchemy engine used to connect to the database.
        row_id (int): The id of the row that the solutions should be uploaded to.
        solutions (dict): The solutions to be uploaded.
        table_name (str): The name of the table to upload the solutions to. Defaults to "questions".
        col_name (str): The name of the column to upload the solutions to. Defaults to "solutions".
    """
    varss = MetaData(bind=engine)
    MetaData.reflect(varss)
    questions = varss.tables[table_name]
    engine.execute(
        update(questions).where(questions.c.QID == row_id).values({col_name: solutions})
    )


def camel_case(s):
    s = re.sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])
