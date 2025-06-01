"""Tests for curriculum schema models."""

import pytest
from pydantic import ValidationError

from app.schemas.curriculum import (
    CurriculumRequest, CurriculumResponse, CurriculumIntervention,
    SkillArea, GradeLevel, Implementation
)


class TestCurriculumSchemas:
    """Test cases for curriculum schema models."""
    
    def test_skill_area_enum_values(self):
        """Test SkillArea enum has correct values."""
        expected_values = [
            "emotional_awareness",
            "emotional_regulation", 
            "anger_management"
        ]
        
        actual_values = [skill.value for skill in SkillArea]
        assert set(actual_values) == set(expected_values)
    
    def test_grade_level_enum_values(self):
        """Test GradeLevel enum has correct values."""
        expected_values = [
            "1",
            "2",
            "5"
        ]
        
        actual_values = [grade.value for grade in GradeLevel]
        assert set(actual_values) == set(expected_values)
    
    def test_curriculum_request_valid(self):
        """Test valid CurriculumRequest creation."""
        request = CurriculumRequest(
            skill_areas=[SkillArea.EMOTIONAL_AWARENESS],
            grade_level=GradeLevel.GRADE_1,
            score=75.5
        )
        
        assert request.skill_areas == [SkillArea.EMOTIONAL_AWARENESS]
        assert request.grade_level == GradeLevel.GRADE_1
        assert request.score == 75.5
    
    def test_curriculum_request_multiple_skill_areas(self):
        """Test CurriculumRequest with multiple skill areas."""
        request = CurriculumRequest(
            skill_areas=[
                SkillArea.EMOTIONAL_AWARENESS,
                SkillArea.EMOTIONAL_REGULATION
            ],
            grade_level=GradeLevel.GRADE_2,
            score=68.0
        )
        
        assert len(request.skill_areas) == 2
        assert SkillArea.EMOTIONAL_AWARENESS in request.skill_areas
        assert SkillArea.EMOTIONAL_REGULATION in request.skill_areas
    
    def test_curriculum_request_invalid_score_high(self):
        """Test CurriculumRequest with score too high."""
        with pytest.raises(ValidationError) as exc_info:
            CurriculumRequest(
                skill_areas=[SkillArea.EMOTIONAL_AWARENESS],
                grade_level=GradeLevel.GRADE_1,
                score=150.0  # Invalid: > 100
            )
        
        assert "Input should be less than or equal to 100" in str(exc_info.value)
    
    def test_curriculum_request_invalid_score_low(self):
        """Test CurriculumRequest with score too low."""
        with pytest.raises(ValidationError) as exc_info:
            CurriculumRequest(
                skill_areas=[SkillArea.EMOTIONAL_AWARENESS],
                grade_level=GradeLevel.GRADE_1,
                score=-10.0  # Invalid: < 0
            )
        
        assert "Input should be greater than or equal to 0" in str(exc_info.value)
    
    def test_curriculum_request_empty_skill_areas(self):
        """Test CurriculumRequest with empty skill areas."""
        # Empty skill areas list is actually valid in the current schema
        request = CurriculumRequest(
            skill_areas=[],  # Valid: empty list is allowed
            grade_level=GradeLevel.GRADE_1,
            score=75.0
        )
        
        assert len(request.skill_areas) == 0
        assert request.grade_level == GradeLevel.GRADE_1
        assert request.score == 75.0
    
    def test_implementation_valid(self):
        """Test valid Implementation creation."""
        implementation = Implementation(
            steps=["Step 1", "Step 2", "Step 3"],
            materials=["Books", "Worksheets"],
            time_allocation="30 minutes"
        )
        
        assert len(implementation.steps) == 3
        assert len(implementation.materials) == 2
        assert implementation.time_allocation == "30 minutes"
    
    def test_implementation_minimal(self):
        """Test Implementation with only required fields."""
        implementation = Implementation(
            steps=["Step 1"]
        )
        
        assert len(implementation.steps) == 1
        assert implementation.materials is None
        assert implementation.time_allocation is None
    
    def test_curriculum_intervention_valid(self):
        """Test valid CurriculumIntervention creation."""
        implementation = Implementation(
            steps=["Step 1"],
            materials=["Books"],
            time_allocation="30 minutes"
        )
        
        intervention = CurriculumIntervention(
            name="Emotion Recognition Program",
            grade_levels=[GradeLevel.GRADE_1],
            skill_area=SkillArea.EMOTIONAL_AWARENESS,
            summary="A structured emotion recognition intervention",
            implementation=implementation,
            intended_purpose="Improve emotional awareness skills"
        )
        
        assert intervention.name == "Emotion Recognition Program"
        assert intervention.summary == "A structured emotion recognition intervention"
        assert len(intervention.grade_levels) == 1
        assert intervention.skill_area == SkillArea.EMOTIONAL_AWARENESS
        assert intervention.intended_purpose == "Improve emotional awareness skills"
    
    def test_curriculum_response_valid(self):
        """Test valid CurriculumResponse creation."""
        implementation = Implementation(
            steps=["Step 1"],
            materials=["Books"],
            time_allocation="30 minutes"
        )
        
        intervention = CurriculumIntervention(
            name="Test Intervention",
            grade_levels=[GradeLevel.GRADE_1],
            skill_area=SkillArea.EMOTIONAL_AWARENESS,
            summary="Test description",
            implementation=implementation,
            intended_purpose="Test purpose"
        )
        
        response = CurriculumResponse(
            recommended_interventions=[intervention],
            skill_focus=["emotional_awareness"],
            implementation_order=["Test Intervention"]
        )
        
        assert len(response.recommended_interventions) == 1
        assert response.recommended_interventions[0].name == "Test Intervention"
        assert len(response.skill_focus) == 1
        assert len(response.implementation_order) == 1
    
    def test_curriculum_response_empty_interventions(self):
        """Test CurriculumResponse with empty interventions list."""
        response = CurriculumResponse(
            recommended_interventions=[],
            skill_focus=[],
            implementation_order=[]
        )
        
        assert len(response.recommended_interventions) == 0
        assert len(response.skill_focus) == 0
        assert len(response.implementation_order) == 0
    
    def test_curriculum_request_json_serialization(self):
        """Test CurriculumRequest JSON serialization."""
        request = CurriculumRequest(
            skill_areas=[SkillArea.EMOTIONAL_AWARENESS],
            grade_level=GradeLevel.GRADE_1,
            score=75.0
        )
        
        json_data = request.model_dump()
        
        assert json_data["skill_areas"] == ["emotional_awareness"]
        assert json_data["grade_level"] == "1"
        assert json_data["score"] == 75.0
    
    def test_curriculum_response_json_serialization(self):
        """Test CurriculumResponse JSON serialization."""
        implementation = Implementation(
            steps=["Step 1"],
            materials=["Books"],
            time_allocation="30 minutes"
        )
        
        intervention = CurriculumIntervention(
            name="Test Intervention",
            grade_levels=[GradeLevel.GRADE_1],
            skill_area=SkillArea.EMOTIONAL_AWARENESS,
            summary="Test description",
            implementation=implementation,
            intended_purpose="Test purpose"
        )
        
        response = CurriculumResponse(
            recommended_interventions=[intervention],
            skill_focus=["emotional_awareness"],
            implementation_order=["Test Intervention"]
        )
        
        json_data = response.model_dump()
        
        assert len(json_data["recommended_interventions"]) == 1
        assert json_data["recommended_interventions"][0]["name"] == "Test Intervention"
        assert json_data["recommended_interventions"][0]["skill_area"] == "emotional_awareness"
    
    def test_skill_area_string_conversion(self):
        """Test SkillArea string conversion."""
        skill = SkillArea.EMOTIONAL_AWARENESS
        assert str(skill) == "SkillArea.EMOTIONAL_AWARENESS"
        assert skill.value == "emotional_awareness"
    
    def test_grade_level_string_conversion(self):
        """Test GradeLevel string conversion."""
        grade = GradeLevel.GRADE_1
        assert str(grade) == "GradeLevel.GRADE_1"
        assert grade.value == "1"
    
    def test_curriculum_request_edge_case_scores(self):
        """Test CurriculumRequest with edge case scores."""
        # Test minimum valid score
        request_min = CurriculumRequest(
            skill_areas=[SkillArea.EMOTIONAL_AWARENESS],
            grade_level=GradeLevel.GRADE_1,
            score=0.0
        )
        assert request_min.score == 0.0
        
        # Test maximum valid score
        request_max = CurriculumRequest(
            skill_areas=[SkillArea.EMOTIONAL_AWARENESS],
            grade_level=GradeLevel.GRADE_1,
            score=100.0
        )
        assert request_max.score == 100.0
    
    def test_implementation_empty_lists(self):
        """Test Implementation with empty lists."""
        implementation = Implementation(
            steps=["Step 1"],
            materials=[],  # Empty list should be valid
            time_allocation="30 minutes"
        )
        
        assert len(implementation.materials) == 0
        assert len(implementation.steps) == 1
    
    def test_curriculum_intervention_multiple_grades(self):
        """Test CurriculumIntervention with multiple grade levels."""
        implementation = Implementation(steps=["Step 1"])
        
        intervention = CurriculumIntervention(
            name="Multi-Grade Intervention",
            grade_levels=[GradeLevel.GRADE_1, GradeLevel.GRADE_2],
            skill_area=SkillArea.EMOTIONAL_REGULATION,
            summary="Intervention for multiple grades",
            implementation=implementation,
            intended_purpose="Cross-grade emotional regulation"
        )
        
        assert len(intervention.grade_levels) == 2
        assert GradeLevel.GRADE_1 in intervention.grade_levels
        assert GradeLevel.GRADE_2 in intervention.grade_levels 