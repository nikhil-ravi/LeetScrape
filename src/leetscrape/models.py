from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class Question:
    QID: int
    titleSlug: str
    Hints: list[str] = Field(default_factory=list)
    Companies: list[str] | None = None
    SimilarQuestions: list[int] = Field(default_factory=list)
    Code: str = Field(default_factory=str)
    Body: str = Field(default_factory=str)
    isPaidOnly: bool = False

    def __repr__(self) -> str:
        repr = f"{self.QID}. {self.titleSlug}\n"
        repr += pypandoc.convert_text(self.Body, "md", "html")
        if len(self.Hints) > 1:
            repr += "Hints:\n"
            for idx, hint in enumerate(self.Hints):
                repr += f"    {idx}. {hint}\n"
        if self.Companies is not None:
            repr += f"Companies: {self.Companies}\n"
        if len(self.SimilarQuestions) > 0:
            repr += f"SimilarQuestions: {self.SimilarQuestions}\n"
        return repr
