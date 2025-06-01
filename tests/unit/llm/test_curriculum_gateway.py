"""Tests for app.llm.curriculum_gateway module."""

import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import HTTPException

from app.llm.curriculum_gateway import CurriculumGateway
from app.schemas.curriculum import (
    CurriculumRequest, CurriculumResponse, CurriculumIntervention,
    SkillArea, GradeLevel, Implementation
)


class TestCurriculumGateway:
    """Test cases for CurriculumGateway class."""

    def test_init(self):
        """Test CurriculumGateway initialization."""
        gateway = CurriculumGateway()
        assert gateway is not None

    @pytest.mark.asyncio
    async def test_generate_curriculum_interventions_success(self, sample_curriculum_request):
        """Test successful curriculum intervention generation."""
        gateway = CurriculumGateway()
        
        # Mock the LLM response
        mock_response = {
            "recommended_interventions": [
                {
                    "title": "Guided Reading Comprehension",
                    "description": "Structured reading sessions with comprehension questions",
                    "skill_areas": ["READING_COMPREHENSION"],
                    "grade_levels": ["ELEMENTARY"],
                    "implementation": {
                        "duration": "4 weeks",
                        "frequency": "3 times per week",
                        "group_size": "4-6 students",
                        "materials": ["Reading books", "Comprehension worksheets"],
                        "steps": [
                            "Select appropriate reading material",
                            "Guide students through reading",
                            "Ask comprehension questions"
                        ]
                    }
                }
            ]
        }
        
        with patch.object(gateway, '_call_llm', new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = json.dumps(mock_response)
            
            result = await gateway.generate_curriculum_interventions(sample_curriculum_request)
            
            assert isinstance(result, CurriculumResponse)
            assert len(result.recommended_interventions) == 1
            
            intervention = result.recommended_interventions[0]
            assert intervention.title == "Guided Reading Comprehension"
            assert SkillArea.READING_COMPREHENSION in intervention.skill_areas
            assert GradeLevel.ELEMENTARY in intervention.grade_levels

    @pytest.mark.asyncio
    async def test_generate_curriculum_interventions_invalid_json(self, sample_curriculum_request):
        """Test curriculum intervention generation with invalid JSON response."""
        gateway = CurriculumGateway()
        
        with patch.object(gateway, '_call_llm', new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = "Invalid JSON response"
            
            with pytest.raises(HTTPException) as exc_info:
                await gateway.generate_curriculum_interventions(sample_curriculum_request)
            
            assert exc_info.value.status_code == 500
            assert "Failed to parse LLM response" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_generate_curriculum_interventions_missing_field(self, sample_curriculum_request):
        """Test curriculum intervention generation with missing required field."""
        gateway = CurriculumGateway()
        
        # Mock response missing required field
        mock_response = {
            "recommended_interventions": [
                {
                    "title": "Guided Reading Comprehension",
                    # Missing description field
                    "skill_areas": ["READING_COMPREHENSION"],
                    "grade_levels": ["ELEMENTARY"],
                    "implementation": {
                        "duration": "4 weeks",
                        "frequency": "3 times per week",
                        "group_size": "4-6 students",
                        "materials": ["Reading books"],
                        "steps": ["Step 1"]
                    }
                }
            ]
        }
        
        with patch.object(gateway, '_call_llm', new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = json.dumps(mock_response)
            
            with pytest.raises(HTTPException) as exc_info:
                await gateway.generate_curriculum_interventions(sample_curriculum_request)
            
            assert exc_info.value.status_code == 500
            assert "Failed to validate LLM response" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_generate_curriculum_interventions_empty_interventions(self, sample_curriculum_request):
        """Test curriculum intervention generation with empty interventions list."""
        gateway = CurriculumGateway()
        
        mock_response = {
            "recommended_interventions": []
        }
        
        with patch.object(gateway, '_call_llm', new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = json.dumps(mock_response)
            
            result = await gateway.generate_curriculum_interventions(sample_curriculum_request)
            
            assert isinstance(result, CurriculumResponse)
            assert len(result.recommended_interventions) == 0

    @pytest.mark.asyncio
    async def test_generate_curriculum_interventions_multiple_interventions(self, sample_curriculum_request):
        """Test curriculum intervention generation with multiple interventions."""
        gateway = CurriculumGateway()
        
        mock_response = {
            "recommended_interventions": [
                {
                    "title": "Guided Reading Comprehension",
                    "description": "Structured reading sessions",
                    "skill_areas": ["READING_COMPREHENSION"],
                    "grade_levels": ["ELEMENTARY"],
                    "implementation": {
                        "duration": "4 weeks",
                        "frequency": "3 times per week",
                        "group_size": "4-6 students",
                        "materials": ["Books"],
                        "steps": ["Step 1"]
                    }
                },
                {
                    "title": "Math Problem Solving",
                    "description": "Step-by-step math practice",
                    "skill_areas": ["MATHEMATICAL_REASONING"],
                    "grade_levels": ["ELEMENTARY"],
                    "implementation": {
                        "duration": "3 weeks",
                        "frequency": "Daily",
                        "group_size": "2-4 students",
                        "materials": ["Math worksheets"],
                        "steps": ["Step 1", "Step 2"]
                    }
                }
            ]
        }
        
        with patch.object(gateway, '_call_llm', new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = json.dumps(mock_response)
            
            result = await gateway.generate_curriculum_interventions(sample_curriculum_request)
            
            assert isinstance(result, CurriculumResponse)
            assert len(result.recommended_interventions) == 2
            
            titles = [intervention.title for intervention in result.recommended_interventions]
            assert "Guided Reading Comprehension" in titles
            assert "Math Problem Solving" in titles

    @pytest.mark.asyncio
    async def test_generate_curriculum_interventions_invalid_skill_area(self, sample_curriculum_request):
        """Test curriculum intervention generation with invalid skill area."""
        gateway = CurriculumGateway()
        
        mock_response = {
            "recommended_interventions": [
                {
                    "title": "Test Intervention",
                    "description": "Test description",
                    "skill_areas": ["INVALID_SKILL_AREA"],
                    "grade_levels": ["ELEMENTARY"],
                    "implementation": {
                        "duration": "4 weeks",
                        "frequency": "3 times per week",
                        "group_size": "4-6 students",
                        "materials": ["Materials"],
                        "steps": ["Step 1"]
                    }
                }
            ]
        }
        
        with patch.object(gateway, '_call_llm', new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = json.dumps(mock_response)
            
            with pytest.raises(HTTPException) as exc_info:
                await gateway.generate_curriculum_interventions(sample_curriculum_request)
            
            assert exc_info.value.status_code == 500
            assert "Failed to validate LLM response" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_generate_curriculum_interventions_invalid_grade_level(self, sample_curriculum_request):
        """Test curriculum intervention generation with invalid grade level."""
        gateway = CurriculumGateway()
        
        mock_response = {
            "recommended_interventions": [
                {
                    "title": "Test Intervention",
                    "description": "Test description",
                    "skill_areas": ["READING_COMPREHENSION"],
                    "grade_levels": ["INVALID_GRADE"],
                    "implementation": {
                        "duration": "4 weeks",
                        "frequency": "3 times per week",
                        "group_size": "4-6 students",
                        "materials": ["Materials"],
                        "steps": ["Step 1"]
                    }
                }
            ]
        }
        
        with patch.object(gateway, '_call_llm', new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = json.dumps(mock_response)
            
            with pytest.raises(HTTPException) as exc_info:
                await gateway.generate_curriculum_interventions(sample_curriculum_request)
            
            assert exc_info.value.status_code == 500
            assert "Failed to validate LLM response" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_call_llm_success(self):
        """Test successful LLM call."""
        gateway = CurriculumGateway()
        
        mock_response = MagicMock()
        mock_response.text = "Test response from LLM"
        
        with patch('google.generativeai.GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model.generate_content.return_value = mock_response
            mock_model_class.return_value = mock_model
            
            result = await gateway._call_llm("Test prompt")
            
            assert result == "Test response from LLM"
            mock_model.generate_content.assert_called_once_with("Test prompt")

    @pytest.mark.asyncio
    async def test_call_llm_exception(self):
        """Test LLM call with exception."""
        gateway = CurriculumGateway()
        
        with patch('google.generativeai.GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model.generate_content.side_effect = Exception("LLM Error")
            mock_model_class.return_value = mock_model
            
            with pytest.raises(HTTPException) as exc_info:
                await gateway._call_llm("Test prompt")
            
            assert exc_info.value.status_code == 500
            assert "LLM generation failed" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_generate_curriculum_interventions_llm_exception(self, sample_curriculum_request):
        """Test curriculum intervention generation when LLM call fails."""
        gateway = CurriculumGateway()
        
        with patch.object(gateway, '_call_llm', new_callable=AsyncMock) as mock_llm:
            mock_llm.side_effect = HTTPException(status_code=500, detail="LLM Error")
            
            with pytest.raises(HTTPException) as exc_info:
                await gateway.generate_curriculum_interventions(sample_curriculum_request)
            
            assert exc_info.value.status_code == 500
            assert "LLM Error" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_generate_curriculum_interventions_complex_implementation(self, sample_curriculum_request):
        """Test curriculum intervention generation with complex implementation details."""
        gateway = CurriculumGateway()
        
        mock_response = {
            "recommended_interventions": [
                {
                    "title": "Advanced Reading Program",
                    "description": "Comprehensive reading intervention with multiple components",
                    "skill_areas": ["READING_COMPREHENSION", "CRITICAL_THINKING"],
                    "grade_levels": ["ELEMENTARY", "MIDDLE_SCHOOL"],
                    "implementation": {
                        "duration": "8 weeks",
                        "frequency": "Daily sessions of 45 minutes",
                        "group_size": "Small groups of 3-5 students",
                        "materials": [
                            "Leveled reading books",
                            "Comprehension worksheets",
                            "Digital reading platform",
                            "Assessment rubrics"
                        ],
                        "steps": [
                            "Assess current reading level",
                            "Select appropriate materials",
                            "Conduct guided reading sessions",
                            "Practice comprehension strategies",
                            "Monitor progress weekly",
                            "Adjust instruction based on data"
                        ]
                    }
                }
            ]
        }
        
        with patch.object(gateway, '_call_llm', new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = json.dumps(mock_response)
            
            result = await gateway.generate_curriculum_interventions(sample_curriculum_request)
            
            assert isinstance(result, CurriculumResponse)
            assert len(result.recommended_interventions) == 1
            
            intervention = result.recommended_interventions[0]
            assert intervention.title == "Advanced Reading Program"
            assert len(intervention.skill_areas) == 2
            assert len(intervention.grade_levels) == 2
            assert len(intervention.implementation.materials) == 4
            assert len(intervention.implementation.steps) == 6

    @pytest.mark.asyncio
    async def test_generate_curriculum_interventions_prompt_generation(self, sample_curriculum_request):
        """Test that curriculum intervention generation uses correct prompt."""
        gateway = CurriculumGateway()
        
        mock_response = {
            "recommended_interventions": []
        }
        
        with patch.object(gateway, '_call_llm', new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = json.dumps(mock_response)
            
            with patch('app.prompts.curriculum.CurriculumPrompt.get_prompt') as mock_prompt:
                mock_prompt.return_value = "Generated prompt"
                
                await gateway.generate_curriculum_interventions(sample_curriculum_request)
                
                # Verify prompt was generated with correct data
                mock_prompt.assert_called_once()
                call_args = mock_prompt.call_args[0][0]
                
                assert call_args['skill_areas'] == ['READING_COMPREHENSION']
                assert call_args['grade_levels'] == ['ELEMENTARY']
                assert call_args['reading_score'] == 65.0
                assert call_args['math_score'] == 85.0

    @pytest.mark.asyncio
    async def test_generate_curriculum_interventions_safety_validation(self, sample_curriculum_request):
        """Test that curriculum intervention generation includes safety validation."""
        gateway = CurriculumGateway()
        
        # Mock response with potentially harmful content
        mock_response = {
            "recommended_interventions": [
                {
                    "title": "Reading with violence themes",
                    "description": "This intervention includes violence",
                    "skill_areas": ["READING_COMPREHENSION"],
                    "grade_levels": ["ELEMENTARY"],
                    "implementation": {
                        "duration": "4 weeks",
                        "frequency": "3 times per week",
                        "group_size": "4-6 students",
                        "materials": ["Books"],
                        "steps": ["Step 1"]
                    }
                }
            ]
        }
        
        with patch.object(gateway, '_call_llm', new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = json.dumps(mock_response)
            
            with patch('app.safety.guardrails.SafetyValidator.validate_content') as mock_safety:
                mock_safety.return_value = False  # Content is unsafe
                
                with pytest.raises(HTTPException) as exc_info:
                    await gateway.generate_curriculum_interventions(sample_curriculum_request)
                
                assert exc_info.value.status_code == 400
                assert "Content safety validation failed" in str(exc_info.value.detail) 