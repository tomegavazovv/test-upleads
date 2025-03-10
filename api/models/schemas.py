from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from api.agents.suitability_agent.models import SuitabilityRatingByModel
from api.agents.proposal_agent.models import ProposalByModel


class AIRequest(BaseModel):
    job: Dict = {}
    models: List[str] = []
    aiConfig: Dict = {}

class SuitabilityRating(BaseModel):
    suitability_score: str = Field(description="A score between 0 and 100 indicating the suitability of the job post for the company")
    reason: str = Field(description="A detailed explanation of the suitability score. Max 2 sentences.")
    

class AiConfig(BaseModel):
    id: str
    suitabilityPrompt: Optional[str] = None
    proposalPrompt: Optional[str] = None
    questionProposalPrompt: Optional[str] = None
    knowledgeBase: Optional[str] = None