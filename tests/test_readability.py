from evaluate.readability import evaluate_text_level


def test_evaluate_text_level_simple():
    result = evaluate_text_level("This is a simple sentence.")
    assert isinstance(result, dict)
    assert result["flesch_reading_ease"] > 90
    assert 0 <= result["flesch_kincaid_grade"] < 1


def test_evaluate_text_level_empty():
    result = evaluate_text_level("")
    assert result == {"flesch_reading_ease": 0.0, "flesch_kincaid_grade": 0.0}
