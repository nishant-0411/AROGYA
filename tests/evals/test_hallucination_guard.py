import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.arogya.evals.hallucination_eval import HallucinationEvaluator, LocalEvaluatorModel

def test_local_evaluator_model_init():
    model = LocalEvaluatorModel(model_name="test_model")
    assert model.get_model_name() == "Local Ollama Evaluator"
    assert model.load_model() == model

@patch("src.arogya.evals.hallucination_eval.ChatOllama")
def test_local_evaluator_generate(mock_chat_ollama):
    mock_instance = MagicMock()
    mock_instance.invoke.return_value.content = "mock response"
    mock_chat_ollama.return_value = mock_instance
    
    model = LocalEvaluatorModel()
    result = model.generate("test prompt")
    
    assert result == "mock response"
    mock_instance.invoke.assert_called_once_with("test prompt")

@pytest.mark.asyncio
@patch("src.arogya.evals.hallucination_eval.ChatOllama")
async def test_local_evaluator_a_generate(mock_chat_ollama):
    mock_instance = AsyncMock()
    mock_instance.ainvoke.return_value.content = "mock async response"
    mock_chat_ollama.return_value = mock_instance
    
    model = LocalEvaluatorModel()
    result = await model.a_generate("test prompt")
    
    assert result == "mock async response"
    mock_instance.ainvoke.assert_called_once_with("test prompt")

@patch("src.arogya.evals.hallucination_eval.HallucinationMetric")
@patch("src.arogya.evals.hallucination_eval.LocalEvaluatorModel")
def test_evaluator_init_local(mock_local_model, mock_metric):
    evaluator = HallucinationEvaluator(threshold=0.7, use_local_model=True)
    assert evaluator.threshold == 0.7
    mock_local_model.assert_called_once()
    mock_metric.assert_called_once_with(threshold=0.7, model=mock_local_model.return_value)

@patch("src.arogya.evals.hallucination_eval.HallucinationMetric")
def test_evaluator_init_remote(mock_metric):
    evaluator = HallucinationEvaluator(threshold=0.8, use_local_model=False)
    assert evaluator.threshold == 0.8
    mock_metric.assert_called_once_with(threshold=0.8)

@patch("src.arogya.evals.hallucination_eval.HallucinationMetric")
@patch("src.arogya.evals.hallucination_eval.LocalEvaluatorModel")
@patch("src.arogya.evals.hallucination_eval.LLMTestCase")
def test_evaluate_single(mock_test_case, mock_local_model, mock_metric):
    mock_metric_instance = mock_metric.return_value
    mock_metric_instance.score = 0.9
    mock_metric_instance.is_successful.return_value = True
    mock_metric_instance.reason = "Good"
    
    evaluator = HallucinationEvaluator()
    result = evaluator.evaluate_single(
        input_text="input",
        actual_output="output",
        contexts=["context"]
    )
    
    mock_test_case.assert_called_once_with(
        input="input",
        actual_output="output",
        context=["context"]
    )
    mock_metric_instance.measure.assert_called_once_with(mock_test_case.return_value)
    assert result == {
        "score": 0.9,
        "is_successful": True,
        "reason": "Good"
    }

@patch("src.arogya.evals.hallucination_eval.HallucinationMetric")
@patch("src.arogya.evals.hallucination_eval.LocalEvaluatorModel")
def test_evaluate_batch(mock_local_model, mock_metric):
    mock_metric_instance = mock_metric.return_value
    mock_metric_instance.score = 0.5
    mock_metric_instance.is_successful.return_value = False
    mock_metric_instance.reason = "Bad"
    
    evaluator = HallucinationEvaluator()
    data = [
        {"input": "i1", "actual_output": "o1", "contexts": ["c1"]},
        {"input": "i2", "actual_output": "o2", "contexts": ["c2"]}
    ]
    
    results = evaluator.evaluate_batch(data)
    
    assert len(results) == 2
    assert results[0] == {"score": 0.5, "is_successful": False, "reason": "Bad"}
    assert results[1] == {"score": 0.5, "is_successful": False, "reason": "Bad"}
    assert mock_metric_instance.measure.call_count == 2
