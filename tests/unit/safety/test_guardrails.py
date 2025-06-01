"""Tests for the safety guardrails module."""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException

from app.safety.guardrails import LLMSafetyValidator, SafetyViolation


class TestLLMSafetyValidator:
    """Test cases for LLMSafetyValidator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = LLMSafetyValidator()
    
    def test_init(self):
        """Test LLMSafetyValidator initialization."""
        validator = LLMSafetyValidator()
        assert validator is not None
        assert validator.model_name == "gemini-1.5-flash"
    
    @patch('app.safety.guardrails.genai.GenerativeModel')
    def test_validate_content_safe(self, mock_model):
        """Test validation of safe content."""
        mock_response = MagicMock()
        mock_response.text = "SAFE: This content is appropriate for educational use."
        
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        content = "This is a safe educational intervention about reading comprehension."
        result = self.validator.validate_content(content)
        
        assert result is True
    
    @patch('app.safety.guardrails.genai.GenerativeModel')
    def test_validate_content_unsafe(self, mock_model):
        """Test validation of unsafe content."""
        mock_response = MagicMock()
        mock_response.text = "UNSAFE: This content contains inappropriate material."
        
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        content = "This intervention involves harmful activities."
        result = self.validator.validate_content(content)
        
        assert result is False
    
    @patch('app.safety.guardrails.genai.GenerativeModel')
    def test_validate_content_api_error(self, mock_model):
        """Test validation when API raises an error."""
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.side_effect = Exception("API Error")
        mock_model.return_value = mock_model_instance
        
        content = "Test content"
        
        with pytest.raises(HTTPException) as exc_info:
            self.validator.validate_content(content)
        
        assert exc_info.value.status_code == 500
        assert "Safety validation failed" in str(exc_info.value.detail)
    
    @patch('app.safety.guardrails.genai.GenerativeModel')
    def test_validate_content_ambiguous_response(self, mock_model):
        """Test validation with ambiguous response."""
        mock_response = MagicMock()
        mock_response.text = "This response doesn't clearly indicate safety."
        
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        content = "Ambiguous content"
        result = self.validator.validate_content(content)
        
        # Should default to unsafe for ambiguous responses
        assert result is False
    
    @patch('app.safety.guardrails.genai.GenerativeModel')
    def test_validate_content_empty_response(self, mock_model):
        """Test validation with empty response."""
        mock_response = MagicMock()
        mock_response.text = ""
        
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        content = "Test content"
        result = self.validator.validate_content(content)
        
        # Should default to unsafe for empty responses
        assert result is False
    
    def test_safety_violation_creation(self):
        """Test SafetyViolation data class creation."""
        violation = SafetyViolation(
            content="Unsafe content",
            reason="Contains inappropriate material",
            severity="HIGH"
        )
        
        assert violation.content == "Unsafe content"
        assert violation.reason == "Contains inappropriate material"
        assert violation.severity == "HIGH"
    
    @patch('app.safety.guardrails.genai.GenerativeModel')
    def test_validate_content_case_insensitive(self, mock_model):
        """Test that validation is case insensitive."""
        mock_response = MagicMock()
        mock_response.text = "safe: This content is appropriate."
        
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        content = "Safe educational content"
        result = self.validator.validate_content(content)
        
        assert result is True
    
    @patch('app.safety.guardrails.genai.GenerativeModel')
    def test_validate_content_with_whitespace(self, mock_model):
        """Test validation with response containing whitespace."""
        mock_response = MagicMock()
        mock_response.text = "  SAFE: Content is appropriate  "
        
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        content = "Educational content"
        result = self.validator.validate_content(content)
        
        assert result is True
    
    @patch('app.safety.guardrails.genai.GenerativeModel')
    def test_validate_multiple_contents(self, mock_model):
        """Test validation of multiple content pieces."""
        mock_responses = [
            MagicMock(text="SAFE: First content is appropriate"),
            MagicMock(text="UNSAFE: Second content is inappropriate"),
            MagicMock(text="SAFE: Third content is appropriate")
        ]
        
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.side_effect = mock_responses
        mock_model.return_value = mock_model_instance
        
        contents = [
            "Safe educational content 1",
            "Unsafe content with harmful material",
            "Safe educational content 2"
        ]
        
        results = [self.validator.validate_content(content) for content in contents]
        
        assert results == [True, False, True] 