import os
import time
import pandas as pd
from typing import List, Dict, Any, Optional
from src.arogya.evals.ragas_eval import RagasEvaluator
from src.arogya.evals.hallucination_eval import HallucinationEvaluator

class RegressionSuite:
    def __init__(self, output_dir: str = "data/eval/reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.ragas_evaluator = RagasEvaluator()
        self.hallucination_evaluator = HallucinationEvaluator()
        self.results = []

    def run_suite(self, test_cases: List[Dict[str, Any]], version_name: str = "baseline") -> pd.DataFrame:
        self.results = []
        for case in test_cases:
            start_time = time.time()
            
            ragas_result = self.ragas_evaluator.evaluate_single(
                question=case.get("question", ""),
                answer=case.get("answer", ""),
                contexts=case.get("contexts", []),
                ground_truth=case.get("ground_truth")
            )
            
            hallucination_result = self.hallucination_evaluator.evaluate_single(
                input_text=case.get("question", ""),
                actual_output=case.get("answer", ""),
                contexts=case.get("contexts", [])
            )
            
            latency = time.time() - start_time
            cost = case.get("cost_estimate", 0.0)
            
            combined_result = {
                "version": version_name,
                "question": case.get("question", ""),
                "latency_sec": latency,
                "cost": cost,
                **ragas_result,
                "hallucination_score": hallucination_result.get("score", 0.0),
                "is_hallucination_free": hallucination_result.get("is_successful", True),
                "hallucination_reason": hallucination_result.get("reason", "")
            }
            self.results.append(combined_result)
        
        df = pd.DataFrame(self.results)
        self._save_report(df, version_name)
        return df

    def _save_report(self, df: pd.DataFrame, version_name: str):
        timestamp = int(time.time())
        filename = f"{version_name}_eval_report_{timestamp}.csv"
        filepath = os.path.join(self.output_dir, filename)
        df.to_csv(filepath, index=False)

    def compare_versions(self, version1: str, version2: str) -> pd.DataFrame:
        files = os.listdir(self.output_dir)
        v1_files = sorted([f for f in files if f.startswith(f"{version1}_eval_report")], reverse=True)
        v2_files = sorted([f for f in files if f.startswith(f"{version2}_eval_report")], reverse=True)
        
        if not v1_files or not v2_files:
            return pd.DataFrame()
            
        df1 = pd.read_csv(os.path.join(self.output_dir, v1_files[0]))
        df2 = pd.read_csv(os.path.join(self.output_dir, v2_files[0]))
        
        metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall", "hallucination_score", "latency_sec"]
        
        comparison = []
        for metric in metrics:
            if metric in df1.columns and metric in df2.columns:
                v1_mean = df1[metric].mean()
                v2_mean = df2[metric].mean()
                comparison.append({
                    "metric": metric,
                    f"{version1}_mean": v1_mean,
                    f"{version2}_mean": v2_mean,
                    "diff": v2_mean - v1_mean
                })
        return pd.DataFrame(comparison)
