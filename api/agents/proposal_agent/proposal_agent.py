from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Send
from typing import Annotated, TypedDict
import operator
import json
from api.utils.get_model_instance import get_model_instance
from api.agents.proposal_agent.models import ProposalByModel, Proposal, QuestionAnswerPairList, QuestionAnswerPair, QuestionAnswerPairListByModel

class GenerateQuestionsState(TypedDict):
    job_title: str
    job_description: str
    model_name: str
    questions: list[str]
    
class GenerateProposalState(TypedDict):
    job_title: str
    job_description: str
    model_name: str
    job_country: str
class ProposalAgentState(TypedDict):
    proposals: Annotated[list[ProposalByModel], operator.add]
    question_answer_pairs_by_model: Annotated[list[QuestionAnswerPairListByModel], operator.add]
    models: list[str]
    job_title: str
    job_description: str
    job_country: str
    questions: list[str]

class ProposalAgent:
    def __init__(self, models, proposal_system="", question_answer_system=""):
        self.proposal_system = proposal_system
        self.question_answer_system = question_answer_system
        self.models = models
        graph = StateGraph(ProposalAgentState)

        # nodes
        graph.add_node("distribute_to_models", self.distribute_to_models)
        graph.add_node("generate_proposal", self.generate_proposal)
        graph.add_node("generate_questions", self.generate_questions)
        graph.set_entry_point("distribute_to_models")
        
        graph.add_conditional_edges("distribute_to_models", self.distribute_tasks, ["generate_proposal", "generate_questions"])
        graph.add_edge("generate_proposal", END)
        graph.add_edge("generate_questions", END)
        
        self.graph = graph.compile()

    def distribute_to_models(self, state: ProposalAgentState):
        return state

    def distribute_tasks(self, state: ProposalAgentState):
        tasks = []
        for model_name in state["models"]:
            # Separate states for each task
            proposal_state = {
                "job_title": state["job_title"],
                "job_description": state["job_description"],
                "model_name": model_name,
                "job_country": state["job_country"]
            }
            tasks.append(Send("generate_proposal", proposal_state))
            
            # Only add generate_questions task if there are questions
            if state.get("questions"):
                questions_state = {
                    "job_title": state["job_title"],
                    "job_description": state["job_description"],
                    "model_name": model_name,
                    "questions": state["questions"]
                }
                tasks.append(Send("generate_questions", questions_state))
        return tasks

    def generate_proposal(self, state: GenerateProposalState, config: RunnableConfig):
        job = {
            "title": state['job_title'],
            "description": state['job_description'],
            "country": state['job_country']
        }
        messages = [HumanMessage(content=json.dumps(job))]
        if self.proposal_system:
            messages = [SystemMessage(content=self.proposal_system)] + messages

        model = get_model_instance(state['model_name']).with_structured_output(Proposal)

        message = model.invoke(messages, config=config)

        proposal = ProposalByModel(model_name=state['model_name'], proposal=Proposal(text=message.text))

        return {'proposals': [proposal]}

    def generate_questions(self, state: GenerateQuestionsState, config: RunnableConfig):
      questions = state['questions']

      messages = [HumanMessage(content=json.dumps(questions))]
      if self.question_answer_system:
          messages = [SystemMessage(content=self.question_answer_system)] + messages

      model = get_model_instance(state['model_name']).with_structured_output(QuestionAnswerPairList)

      message = model.invoke(messages, config=config)

      question_answer_pair_list_by_model = QuestionAnswerPairListByModel(model_name=state['model_name'], question_answer_pairs=message.question_answer_pairs)

      return {'question_answer_pairs_by_model': [question_answer_pair_list_by_model]}

async def run_proposal_agent(job, models, proposal_system=None, question_answer_system=None):
    abot = ProposalAgent(models, proposal_system=proposal_system, question_answer_system=question_answer_system)
    result = await abot.graph.ainvoke({"job_title": job["title"], "job_description": job["description"], "models": models, "questions": job["questions"]})
 
    return {
        "proposals": result["proposals"],
        "question_answer_pairs_by_model": result["question_answer_pairs_by_model"]
    }