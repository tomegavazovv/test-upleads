from pydantic import BaseModel, Field
from typing import List

class Proposal(BaseModel):
    text: str = Field(description="The proposal text")

class ProposalByModel(BaseModel):
    model_name: str
    proposal: Proposal

class QuestionAnswerPair(BaseModel):
    question: str = Field(description="The question")
    answer: str = Field(description="The answer")

class QuestionAnswerPairList(BaseModel):
    question_answer_pairs: List[QuestionAnswerPair] 

class QuestionAnswerPairListByModel(BaseModel):
    model_name: str
    question_answer_pairs: List[QuestionAnswerPair] 