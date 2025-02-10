from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Send
from typing import Annotated, TypedDict
import operator
import json
from api.agents.suitability_agent.models import SuitabilityRating, SuitabilityRatingByModel
from api.utils.get_model_instance import get_model_instance

class AnalyzeJobState(TypedDict):
    job_title: str
    job_description: str
    model_name: str

class SuitabilityAgentState(TypedDict):
    suitability_ratings: Annotated[list[SuitabilityRatingByModel], operator.add]
    models: list[str]
    job_title: str
    job_description: str

class SuitabilityAgent:
    def __init__(self, models, system=""):
        self.system = system
        self.models = models
        graph = StateGraph(SuitabilityAgentState)

        # nodes
        graph.add_node("distribute_to_models", self.distribute_to_models)
        graph.add_node("analyze_job", self.analyze_job)

        graph.set_entry_point("distribute_to_models")
        
        graph.add_conditional_edges("distribute_to_models", self.continue_to_analyze_job, ["analyze_job"])
        graph.add_edge("analyze_job", END)
        
        self.graph = graph.compile()

    def distribute_to_models(self, state: SuitabilityAgentState):
        return state

    def continue_to_analyze_job(self, state: SuitabilityAgentState):
        return [Send("analyze_job", {"job_title": state["job_title"], "job_description": state["job_description"], "model_name": model_name}) for model_name in state["models"]]

    def analyze_job(self, state: AnalyzeJobState, config: RunnableConfig):
        job = {
            "title": state['job_title'],
            "description": state['job_description']
        }
        messages = [HumanMessage(content=json.dumps(job))]
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages

        model = get_model_instance(state['model_name']).with_structured_output(SuitabilityRating)

        message = model.invoke(messages, config=config)

        suitability_rating = SuitabilityRating(rating=message.rating, reason=message.reason)
        result = SuitabilityRatingByModel(model_name=state['model_name'], suitability_rating=suitability_rating)

        return {'suitability_ratings': [result]}

async def run_suitability_agent(job, models, system=None):
    abot = SuitabilityAgent(models, system=system)
    result = await abot.graph.ainvoke({"job_title": job["title"], "job_description": job["description"], "models": models})
    return result["suitability_ratings"]

