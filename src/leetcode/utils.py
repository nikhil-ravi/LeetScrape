import pandas as pd
import numpy as np
from tqdm import tqdm
from leetcode.GetQuestionInfo import GetQuestionInfo
import pickle


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
    titleSlugs, isPaidOnlyList, filename: str = "../data/dump.pickle"
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
