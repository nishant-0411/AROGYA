from typing import List, Dict, Any
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase
from deepeval.models import DeepEvalBaseLLM
from langchain_community.chat_models import ChatOllama

class LocalEvaluatorModel(DeepEvalBaseLLM):
    def __init__(self, model_name: str = "llama3"):
        self.chat_model = ChatOllama(model=model_name)

    def load_model(self):
        return self

    def generate(self, prompt: str) -> str:
        response = self.chat_model.invoke(prompt)
        return str(response.content)

    async def a_generate(self, prompt: str) -> str:
        response = await self.chat_model.ainvoke(prompt)
        return str(response.content)

    def get_model_name(self) -> str:
        return "Local Ollama Evaluator"
