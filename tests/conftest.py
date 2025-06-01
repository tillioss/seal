"""Pytest configuration and shared fixtures."""

import os
import sys
import pytest
from unittest.mock import Mock, patch
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set test environment variables
os.environ["GOOGLE_API_KEY"] = "test_api_key"
os.environ["ENVIRONMENT"] = "test"
os.environ["LLM_PROVIDER"] = "gemini"

@pytest.fixture
def mock_genai():
    """Mock Google Generative AI for testing."""
    with patch('google.generativeai.configure') as mock_configure, \
         patch('google.generativeai.GenerativeModel') as mock_model_class:
        
        # Mock model instance
        mock_model = Mock()
        mock_model_class.return_value = mock_model
        
        # Mock response
        mock_response = Mock()
        mock_response.text = '{"test": "response"}'
        mock_response.candidates = [Mock()]
        mock_response.candidates[0].content.parts = [Mock()]
        mock_response.candidates[0].content.parts[0].text = '{"test": "response"}'
        
        mock_model.generate_content.return_value = mock_response
        
        yield {
            'configure': mock_configure,
            'model_class': mock_model_class,
            'model': mock_model,
            'response': mock_response
        }

@pytest.fixture
def sample_emt_scores():
    """Sample EMT scores for testing."""
    return {
        "EMT1": [65.0, 70.0, 68.0, 72.0, 69.0],
        "EMT2": [58.0, 62.0, 60.0, 64.0, 61.0],
        "EMT3": [72.0, 75.0, 70.0, 78.0, 74.0],
        "EMT4": [63.0, 65.0, 64.0, 67.0, 66.0]
    }

@pytest.fixture
def sample_class_metadata():
    """Sample class metadata for testing."""
    return {
        "class_id": "TEST_CLASS_001",
        "deficient_area": "EMT2",
        "num_students": 25
    }

@pytest.fixture
def sample_intervention_request(sample_emt_scores, sample_class_metadata):
    """Sample intervention request for testing."""
    from app.schemas import InterventionRequest, EMTScores, ClassMetadata
    
    return InterventionRequest(
        scores=EMTScores(**sample_emt_scores),
        metadata=ClassMetadata(**sample_class_metadata)
    )

@pytest.fixture
def sample_curriculum_request():
    """Sample curriculum request for testing."""
    from app.schemas.curriculum import CurriculumRequest, SkillArea, GradeLevel
    
    return CurriculumRequest(
        grade_level=GradeLevel.GRADE_2,
        skill_areas=[SkillArea.EMOTIONAL_AWARENESS, SkillArea.EMOTIONAL_REGULATION],
        score=65.5
    )

@pytest.fixture
def mock_intervention_response():
    """Mock intervention response for testing."""
    return {
        "classId": "TEST_CLASS_001",
        "numberOfStudents": 25,
        "deficientArea": "EMT2",
        "strategies": [
            {
                "title": "Story Time Emotions",
                "implementationPlan": [
                    "Read emotional stories",
                    "Discuss character feelings",
                    "Practice expression matching"
                ],
                "successMetrics": [
                    "Improved emotion recognition",
                    "Better story comprehension"
                ]
            }
        ],
        "timeline": [
            {
                "week": 1,
                "activities": ["Introduce story-based activities", "Basic emotion identification"]
            },
            {
                "week": 2,
                "activities": ["Advanced story discussions", "Expression practice"]
            }
        ],
        "overallSuccessMetrics": [
            "15% improvement in EMT2 scores",
            "Increased student engagement"
        ]
    }

@pytest.fixture
def mock_curriculum_response():
    """Mock curriculum response for testing."""
    return {
        "recommended_interventions": [
            {
                "name": "Emotion Recognition Games",
                "grade_levels": ["2"],
                "skill_area": "emotional_awareness",
                "summary": "Interactive games to help students identify emotions",
                "implementation": {
                    "steps": ["Set up game materials", "Explain rules", "Practice sessions"],
                    "materials": ["Emotion cards", "Timer"],
                    "time_allocation": "30 minutes"
                },
                "intended_purpose": "Improve emotion recognition skills"
            }
        ],
        "skill_focus": ["emotional_awareness", "emotional_regulation"],
        "implementation_order": ["Emotion Recognition Games"]
    }

@pytest.fixture
def mock_safety_validator():
    """Mock safety validator for testing."""
    with patch('app.safety.guardrails.LLMSafetyValidator') as mock_validator_class:
        mock_validator = Mock()
        mock_validator.validate_content.return_value = (True, None)
        mock_validator_class.return_value = mock_validator
        yield mock_validator 