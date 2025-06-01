"""Tests for the LLM intervention gateway."""

import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException

from app.llm.gateway import LLMGatewayFactory, GeminiGateway
from app.schemas.base import InterventionRequest, EMTScores, ClassMetadata, InterventionPlan


class TestLLMGateway:
    """Test cases for the LLM Gateway."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.factory = LLMGatewayFactory()
        
    def test_factory_create_gemini(self):
        """Test factory creates Gemini gateway."""
        with patch.dict('os.environ', {'LLM_PROVIDER': 'gemini'}):
            gateway = self.factory.create()
            assert isinstance(gateway, GeminiGateway)
    
    def test_factory_create_default(self):
        """Test factory creates default gateway."""
        with patch.dict('os.environ', {}, clear=True):
            gateway = self.factory.create()
            assert isinstance(gateway, GeminiGateway)  # Default is Gemini
    
    @patch('app.llm.gateway.genai.GenerativeModel')
    def test_gemini_gateway_init(self, mock_model):
        """Test Gemini gateway initialization."""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            gateway = GeminiGateway()
            assert gateway.model_name == "gemini-1.5-flash"
            mock_model.assert_called_once()
    
    @patch('app.llm.gateway.genai.GenerativeModel')
    def test_generate_intervention_success(self, mock_model):
        """Test successful intervention generation."""
        # Mock response
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "analysis": "Test analysis of EMT scores",
            "strategies": [
                {
                    "activity": "Reading Comprehension Practice",
                    "implementation": ["Step 1", "Step 2"],
                    "expected_outcomes": ["Improved reading"],
                    "time_allocation": "30 minutes",
                    "resources": ["Books", "Worksheets"]
                }
            ],
            "timeline": {
                "week1": "Introduction activities",
                "week2": "Practice activities"
            },
            "success_metrics": {
                "quantitative": ["Test scores improvement"],
                "qualitative": ["Student engagement"],
                "assessment_methods": ["Weekly quizzes"]
            }
        })
        
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            gateway = GeminiGateway()
            
            request = InterventionRequest(
                scores=EMTScores(emt1=75.0, emt2=45.0, emt3=80.0, emt4=70.0),
                metadata=ClassMetadata(
                    class_id="TEST",
                    num_students=20,
                    deficient_area="EMT2"
                )
            )
            
            result = gateway.generate_intervention(request)
            
            assert isinstance(result, InterventionPlan)
            assert result.analysis == "Test analysis of EMT scores"
            assert len(result.strategies) == 1
            assert result.strategies[0].activity == "Reading Comprehension Practice"
    
    @patch('app.llm.gateway.genai.GenerativeModel')
    def test_generate_intervention_invalid_json(self, mock_model):
        """Test intervention generation with invalid JSON response."""
        mock_response = MagicMock()
        mock_response.text = "Invalid JSON response"
        
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            gateway = GeminiGateway()
            
            request = InterventionRequest(
                scores=EMTScores(emt1=75.0, emt2=45.0, emt3=80.0, emt4=70.0),
                metadata=ClassMetadata(
                    class_id="TEST",
                    num_students=20,
                    deficient_area="EMT2"
                )
            )
            
            with pytest.raises(HTTPException) as exc_info:
                gateway.generate_intervention(request)
            
            assert exc_info.value.status_code == 500
            assert "Failed to parse LLM response" in str(exc_info.value.detail)
    
    @patch('app.llm.gateway.genai.GenerativeModel')
    def test_generate_intervention_missing_field(self, mock_model):
        """Test intervention generation with missing required field."""
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "analysis": "Test analysis",
            # Missing strategies, timeline, success_metrics
        })
        
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            gateway = GeminiGateway()
            
            request = InterventionRequest(
                scores=EMTScores(emt1=75.0, emt2=45.0, emt3=80.0, emt4=70.0),
                metadata=ClassMetadata(
                    class_id="TEST",
                    num_students=20,
                    deficient_area="EMT2"
                )
            )
            
            with pytest.raises(HTTPException) as exc_info:
                gateway.generate_intervention(request)
            
            assert exc_info.value.status_code == 500
            assert "Missing required field" in str(exc_info.value.detail)
    
    @patch('app.llm.gateway.genai.GenerativeModel')
    def test_generate_intervention_empty_strategies(self, mock_model):
        """Test intervention generation with empty strategies."""
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "analysis": "Test analysis",
            "strategies": [],
            "timeline": {},
            "success_metrics": {
                "quantitative": [],
                "qualitative": [],
                "assessment_methods": []
            }
        })
        
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model.return_value = mock_model_instance
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            gateway = GeminiGateway()
            
            request = InterventionRequest(
                scores=EMTScores(emt1=75.0, emt2=45.0, emt3=80.0, emt4=70.0),
                metadata=ClassMetadata(
                    class_id="TEST",
                    num_students=20,
                    deficient_area="EMT2"
                )
            )
            
            result = gateway.generate_intervention(request)
            
            assert isinstance(result, InterventionPlan)
            assert len(result.strategies) == 0
    
    @patch('app.llm.gateway.genai.GenerativeModel')
    def test_generate_intervention_api_error(self, mock_model):
        """Test intervention generation when API raises an error."""
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.side_effect = Exception("API Error")
        mock_model.return_value = mock_model_instance
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            gateway = GeminiGateway()
            
            request = InterventionRequest(
                scores=EMTScores(emt1=75.0, emt2=45.0, emt3=80.0, emt4=70.0),
                metadata=ClassMetadata(
                    class_id="TEST",
                    num_students=20,
                    deficient_area="EMT2"
                )
            )
            
            with pytest.raises(HTTPException) as exc_info:
                gateway.generate_intervention(request)
            
            assert exc_info.value.status_code == 500
            assert "LLM API error" in str(exc_info.value.detail)
    
    @patch('app.llm.gateway.genai.GenerativeModel')
    def test_health_check_success(self, mock_model):
        """Test successful health check."""
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.return_value = MagicMock(text="OK")
        mock_model.return_value = mock_model_instance
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            gateway = GeminiGateway()
            result = gateway.health_check()
            assert result is True
    
    @patch('app.llm.gateway.genai.GenerativeModel')
    def test_health_check_failure(self, mock_model):
        """Test health check failure."""
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.side_effect = Exception("Health check failed")
        mock_model.return_value = mock_model_instance
        
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-key'}):
            gateway = GeminiGateway()
            result = gateway.health_check()
            assert result is False 