from pydantic import BaseModel, Field
from typing import List

class QuestionAnswerPair(BaseModel):
    question: str = Field(description="The question")
    answer: str = Field(description="The answer")

class Proposal(BaseModel):
    text: str = Field(description="The proposal text")
    question_answer_pairs: List[QuestionAnswerPair] = Field(description="The question answer pairs")

class ProposalByModel(BaseModel):
    model_name: str
    proposal: Proposal
    