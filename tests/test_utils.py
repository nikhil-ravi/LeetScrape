import os
import pickle

import pandas as pd

from leetscrape.utils import combine_list_and_info, get_all_questions_body


def test_combine_list_and_info():
    with open("./example/data/questionBody.pickle", "rb") as f:
        data = pickle.load(f)
    questions_body = pd.DataFrame(data).drop(columns=["titleSlug"])
    questions_body["QID"] = questions_body["QID"].astype(int)
    questions = pd.read_csv("./example/data/questions.csv")
    questions = combine_list_and_info(
        info_df=questions_body, list_df=questions, save_to="./all.json"
    )
    os.remove("./all.json")


def test_get_all_questions_body():
    get_all_questions_body(
        ["two-sum", "add-two-numbers"], [False, False], "./dump.pickle"
    )
    os.remove("./dump.pickle")
