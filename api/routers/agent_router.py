from fastapi import APIRouter, Request
from typing import List
from api.models.schemas import AIRequest, SuitabilityResponse, ProposalResponse
from api.services.agent_service import AgentService

router = APIRouter()

agent_service = AgentService()

@router.post("/analyze-job", response_model=SuitabilityResponse)
async def analyze_job(req: AIRequest):
    ratings = await agent_service.analyze_job(req)
    return SuitabilityResponse(data=ratings)

@router.post("/generate-proposal", response_model=ProposalResponse)
async def generate_proposal(req: AIRequest):
    result = await agent_service.generate_proposal(req)
    proposals = result["proposals"]
    
    return ProposalResponse(
        proposals=proposals,
    )

