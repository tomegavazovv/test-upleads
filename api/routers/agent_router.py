from fastapi import APIRouter
from typing import List
from api.models.schemas import AIRequest
from api.agents.suitability_agent.models import SuitabilityRatingByModel
from api.agents.proposal_agent.models import ProposalByModel
from api.services.agent_service import AgentService

router = APIRouter()

agent_service = AgentService()

@router.post("/analyze-job", response_model=List[SuitabilityRatingByModel])
async def analyze_job(req: AIRequest):
    ratings = await agent_service.analyze_job(req)
    return ratings

@router.post("/generate-proposal", response_model=List[ProposalByModel])
async def generate_proposal(req: AIRequest):
    proposals = await agent_service.generate_proposal(req)
    return proposals

