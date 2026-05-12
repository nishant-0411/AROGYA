import os
import pandas as pd
from typing import List, Dict, Any, Optional
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings

class RagasEvaluator:
    def __init__(self, llm_model: str = "llama3", embeddings_model: str = "nomic-embed-text"):
        self.llm = ChatOllama(model=llm_model)
        self.embeddings = OllamaEmbeddings(model=embeddings_model)
        self.metrics = [
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ]

    def evaluate_dataset(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        formatted_data = {
            "question": [],
            "answer": [],
            "contexts": [],
            "ground_truth": []
        }
        for item in data:
            formatted_data["question"].append(item.get("question", ""))
            formatted_data["answer"].append(item.get("answer", ""))
            formatted_data["contexts"].append(item.get("contexts", []))
            formatted_data["ground_truth"].append(item.get("ground_truth", ""))
        dataset = Dataset.from_dict(formatted_data)
        result = evaluate(
            dataset,
            metrics=self.metrics,
            llm=self.llm,
            embeddings=self.embeddings,
        )
        return result.to_pandas()  # type: ignore

    def evaluate_single(
        self,
        question: str,
        answer: str,
        contexts: List[str],
        ground_truth: Optional[str] = None
    ) -> Dict[str, float]:
        data = [{
            "question": question,
            "answer": answer,
            "contexts": contexts,
            "ground_truth": ground_truth or ""
        }]
        df = self.evaluate_dataset(data)
        result_dict = df.iloc[0].to_dict()
        return {k: float(v) for k, v in result_dict.items() if isinstance(v, (int, float))}
