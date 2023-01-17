import ast
import pickle
import re

import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy import MetaData, update
from tqdm import tqdm

from GetQuestionInfo import GetQuestionInfo


def combine_list_and_info(list_df: pd.DataFrame, info_df: pd.DataFrame) -> pd.DataFrame:
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
    return questions


def get_all_questions_body(
    titleSlugs, isPaidOnlyList, filename: str = "../example/data/dump.pickle"
):
    questions_info_list = []
    for i, (titleSlug, paidOnly) in enumerate(tqdm(zip(titleSlugs, isPaidOnlyList))):
        if not paidOnly:
            questions_info_list.append(GetQuestionInfo(titleSlug).scrape())
        if i % 10 == 0:
            with open(filename, "wb") as f:
                pickle.dump(questions_info_list, f)

    with open(filename, "wb") as f:
        pickle.dump(questions_info_list, f)
    return questions_info_list


def extract_solutions(filename: str) -> dict:
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
):
    varss = MetaData(bind=engine)
    MetaData.reflect(varss)
    questions = varss.tables[table_name]
    engine.execute(
        update(questions).where(questions.c.QID == row_id).values({col_name: solutions})
    )
    pass
