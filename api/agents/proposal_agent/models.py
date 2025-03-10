from pydantic import BaseModel, Field
from typing import List, Optional

class QuestionAnswerPair(BaseModel):
    question: str = Field(description="The question")
    answer: str = Field(description="The answer")

class Proposal(BaseModel):
    coverLetter: str = Field(description="The proposal text")
    questionAnswerPairs: Optional[List[QuestionAnswerPair]] = Field(default=None, description="The question answer pairs (optional)")

class ProposalByModel(BaseModel):
    modelName: str
    proposal: Proposal
    