"""Tests for app.prompts.curriculum module."""

import pytest
import json
from unittest.mock import patch

from app.prompts.curriculum import CurriculumPrompt
from app.schemas.curriculum import SkillArea, GradeLevel


class TestCurriculumPrompt:
    """Test cases for CurriculumPrompt class."""

    def test_skill_area_strategies_structure(self):
        """Test SKILL_AREA_STRATEGIES has correct structure."""
        strategies = CurriculumPrompt.SKILL_AREA_STRATEGIES
        
        # Test all skill areas are present
        expected_areas = [
            "READING_COMPREHENSION",
            "MATHEMATICAL_REASONING", 
            "SCIENTIFIC_INQUIRY",
            "WRITING_SKILLS",
            "CRITICAL_THINKING"
        ]
        
        for area in expected_areas:
            assert area in strategies
            strategy_info = strategies[area]
            
            # Test required fields
            assert "focus" in strategy_info
            assert "description" in strategy_info
            assert "strategies" in strategy_info
            assert isinstance(strategy_info["strategies"], list)
            assert len(strategy_info["strategies"]) > 0
            
            # Test each strategy has required fields
            for strategy in strategy_info["strategies"]:
                assert "activity" in strategy
                assert "implementation" in strategy
                assert "resources" in strategy
                assert isinstance(strategy["implementation"], list)
                assert isinstance(strategy["resources"], list)

    def test_reading_comprehension_strategies(self):
        """Test reading comprehension strategies content."""
        reading = CurriculumPrompt.SKILL_AREA_STRATEGIES["READING_COMPREHENSION"]
        assert reading["focus"] == "Text Understanding and Analysis"
        assert "reading comprehension difficulties" in reading["description"]
        
        # Check specific activities
        activities = [s["activity"] for s in reading["strategies"]]
        assert "Guided Reading Sessions" in activities
        assert "Text Annotation Practice" in activities
        assert "Reading Comprehension Games" in activities

    def test_mathematical_reasoning_strategies(self):
        """Test mathematical reasoning strategies content."""
        math = CurriculumPrompt.SKILL_AREA_STRATEGIES["MATHEMATICAL_REASONING"]
        assert math["focus"] == "Problem-Solving and Logical Thinking"
        assert "mathematical problem-solving difficulties" in math["description"]
        
        # Check specific activities
        activities = [s["activity"] for s in math["strategies"]]
        assert "Step-by-Step Problem Solving" in activities
        assert "Math Manipulatives Practice" in activities
        assert "Real-World Math Applications" in activities

    def test_scientific_inquiry_strategies(self):
        """Test scientific inquiry strategies content."""
        science = CurriculumPrompt.SKILL_AREA_STRATEGIES["SCIENTIFIC_INQUIRY"]
        assert science["focus"] == "Investigation and Discovery"
        assert "scientific thinking and inquiry difficulties" in science["description"]
        
        # Check specific activities
        activities = [s["activity"] for s in science["strategies"]]
        assert "Hands-On Experiments" in activities
        assert "Scientific Method Practice" in activities
        assert "Observation and Recording" in activities

    def test_writing_skills_strategies(self):
        """Test writing skills strategies content."""
        writing = CurriculumPrompt.SKILL_AREA_STRATEGIES["WRITING_SKILLS"]
        assert writing["focus"] == "Expression and Communication"
        assert "written expression and communication difficulties" in writing["description"]
        
        # Check specific activities
        activities = [s["activity"] for s in writing["strategies"]]
        assert "Structured Writing Practice" in activities
        assert "Peer Review Sessions" in activities
        assert "Creative Writing Exercises" in activities

    def test_critical_thinking_strategies(self):
        """Test critical thinking strategies content."""
        critical = CurriculumPrompt.SKILL_AREA_STRATEGIES["CRITICAL_THINKING"]
        assert critical["focus"] == "Analysis and Evaluation"
        assert "critical thinking and analysis difficulties" in critical["description"]
        
        # Check specific activities
        activities = [s["activity"] for s in critical["strategies"]]
        assert "Socratic Questioning" in activities
        assert "Case Study Analysis" in activities
        assert "Debate and Discussion" in activities

    def test_example_response_structure(self):
        """Test EXAMPLE_RESPONSE has correct structure."""
        example = CurriculumPrompt.EXAMPLE_RESPONSE
        
        # Test required fields
        assert "recommended_interventions" in example
        assert isinstance(example["recommended_interventions"], list)
        assert len(example["recommended_interventions"]) > 0
        
        intervention = example["recommended_interventions"][0]
        assert "title" in intervention
        assert "description" in intervention
        assert "skill_areas" in intervention
        assert "grade_levels" in intervention
        assert "implementation" in intervention
        
        # Test implementation structure
        impl = intervention["implementation"]
        assert "duration" in impl
        assert "frequency" in impl
        assert "group_size" in impl
        assert "materials" in impl
        assert "steps" in impl

    def test_format_strategies_for_prompt_reading(self):
        """Test _format_strategies_for_prompt with reading comprehension."""
        strategy_info = CurriculumPrompt.SKILL_AREA_STRATEGIES["READING_COMPREHENSION"]
        formatted = CurriculumPrompt._format_strategies_for_prompt(strategy_info)
        
        assert "Focus: Text Understanding and Analysis" in formatted
        assert "Description: reading comprehension difficulties" in formatted
        assert "Available Strategies:" in formatted
        assert "1. Guided Reading Sessions" in formatted
        assert "Implementation:" in formatted
        assert "Resources:" in formatted

    def test_format_strategies_for_prompt_math(self):
        """Test _format_strategies_for_prompt with mathematical reasoning."""
        strategy_info = CurriculumPrompt.SKILL_AREA_STRATEGIES["MATHEMATICAL_REASONING"]
        formatted = CurriculumPrompt._format_strategies_for_prompt(strategy_info)
        
        assert "Focus: Problem-Solving and Logical Thinking" in formatted
        assert "1. Step-by-Step Problem Solving" in formatted
        assert "2. Math Manipulatives Practice" in formatted
        assert "3. Real-World Math Applications" in formatted

    def test_get_prompt_single_skill_area(self):
        """Test get_prompt with single skill area."""
        data = {
            'skill_areas': ['READING_COMPREHENSION'],
            'grade_levels': ['ELEMENTARY'],
            'reading_score': 65.0,
            'math_score': 85.0,
            'science_score': 80.0,
            'writing_score': 75.0,
            'critical_thinking_score': 70.0
        }
        
        prompt = CurriculumPrompt.get_prompt(data)
        
        # Test basic structure
        assert 'READING_COMPREHENSION' in prompt
        assert 'ELEMENTARY' in prompt
        assert '65.00%' in prompt
        
        # Test reading comprehension specific content
        assert 'Text Understanding and Analysis' in prompt
        assert 'Guided Reading Sessions' in prompt

    def test_get_prompt_multiple_skill_areas(self):
        """Test get_prompt with multiple skill areas."""
        data = {
            'skill_areas': ['READING_COMPREHENSION', 'MATHEMATICAL_REASONING'],
            'grade_levels': ['ELEMENTARY', 'MIDDLE_SCHOOL'],
            'reading_score': 65.0,
            'math_score': 60.0,
            'science_score': 85.0,
            'writing_score': 75.0,
            'critical_thinking_score': 70.0
        }
        
        prompt = CurriculumPrompt.get_prompt(data)
        
        # Test both skill areas are included
        assert 'READING_COMPREHENSION' in prompt
        assert 'MATHEMATICAL_REASONING' in prompt
        assert 'Text Understanding and Analysis' in prompt
        assert 'Problem-Solving and Logical Thinking' in prompt

    def test_get_prompt_all_skill_areas(self):
        """Test get_prompt with all skill areas."""
        data = {
            'skill_areas': [
                'READING_COMPREHENSION',
                'MATHEMATICAL_REASONING',
                'SCIENTIFIC_INQUIRY',
                'WRITING_SKILLS',
                'CRITICAL_THINKING'
            ],
            'grade_levels': ['ELEMENTARY'],
            'reading_score': 65.0,
            'math_score': 60.0,
            'science_score': 55.0,
            'writing_score': 50.0,
            'critical_thinking_score': 45.0
        }
        
        prompt = CurriculumPrompt.get_prompt(data)
        
        # Test all areas are included
        expected_focuses = [
            'Text Understanding and Analysis',
            'Problem-Solving and Logical Thinking',
            'Investigation and Discovery',
            'Expression and Communication',
            'Analysis and Evaluation'
        ]
        
        for focus in expected_focuses:
            assert focus in prompt

    def test_get_prompt_all_grade_levels(self):
        """Test get_prompt with all grade levels."""
        data = {
            'skill_areas': ['READING_COMPREHENSION'],
            'grade_levels': ['ELEMENTARY', 'MIDDLE_SCHOOL', 'HIGH_SCHOOL'],
            'reading_score': 65.0,
            'math_score': 85.0,
            'science_score': 80.0,
            'writing_score': 75.0,
            'critical_thinking_score': 70.0
        }
        
        prompt = CurriculumPrompt.get_prompt(data)
        
        # Test all grade levels are included
        assert 'ELEMENTARY' in prompt
        assert 'MIDDLE_SCHOOL' in prompt
        assert 'HIGH_SCHOOL' in prompt

    def test_get_prompt_invalid_skill_area(self):
        """Test get_prompt with invalid skill area."""
        data = {
            'skill_areas': ['INVALID_SKILL'],
            'grade_levels': ['ELEMENTARY'],
            'reading_score': 65.0,
            'math_score': 85.0,
            'science_score': 80.0,
            'writing_score': 75.0,
            'critical_thinking_score': 70.0
        }
        
        prompt = CurriculumPrompt.get_prompt(data)
        
        # Should contain fallback message
        assert 'No specific strategies available for this skill area' in prompt

    def test_get_prompt_includes_schema(self):
        """Test get_prompt includes JSON schema."""
        data = {
            'skill_areas': ['READING_COMPREHENSION'],
            'grade_levels': ['ELEMENTARY'],
            'reading_score': 65.0,
            'math_score': 85.0,
            'science_score': 80.0,
            'writing_score': 75.0,
            'critical_thinking_score': 70.0
        }
        
        prompt = CurriculumPrompt.get_prompt(data)
        
        # Should contain schema information
        assert '"type": "object"' in prompt
        assert '"properties"' in prompt
        assert '"recommended_interventions"' in prompt

    def test_get_prompt_includes_example(self):
        """Test get_prompt includes example response."""
        data = {
            'skill_areas': ['READING_COMPREHENSION'],
            'grade_levels': ['ELEMENTARY'],
            'reading_score': 65.0,
            'math_score': 85.0,
            'science_score': 80.0,
            'writing_score': 75.0,
            'critical_thinking_score': 70.0
        }
        
        prompt = CurriculumPrompt.get_prompt(data)
        
        # Should contain example response
        assert '"recommended_interventions":' in prompt
        assert '"Guided Reading Comprehension"' in prompt

    def test_get_prompt_safety_guidelines(self):
        """Test get_prompt includes safety guidelines."""
        data = {
            'skill_areas': ['READING_COMPREHENSION'],
            'grade_levels': ['ELEMENTARY'],
            'reading_score': 65.0,
            'math_score': 85.0,
            'science_score': 80.0,
            'writing_score': 75.0,
            'critical_thinking_score': 70.0
        }
        
        prompt = CurriculumPrompt.get_prompt(data)
        
        # Should contain safety guidelines
        assert 'SAFETY GUIDELINES - CRITICAL:' in prompt
        assert 'positive, encouraging, and age-appropriate language' in prompt
        assert 'safe and suitable for the classroom' in prompt

    def test_get_prompt_formatting_requirements(self):
        """Test get_prompt includes formatting requirements."""
        data = {
            'skill_areas': ['READING_COMPREHENSION'],
            'grade_levels': ['ELEMENTARY'],
            'reading_score': 65.0,
            'math_score': 85.0,
            'science_score': 80.0,
            'writing_score': 75.0,
            'critical_thinking_score': 70.0
        }
        
        prompt = CurriculumPrompt.get_prompt(data)
        
        # Should contain formatting requirements
        assert 'IMPORTANT REQUIREMENTS:' in prompt
        assert 'Return ONLY the JSON object' in prompt
        assert 'valid JSON' in prompt

    def test_base_template_placeholders(self):
        """Test BASE_TEMPLATE contains all required placeholders."""
        template = CurriculumPrompt.BASE_TEMPLATE
        
        required_placeholders = [
            '{skill_areas}',
            '{grade_levels}',
            '{reading_score:.2f}',
            '{math_score:.2f}',
            '{science_score:.2f}',
            '{writing_score:.2f}',
            '{critical_thinking_score:.2f}',
            '{focused_strategies}',
            '{schema}',
            '{example}'
        ]
        
        for placeholder in required_placeholders:
            assert placeholder in template

    def test_get_prompt_score_formatting(self):
        """Test get_prompt formats scores correctly."""
        data = {
            'skill_areas': ['READING_COMPREHENSION'],
            'grade_levels': ['ELEMENTARY'],
            'reading_score': 65.123,
            'math_score': 85.456,
            'science_score': 80.789,
            'writing_score': 75.012,
            'critical_thinking_score': 70.345
        }
        
        prompt = CurriculumPrompt.get_prompt(data)
        
        # Test scores are formatted to 2 decimal places
        assert '65.12%' in prompt
        assert '85.46%' in prompt
        assert '80.79%' in prompt
        assert '75.01%' in prompt
        assert '70.35%' in prompt

    def test_get_prompt_empty_skill_areas(self):
        """Test get_prompt with empty skill areas."""
        data = {
            'skill_areas': [],
            'grade_levels': ['ELEMENTARY'],
            'reading_score': 65.0,
            'math_score': 85.0,
            'science_score': 80.0,
            'writing_score': 75.0,
            'critical_thinking_score': 70.0
        }
        
        prompt = CurriculumPrompt.get_prompt(data)
        
        # Should handle empty skill areas gracefully
        assert 'No specific strategies available' in prompt

    def test_get_prompt_mixed_valid_invalid_skill_areas(self):
        """Test get_prompt with mix of valid and invalid skill areas."""
        data = {
            'skill_areas': ['READING_COMPREHENSION', 'INVALID_SKILL'],
            'grade_levels': ['ELEMENTARY'],
            'reading_score': 65.0,
            'math_score': 85.0,
            'science_score': 80.0,
            'writing_score': 75.0,
            'critical_thinking_score': 70.0
        }
        
        prompt = CurriculumPrompt.get_prompt(data)
        
        # Should include valid skill area strategies
        assert 'Text Understanding and Analysis' in prompt
        # Should also include fallback for invalid areas
        assert 'No specific strategies available for this skill area' in prompt 