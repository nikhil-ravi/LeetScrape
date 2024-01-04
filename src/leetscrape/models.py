from typing import Literal

from markdownify import markdownify as md
from pydantic import Field
from pydantic.dataclasses import dataclass

Difficulty = Literal["Easy", "Medium", "Hard"]


@dataclass
class Question:
    QID: int
    title: str
    titleSlug: str
    difficulty: Difficulty = Field(default_factory=Difficulty)
    Hints: list[str] = Field(default_factory=list)
    Companies: list[str] | None = None
    topics: list[str] | None = Field(default_factory=list)
    SimilarQuestions: list[int] = Field(default_factory=list)
    Code: str = Field(default_factory=str)
    Body: str = Field(default_factory=str)
    isPaidOnly: bool = False

    def __repr__(self) -> str:
        repr = f"{self.QID}. {self.titleSlug}\n"
        repr += md(self.Body)
        if len(self.Hints) > 1:
            repr += "Hints:\n"
            for idx, hint in enumerate(self.Hints):
                repr += f"    {idx}. {hint}\n"
        if self.Companies is not None:
            repr += f"Companies: {self.Companies}\n"
        if len(self.SimilarQuestions) > 0:
            repr += f"SimilarQuestions: {self.SimilarQuestions}\n"
        return repr


@dataclass
class Solution:
    id: int
    code: str
    docs: dict | None = None
    problem_statement: str | None = None

    def __repr__(self) -> str:
        repr = f"{self.id}.\n{self.code}\n"
        return repr
