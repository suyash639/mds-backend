import pytest
from app.validators import QuestionValidator, CategoryValidator, SourceValidator

class TestQuestionValidator:
    def test_validate_question_text_valid(self):
        text = "What is 2+2?"
        result = QuestionValidator.validate_question_text(text)
        assert result == text
    
    def test_validate_question_text_empty(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            QuestionValidator.validate_question_text("")
    
    def test_validate_question_text_too_long(self):
        text = "x" * 10001
        with pytest.raises(ValueError, match="exceeds maximum length"):
            QuestionValidator.validate_question_text(text)
    
    def test_validate_options_valid(self):
        options = ["A", "B", "C"]
        result = QuestionValidator.validate_options(options)
        assert result == options
    
    def test_validate_options_duplicate(self):
        with pytest.raises(ValueError, match="Duplicate options"):
            QuestionValidator.validate_options(["A", "B", "A"])
    
    def test_validate_correct_answer_valid(self):
        answer = QuestionValidator.validate_correct_answer("A", ["A", "B", "C"])
        assert answer == "A"
    
    def test_validate_correct_answer_not_in_options(self):
        with pytest.raises(ValueError, match="must be one of"):
            QuestionValidator.validate_correct_answer("D", ["A", "B", "C"])
    
    def test_validate_metadata_valid(self):
        metadata = {"difficulty": "easy", "passing_score": 75}
        result = QuestionValidator.validate_metadata(metadata)
        assert result["passing_score"] == 75
    
    def test_validate_metadata_invalid_score(self):
        with pytest.raises(ValueError, match="between 0 and 100"):
            QuestionValidator.validate_metadata({"passing_score": 150})

class TestCategoryValidator:
    def test_validate_name_valid(self):
        name = QuestionValidator.validate_question_text("Mathematics")
        assert isinstance(name, str)
    
    def test_validate_name_empty(self):
        with pytest.raises(ValueError):
            CategoryValidator.validate_name("")

class TestSourceValidator:
    def test_validate_url_valid(self):
        url = "https://example.com"
        result = SourceValidator.validate_url(url)
        assert result == url
    
    def test_validate_year_valid(self):
        year = SourceValidator.validate_year(2023)
        assert year == 2023
    
    def test_validate_year_invalid(self):
        with pytest.raises(ValueError, match="Invalid year"):
            SourceValidator.validate_year(1850)
