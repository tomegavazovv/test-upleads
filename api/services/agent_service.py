import concurrent.futures
from typing import List
from api.models.schemas import AIRequest, SuitabilityResponse, ProposalResponse, SuitabilityRating
from api.utils.get_model_instance import get_model_instance
from api.prompts.answer_questions import answer_questions_prompt
from api.agents.suitability_agent.suitability_agent import run_suitability_agent
from api.agents.proposal_agent.proposal_agent import run_proposal_agent
from api.agents.suitability_agent.models import SuitabilityRatingByModel
from api.agents.proposal_agent.models import ProposalByModel
from api.prompts.system_with_knowledge_base_prompt import system_with_knowledge_base_prompt
from api.models.types import AiConfig

class AgentService:
    def __init__(self):
      pass

    async def analyze_job(self, req: AIRequest) -> List[SuitabilityRatingByModel]:
      ai_config = AiConfig(**req.aiConfig)

      knowledge_base = ai_config.knowledgeBase
      system_with_knowledge_base = system_with_knowledge_base_prompt.format(knowledge_base=knowledge_base, system_prompt=ai_config.suitabilityPrompt)

      ratings = await run_suitability_agent(req.job, req.models, system_with_knowledge_base)
      return ratings
      

    async def generate_proposal(self, req: AIRequest) -> dict:
      ai_config = AiConfig(**req.aiConfig)

      knowledge_base = ai_config.knowledgeBase
      proposal_system = ai_config.proposalPrompt if req.job['questions'] else ai_config.questionProposalPrompt
      proposal_system_with_knowledge_base = system_with_knowledge_base_prompt.format(knowledge_base=knowledge_base, system_prompt=proposal_system)
      
      question_system = answer_questions_prompt.format(knowledge_base=ai_config.knowledgeBase)
      
      proposals = await run_proposal_agent(req.job, req.models, proposal_system_with_knowledge_base)
      return proposals
   
