from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_openai.chat_models.base import BaseChatOpenAI
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.tracers import LangChainTracer
import os

tracer = LangChainTracer(project_name="chatbot-upleads")

def get_model_instance(model_name: str):

  if 'gpt' in model_name:
    return ChatOpenAI(
      model=model_name,
      temperature=0,
      callback_manager=CallbackManager([tracer]),
      api_key=os.getenv("OPENAI_API_KEY"),
      request_timeout=30
    )
  elif 'deepseek' in model_name:
    return BaseChatOpenAI(
      model=model_name,
      openai_api_key=os.getenv('DEEPSEEK_API_KEY'),
      openai_api_base="https://api.deepseek.com",
      max_tokens=1024,
      temperature=0,
      callback_manager=CallbackManager([tracer]),
      request_timeout=30
    )
  elif 'claude' in model_name:
    return ChatAnthropic(
      model=model_name,
      temperature=0,
      max_tokens=1024,
      timeout=30,
      max_retries=2,
      api_key=os.getenv('ANTHROPIC_API_KEY'),
      callback_manager=CallbackManager([tracer])
    )