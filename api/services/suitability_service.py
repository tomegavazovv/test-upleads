import concurrent.futures
from typing import List
from api.models.schemas import AIRequest, SuitabilityResponse, ProposalResponse, SuitabilityRating
from api.utils.get_model_instance import get_model_instance
from api.prompts.answer_questions import answer_questions_prompt
from api.agents.suitability_agent.suitability_agent import run_suitability_agent
from api.agents.proposal_agent.proposal_agent import run_proposal_agent
from api.agents.suitability_agent.models import SuitabilityRatingByModel
from api.agents.proposal_agent.models import ProposalByModel

class SuitabilityService:
    def __init__(self):
      pass

    async def analyze_job(self, req: AIRequest) -> List[SuitabilityRatingByModel]:
      ratings = await run_suitability_agent(req.job, req.models, req.aiConfig['suitabilityPrompt'])
      return ratings
      

    async def generate_proposal(self, req: AIRequest) -> dict:
        question_instructions = '\n'.join([f"{qa['question']}: {qa['answer']}" for qa in req.aiConfig['questionAnswers'] if qa['answer'] != ''])
        question_system = answer_questions_prompt.format(
          question_instructions=question_instructions, 
          knowledge_base=req.aiConfig['questionsKnowledgeBase'], 
          answer_template=req.aiConfig['questionDefaultAnswerTemplate'])
        
        proposals = await run_proposal_agent(req.job, req.models, req.aiConfig['proposalPrompt'], question_system)
        return proposals
   
