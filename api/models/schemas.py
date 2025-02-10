from pydantic import BaseModel, Field
from typing import List, Dict
from api.agents.suitability_agent.models import SuitabilityRatingByModel
from api.agents.proposal_agent.models import ProposalByModel, QuestionAnswerPairListByModel

class AIRequest(BaseModel):
    job: Dict = {}
    models: List[str] = []
    aiConfig: Dict = {}

class SuitabilityResponse(BaseModel):
    data: List[SuitabilityRatingByModel]

class SuitabilityRating(BaseModel):
    suitability_score: str = Field(description="A score between 0 and 100 indicating the suitability of the job post for the company")
    reason: str = Field(description="A detailed explanation of the suitability score. Max 2 sentences.")

class ProposalResponse(BaseModel):
    proposals: List[ProposalByModel]
    question_answer_pairs_by_model: List[QuestionAnswerPairListByModel]
