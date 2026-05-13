import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.arogya.evals.regression_suite import RegressionSuite

@pytest.fixture
def mock_evaluators():
    with patch("src.arogya.evals.regression_suite.RagasEvaluator") as MockRagas, \
         patch("src.arogya.evals.regression_suite.HallucinationEvaluator") as MockHallucination:
        
        mock_ragas = MockRagas.return_value
        mock_ragas.evaluate_single.return_value = {
            "faithfulness": 0.9,
            "answer_relevancy": 0.85,
            "context_precision": 0.95,
            "context_recall": 0.88
        }
        
        mock_hallucination = MockHallucination.return_value
        mock_hallucination.evaluate_single.return_value = {
            "score": 0.0,
            "is_successful": True,
            "reason": "No hallucinations detected."
        }
        
        yield MockRagas, MockHallucination

@pytest.fixture
def test_cases():
    return [
        {
            "question": "What are the typical symptoms of Type 2 Diabetes?",
            "answer": "Common symptoms include increased thirst, frequent urination, and increased hunger.",
            "contexts": ["Type 2 diabetes symptoms often develop slowly. They include increased thirst, frequent urination, increased hunger, unintended weight loss, fatigue, and blurred vision."],
            "ground_truth": "Typical symptoms are increased thirst, frequent urination, and hunger.",
            "cost_estimate": 0.005
        },
        {
            "question": "How is hypertension diagnosed?",
            "answer": "It is diagnosed by measuring blood pressure over multiple visits.",
            "contexts": ["Hypertension is diagnosed using a sphygmomanometer. A doctor will typically take multiple readings on separate occasions before making a diagnosis."],
            "ground_truth": "Diagnosis involves taking blood pressure readings on multiple occasions.",
            "cost_estimate": 0.002
        }
    ]

def test_regression_suite_init(mock_evaluators, tmp_path):
    output_dir = str(tmp_path / "reports")
    suite = RegressionSuite(output_dir=output_dir)
    assert suite.output_dir == output_dir
    assert os.path.exists(output_dir)

def test_run_suite(mock_evaluators, test_cases, tmp_path):
    output_dir = str(tmp_path / "reports")
    suite = RegressionSuite(output_dir=output_dir)
    
    df = suite.run_suite(test_cases, version_name="test_v1")
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns).count("question") == 1
    assert list(df.columns).count("faithfulness") == 1
    assert list(df.columns).count("hallucination_score") == 1
    
    assert df.iloc[0]["question"] == "What are the typical symptoms of Type 2 Diabetes?"
    assert df.iloc[0]["faithfulness"] == 0.9
    assert df.iloc[0]["is_hallucination_free"] == True

    files = os.listdir(output_dir)
    assert len(files) == 1
    assert files[0].startswith("test_v1_eval_report_")
    assert files[0].endswith(".csv")

def test_compare_versions(mock_evaluators, tmp_path):
    output_dir = str(tmp_path / "reports")
    suite = RegressionSuite(output_dir=output_dir)
    
    df1 = pd.DataFrame([
        {"faithfulness": 0.8, "answer_relevancy": 0.7, "context_precision": 0.9, "context_recall": 0.8, "hallucination_score": 0.2, "latency_sec": 1.5}
    ])
    df2 = pd.DataFrame([
        {"faithfulness": 0.9, "answer_relevancy": 0.85, "context_precision": 0.95, "context_recall": 0.9, "hallucination_score": 0.0, "latency_sec": 1.2}
    ])
    
    os.makedirs(output_dir, exist_ok=True)
    df1.to_csv(os.path.join(output_dir, "v1_eval_report_1000.csv"), index=False)
    df2.to_csv(os.path.join(output_dir, "v2_eval_report_2000.csv"), index=False)
    
    comparison_df = suite.compare_versions("v1", "v2")
    
    assert isinstance(comparison_df, pd.DataFrame)
    assert len(comparison_df) == 6 
    
    faithfulness_diff = comparison_df[comparison_df["metric"] == "faithfulness"]["diff"].values[0]
    assert abs(faithfulness_diff - 0.1) < 1e-5
    
    hallucination_diff = comparison_df[comparison_df["metric"] == "hallucination_score"]["diff"].values[0]
    assert abs(hallucination_diff - (-0.2)) < 1e-5

def test_compare_versions_no_files(mock_evaluators, tmp_path):
    output_dir = str(tmp_path / "reports")
    suite = RegressionSuite(output_dir=output_dir)
    
    comparison_df = suite.compare_versions("v1", "v2")
    assert comparison_df.empty
