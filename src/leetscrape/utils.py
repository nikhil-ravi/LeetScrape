import pickle

import numpy as np
import pandas as pd
from tqdm import tqdm

from .question import GetQuestion

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
            questions_info_list.append(GetQuestion(titleSlug).scrape())
        if i % 10 == 0:
            with open(save_to, "wb") as f:
                pickle.dump(questions_info_list, f)

    with open(save_to, "wb") as f:
        pickle.dump(questions_info_list, f)
    return questions_info_list
