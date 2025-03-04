from typing import Optional
from pydantic import BaseModel

class AiConfig(BaseModel):
    id: str
    suitabilityPrompt: Optional[str] = None
    proposalPrompt: Optional[str] = None
    questionProposalPrompt: Optional[str] = None
    knowledgeBase: Optional[str] = None

