from fastapi import APIRouter, Request
from typing import List
from api.models.schemas import AIRequest, SuitabilityResponse, ProposalResponse
from api.services.suitability_service import SuitabilityService

router = APIRouter()

suitability_service = SuitabilityService()

@router.post("/analyze-job", response_model=SuitabilityResponse)
async def analyze_job(req: AIRequest):
    ratings = await suitability_service.analyze_job(req)
    return SuitabilityResponse(data=ratings)

@router.post("/generate-proposal", response_model=ProposalResponse)
async def generate_proposal(req: AIRequest):
    result = await suitability_service.generate_proposal(req)
    proposals = result["proposals"]
    question_answer_pairs_by_model = result["question_answer_pairs_by_model"]
    
    return ProposalResponse(
        proposals=proposals,
        question_answer_pairs_by_model=question_answer_pairs_by_model
    )

