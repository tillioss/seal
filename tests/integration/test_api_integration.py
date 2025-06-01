"""Integration tests for SEAL API."""

import pytest
import asyncio
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import concurrent.futures
import time

from app.main import app


class TestAPIIntegration:
    """Integration tests for the complete API workflow."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = TestClient(app)
    
    @pytest.mark.integration
    def test_health_check_integration(self):
        """Test health check endpoint integration."""
        response = self.client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        
        # Verify timestamp format
        import datetime
        timestamp = datetime.datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        assert isinstance(timestamp, datetime.datetime)
    
    @pytest.mark.integration
    @patch('app.llm.intervention_gateway.InterventionGateway.generate_intervention_plan')
    def test_intervention_workflow_integration(self, mock_generate):
        """Test complete intervention generation workflow."""
        # Mock realistic response
        mock_response = MagicMock()
        mock_response.analysis = "Based on the EMT2 scores, students need support with emotional expression and recognition."
        mock_response.strategies = [
            {
                "name": "Emotion Recognition Cards",
                "activity": "Use visual cards to help students identify emotions",
                "implementation": "Show cards daily during circle time",
                "expected_outcomes": "Improved emotion vocabulary",
                "time_allocation": "15 minutes daily",
                "resources": ["Emotion cards", "Circle time space"]
            }
        ]
        mock_response.timeline = {
            "week_1": "Introduction to emotion cards",
            "week_2": "Practice with scenarios",
            "week_3": "Student-led activities",
            "week_4": "Assessment and review"
        }
        mock_response.success_metrics = {
            "qualitative": "Students can name 5 basic emotions",
            "quantitative": "80% accuracy in emotion identification",
            "evaluation_methods": "Weekly assessments and observations"
        }
        mock_generate.return_value = mock_response
        
        # Complete request payload
        request_data = {
            "emt_scores": {
                "EMT1": 3.2,
                "EMT2": 1.8,  # Deficient area
                "EMT3": 2.9,
                "EMT4": 3.1
            },
            "class_metadata": {
                "class_name": "Kindergarten A",
                "grade_level": "Kindergarten",
                "subject": "Social-Emotional Learning",
                "teacher_name": "Ms. Rodriguez",
                "school_name": "Sunshine Elementary"
            },
            "deficient_area": "EMT2"
        }
        
        # Execute request
        response = self.client.post("/generate-intervention", json=request_data)
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure
        assert "analysis" in data
        assert "strategies" in data
        assert "timeline" in data
        assert "success_metrics" in data
        
        # Verify content
        assert "EMT2" in data["analysis"]
        assert len(data["strategies"]) > 0
        assert "week_1" in data["timeline"]
        assert "qualitative" in data["success_metrics"]
        
        # Verify gateway was called with correct parameters
        mock_generate.assert_called_once()
        call_args = mock_generate.call_args[0]
        assert call_args[0].deficient_area == "EMT2"
        assert call_args[0].emt_scores.EMT2 == 1.8
    
    @pytest.mark.integration
    @patch('app.llm.curriculum_gateway.CurriculumGateway.generate_curriculum_interventions')
    def test_curriculum_workflow_integration(self, mock_generate):
        """Test complete curriculum generation workflow."""
        # Mock realistic response
        mock_response = MagicMock()
        mock_response.recommended_interventions = [
            {
                "title": "Reading Comprehension Boost",
                "description": "Targeted activities to improve reading understanding",
                "skill_areas": ["READING_COMPREHENSION"],
                "grade_levels": ["GRADE_3"],
                "implementation": {
                    "duration": "4 weeks",
                    "frequency": "Daily",
                    "group_size": "Small groups of 4-6 students",
                    "materials": ["Leveled readers", "Comprehension worksheets"],
                    "activities": [
                        "Guided reading sessions",
                        "Story mapping exercises",
                        "Question generation practice"
                    ]
                },
                "expected_outcomes": "Improved reading comprehension scores by 15%",
                "assessment_methods": ["Pre/post assessments", "Running records"]
            }
        ]
        mock_generate.return_value = mock_response
        
        # Complete request payload
        request_data = {
            "skill_areas": ["READING_COMPREHENSION"],
            "grade_levels": ["GRADE_3"],
            "scores": {
                "reading_comprehension": 2.1,  # Below average
                "mathematical_reasoning": 3.5,
                "scientific_inquiry": 3.0,
                "writing_skills": 2.8,
                "critical_thinking": 3.2
            },
            "class_metadata": {
                "class_name": "3rd Grade Blue",
                "grade_level": "3rd Grade",
                "subject": "Language Arts",
                "teacher_name": "Mr. Thompson",
                "school_name": "Oak Tree Elementary"
            }
        }
        
        # Execute request
        response = self.client.post("/generate-curriculum", json=request_data)
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure
        assert "recommended_interventions" in data
        assert len(data["recommended_interventions"]) > 0
        
        intervention = data["recommended_interventions"][0]
        assert "title" in intervention
        assert "description" in intervention
        assert "skill_areas" in intervention
        assert "grade_levels" in intervention
        assert "implementation" in intervention
        
        # Verify gateway was called
        mock_generate.assert_called_once()
    
    @pytest.mark.integration
    def test_error_handling_integration(self):
        """Test error handling across the API."""
        # Test validation errors
        invalid_requests = [
            # Missing required fields
            {"emt_scores": {"EMT1": 2.5}},
            
            # Invalid EMT scores
            {
                "emt_scores": {"EMT1": 6.0, "EMT2": 1.8, "EMT3": 3.2, "EMT4": 2.1},
                "class_metadata": {
                    "class_name": "TEST",
                    "grade_level": "3rd Grade",
                    "subject": "Math",
                    "teacher_name": "Teacher",
                    "school_name": "School"
                },
                "deficient_area": "EMT1"
            },
            
            # Invalid deficient area
            {
                "emt_scores": {"EMT1": 2.5, "EMT2": 1.8, "EMT3": 3.2, "EMT4": 2.1},
                "class_metadata": {
                    "class_name": "TEST",
                    "grade_level": "3rd Grade",
                    "subject": "Math",
                    "teacher_name": "Teacher",
                    "school_name": "School"
                },
                "deficient_area": "INVALID"
            }
        ]
        
        for invalid_request in invalid_requests:
            response = self.client.post("/generate-intervention", json=invalid_request)
            assert response.status_code == 422
            data = response.json()
            assert "detail" in data
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        def make_request():
            request_data = {
                "emt_scores": {
                    "EMT1": 2.5,
                    "EMT2": 1.8,
                    "EMT3": 3.2,
                    "EMT4": 2.1
                },
                "class_metadata": {
                    "class_name": "TEST",
                    "grade_level": "3rd Grade",
                    "subject": "Math",
                    "teacher_name": "Teacher",
                    "school_name": "School"
                },
                "deficient_area": "EMT2"
            }
            
            with patch('app.llm.intervention_gateway.InterventionGateway.generate_intervention_plan') as mock_generate:
                mock_response = MagicMock()
                mock_response.analysis = "Test analysis"
                mock_response.strategies = []
                mock_response.timeline = {}
                mock_response.success_metrics = {}
                mock_generate.return_value = mock_response
                
                response = self.client.post("/generate-intervention", json=request_data)
                return response.status_code
        
        # Execute multiple concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        assert all(status == 200 for status in results)
    
    @pytest.mark.integration
    def test_api_documentation_integration(self):
        """Test API documentation endpoints."""
        # Test OpenAPI schema
        response = self.client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
        
        # Verify key endpoints are documented
        paths = schema["paths"]
        assert "/health" in paths
        assert "/generate-intervention" in paths
        assert "/generate-curriculum" in paths
        
        # Test Swagger UI
        response = self.client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    @pytest.mark.integration
    def test_content_type_handling(self):
        """Test different content types and headers."""
        # Test JSON content type
        request_data = {
            "emt_scores": {"EMT1": 2.5, "EMT2": 1.8, "EMT3": 3.2, "EMT4": 2.1},
            "class_metadata": {
                "class_name": "TEST",
                "grade_level": "3rd Grade",
                "subject": "Math",
                "teacher_name": "Teacher",
                "school_name": "School"
            },
            "deficient_area": "EMT2"
        }
        
        with patch('app.llm.intervention_gateway.InterventionGateway.generate_intervention_plan') as mock_generate:
            mock_response = MagicMock()
            mock_response.analysis = "Test"
            mock_response.strategies = []
            mock_response.timeline = {}
            mock_response.success_metrics = {}
            mock_generate.return_value = mock_response
            
            # Test with explicit JSON content type
            response = self.client.post(
                "/generate-intervention",
                json=request_data,
                headers={"Content-Type": "application/json"}
            )
            assert response.status_code == 200
            
            # Test response content type
            assert "application/json" in response.headers["content-type"]
    
    @pytest.mark.integration
    def test_large_payload_handling(self):
        """Test handling of large payloads."""
        # Create a large but valid request
        large_class_name = "A" * 1000  # Very long class name
        
        request_data = {
            "emt_scores": {"EMT1": 2.5, "EMT2": 1.8, "EMT3": 3.2, "EMT4": 2.1},
            "class_metadata": {
                "class_name": large_class_name,
                "grade_level": "3rd Grade",
                "subject": "Math",
                "teacher_name": "Teacher",
                "school_name": "School"
            },
            "deficient_area": "EMT2"
        }
        
        with patch('app.llm.intervention_gateway.InterventionGateway.generate_intervention_plan') as mock_generate:
            mock_response = MagicMock()
            mock_response.analysis = "Test"
            mock_response.strategies = []
            mock_response.timeline = {}
            mock_response.success_metrics = {}
            mock_generate.return_value = mock_response
            
            response = self.client.post("/generate-intervention", json=request_data)
            assert response.status_code == 200
    
    @pytest.mark.integration
    def test_edge_case_scores(self):
        """Test edge cases for score values."""
        edge_cases = [
            # Minimum values
            {"EMT1": 1.0, "EMT2": 1.0, "EMT3": 1.0, "EMT4": 1.0},
            # Maximum values
            {"EMT1": 5.0, "EMT2": 5.0, "EMT3": 5.0, "EMT4": 5.0},
            # Mixed extreme values
            {"EMT1": 1.0, "EMT2": 5.0, "EMT3": 1.0, "EMT4": 5.0},
            # Decimal precision
            {"EMT1": 2.123, "EMT2": 3.456, "EMT3": 4.789, "EMT4": 1.234}
        ]
        
        for scores in edge_cases:
            request_data = {
                "emt_scores": scores,
                "class_metadata": {
                    "class_name": "TEST",
                    "grade_level": "3rd Grade",
                    "subject": "Math",
                    "teacher_name": "Teacher",
                    "school_name": "School"
                },
                "deficient_area": "EMT1"
            }
            
            with patch('app.llm.intervention_gateway.InterventionGateway.generate_intervention_plan') as mock_generate:
                mock_response = MagicMock()
                mock_response.analysis = "Test"
                mock_response.strategies = []
                mock_response.timeline = {}
                mock_response.success_metrics = {}
                mock_generate.return_value = mock_response
                
                response = self.client.post("/generate-intervention", json=request_data)
                assert response.status_code == 200
    
    @pytest.mark.integration
    @patch('app.llm.intervention_gateway.InterventionGateway.generate_intervention_plan')
    @patch('app.llm.curriculum_gateway.CurriculumGateway.generate_curriculum_interventions')
    def test_multiple_endpoint_workflow(self, mock_curriculum, mock_intervention):
        """Test workflow using multiple endpoints."""
        # Mock responses
        mock_intervention_response = MagicMock()
        mock_intervention_response.analysis = "Test analysis"
        mock_intervention_response.strategies = []
        mock_intervention_response.timeline = {}
        mock_intervention_response.success_metrics = {}
        mock_intervention.return_value = mock_intervention_response
        
        mock_curriculum_response = MagicMock()
        mock_curriculum_response.recommended_interventions = []
        mock_curriculum.return_value = mock_curriculum_response
        
        # First, generate intervention
        intervention_request = {
            "emt_scores": {"EMT1": 2.5, "EMT2": 1.8, "EMT3": 3.2, "EMT4": 2.1},
            "class_metadata": {
                "class_name": "TEST",
                "grade_level": "3rd Grade",
                "subject": "Math",
                "teacher_name": "Teacher",
                "school_name": "School"
            },
            "deficient_area": "EMT2"
        }
        
        response1 = self.client.post("/generate-intervention", json=intervention_request)
        assert response1.status_code == 200
        
        # Then, generate curriculum
        curriculum_request = {
            "skill_areas": ["READING_COMPREHENSION"],
            "grade_levels": ["GRADE_3"],
            "scores": {
                "reading_comprehension": 2.5,
                "mathematical_reasoning": 3.0,
                "scientific_inquiry": 2.8,
                "writing_skills": 3.2,
                "critical_thinking": 2.9
            },
            "class_metadata": {
                "class_name": "TEST",
                "grade_level": "3rd Grade",
                "subject": "Reading",
                "teacher_name": "Teacher",
                "school_name": "School"
            }
        }
        
        response2 = self.client.post("/generate-curriculum", json=curriculum_request)
        assert response2.status_code == 200
        
        # Both endpoints should have been called
        mock_intervention.assert_called_once()
        mock_curriculum.assert_called_once()
    
    @pytest.mark.integration
    def test_response_time_performance(self):
        """Test API response time performance."""
        request_data = {
            "emt_scores": {"EMT1": 2.5, "EMT2": 1.8, "EMT3": 3.2, "EMT4": 2.1},
            "class_metadata": {
                "class_name": "TEST",
                "grade_level": "3rd Grade",
                "subject": "Math",
                "teacher_name": "Teacher",
                "school_name": "School"
            },
            "deficient_area": "EMT2"
        }
        
        with patch('app.llm.intervention_gateway.InterventionGateway.generate_intervention_plan') as mock_generate:
            mock_response = MagicMock()
            mock_response.analysis = "Test"
            mock_response.strategies = []
            mock_response.timeline = {}
            mock_response.success_metrics = {}
            mock_generate.return_value = mock_response
            
            start_time = time.time()
            response = self.client.post("/generate-intervention", json=request_data)
            end_time = time.time()
            
            assert response.status_code == 200
            
            # Response should be reasonably fast (under 5 seconds for mocked response)
            response_time = end_time - start_time
            assert response_time < 5.0 