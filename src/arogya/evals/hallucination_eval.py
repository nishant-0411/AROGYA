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

class HallucinationEvaluator:
    def __init__(self, threshold: float = 0.5, use_local_model: bool = True):
        self.threshold = threshold
        if use_local_model:
            self.eval_model = LocalEvaluatorModel()
            self.metric = HallucinationMetric(threshold=self.threshold, model=self.eval_model)
        else:
            self.metric = HallucinationMetric(threshold=self.threshold)

    def evaluate_single(
        self,
        input_text: str,
        actual_output: str,
        contexts: List[str]
    ) -> Dict[str, Any]:
        test_case = LLMTestCase(
            input=input_text,
            actual_output=actual_output,
            context=contexts
        )
        self.metric.measure(test_case)
        return {
            "score": self.metric.score,
            "is_successful": self.metric.is_successful(),
            "reason": self.metric.reason
        }

    def evaluate_batch(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for item in data:
            results.append(self.evaluate_single(
                input_text=item.get("input", ""),
                actual_output=item.get("actual_output", ""),
                contexts=item.get("contexts", [])
            ))
        return results
