"""Tests for the main FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import json

from app.main import app
from app.schemas.base import InterventionRequest, EMTScores, ClassMetadata
from app.schemas.curriculum import CurriculumRequest, SkillArea, GradeLevel


class TestMainApp:
    """Test cases for the main FastAPI application."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = TestClient(app)
    
    def test_health_endpoint(self):
        """Test the health check endpoint."""
        with patch('app.llm.gateway.LLMGatewayFactory.create') as mock_factory, \
             patch('app.llm.curriculum_gateway.GeminiCurriculumGateway') as mock_curriculum:
            
            # Mock the gateways
            mock_llm = MagicMock()
            mock_llm.health_check.return_value = True
            mock_factory.return_value = mock_llm
            
            mock_curr = MagicMock()
            mock_curr.health_check.return_value = True
            mock_curriculum.return_value = mock_curr
            
            response = self.client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "version" in data
    
    @patch('app.llm.gateway.LLMGatewayFactory.create')
    def test_generate_intervention_success(self, mock_factory):
        """Test successful intervention generation."""
        # Mock the gateway response
        mock_gateway = MagicMock()
        mock_response = MagicMock()
        mock_response.analysis = "Test analysis"
        mock_response.strategies = []
        mock_response.timeline = {}
        mock_response.success_metrics = {}
        mock_gateway.generate_intervention.return_value = mock_response
        mock_factory.return_value = mock_gateway
        
        # Test data
        request_data = {
            "scores": {
                "emt1": 75.0,
                "emt2": 45.0,
                "emt3": 80.0,
                "emt4": 70.0
            },
            "metadata": {
                "class_id": "TEST",
                "num_students": 20,
                "deficient_area": "EMT2"
            }
        }
        
        response = self.client.post("/score", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert "analysis" in data
        assert "strategies" in data
        assert "timeline" in data
        assert "success_metrics" in data
    
    def test_generate_intervention_invalid_request(self):
        """Test intervention generation with invalid request data."""
        # Missing required fields
        request_data = {
            "scores": {
                "emt1": 75.0
                # Missing other EMT scores
            }
        }
        
        response = self.client.post("/score", json=request_data)
        assert response.status_code == 422  # Validation error
    
    @patch('app.llm.gateway.LLMGatewayFactory.create')
    def test_generate_intervention_gateway_error(self, mock_factory):
        """Test intervention generation when gateway raises an error."""
        mock_gateway = MagicMock()
        mock_gateway.generate_intervention.side_effect = Exception("Gateway error")
        mock_factory.return_value = mock_gateway
        
        request_data = {
            "scores": {
                "emt1": 75.0,
                "emt2": 45.0,
                "emt3": 80.0,
                "emt4": 70.0
            },
            "metadata": {
                "class_id": "TEST",
                "num_students": 20,
                "deficient_area": "EMT2"
            }
        }
        
        response = self.client.post("/score", json=request_data)
        assert response.status_code == 500
    
    @patch('app.llm.curriculum_gateway.GeminiCurriculumGateway')
    def test_generate_curriculum_success(self, mock_curriculum_class):
        """Test successful curriculum generation."""
        # Mock the gateway response
        mock_gateway = MagicMock()
        mock_response = {
            "recommended_interventions": []
        }
        mock_gateway.generate_curriculum_plan.return_value = mock_response
        mock_curriculum_class.return_value = mock_gateway
        
        # Test data
        request_data = {
            "skill_areas": ["READING_COMPREHENSION"],
            "grade_level": "ELEMENTARY",
            "score": 65.0
        }
        
        response = self.client.post("/curriculum", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert "recommended_interventions" in data
    
    def test_generate_curriculum_invalid_request(self):
        """Test curriculum generation with invalid request data."""
        # Missing required fields
        request_data = {
            "skill_areas": ["READING_COMPREHENSION"]
            # Missing other required fields
        }
        
        response = self.client.post("/curriculum", json=request_data)
        assert response.status_code == 422
    
    @patch('app.llm.curriculum_gateway.GeminiCurriculumGateway')
    def test_generate_curriculum_gateway_error(self, mock_curriculum_class):
        """Test curriculum generation when gateway raises an error."""
        mock_gateway = MagicMock()
        mock_gateway.generate_curriculum_plan.side_effect = Exception("Gateway error")
        mock_curriculum_class.return_value = mock_gateway
        
        request_data = {
            "skill_areas": ["READING_COMPREHENSION"],
            "grade_level": "ELEMENTARY",
            "score": 65.0
        }
        
        response = self.client.post("/curriculum", json=request_data)
        assert response.status_code == 500
    
    def test_openapi_docs(self):
        """Test OpenAPI documentation endpoint."""
        response = self.client.get("/docs")
        assert response.status_code == 200
    
    def test_openapi_json(self):
        """Test OpenAPI JSON schema endpoint."""
        response = self.client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
    
    def test_method_not_allowed(self):
        """Test method not allowed responses."""
        response = self.client.put("/health")
        assert response.status_code == 405
    
    def test_not_found(self):
        """Test 404 responses for non-existent endpoints."""
        response = self.client.get("/non-existent-endpoint")
        assert response.status_code == 404 