"""Tests for app.prompts.intervention module."""

import pytest
import json
from unittest.mock import patch

from app.prompts.intervention import InterventionPrompt
from app.schemas import InterventionPlan


class TestInterventionPrompt:
    """Test cases for InterventionPrompt class."""

    def test_emt_strategies_structure(self):
        """Test EMT_STRATEGIES has correct structure."""
        strategies = InterventionPrompt.EMT_STRATEGIES
        
        # Test all EMT areas are present
        expected_areas = ["EMT1", "EMT2", "EMT3", "EMT4"]
        assert all(area in strategies for area in expected_areas)
        
        # Test each area has required fields
        for area, strategy_info in strategies.items():
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

    def test_emt1_strategies_content(self):
        """Test EMT1 strategies content."""
        emt1 = InterventionPrompt.EMT_STRATEGIES["EMT1"]
        assert emt1["focus"] == "Visual Emotion Recognition"
        assert "Visual-to-visual emotion matching difficulties" in emt1["description"]
        
        # Check specific activities
        activities = [s["activity"] for s in emt1["strategies"]]
        assert "Emotion Flashcard Pairs" in activities
        assert "Mirror Expression Practice" in activities
        assert "Digital Emotion Matching Games" in activities

    def test_emt2_strategies_content(self):
        """Test EMT2 strategies content."""
        emt2 = InterventionPrompt.EMT_STRATEGIES["EMT2"]
        assert emt2["focus"] == "Situation-to-Expression Connection"
        assert "Connecting verbal contexts to visual expressions" in emt2["description"]
        
        # Check specific activities
        activities = [s["activity"] for s in emt2["strategies"]]
        assert "Story-Based Emotion Discussions" in activities
        assert "Scenario Cards with Emotional Contexts" in activities
        assert "Role-Playing Emotional Situations" in activities

    def test_emt3_strategies_content(self):
        """Test EMT3 strategies content."""
        emt3 = InterventionPrompt.EMT_STRATEGIES["EMT3"]
        assert emt3["focus"] == "Emotion Vocabulary Building"
        assert "Visual to verbal emotion labeling difficulties" in emt3["description"]
        
        # Check specific activities
        activities = [s["activity"] for s in emt3["strategies"]]
        assert "Emotion Word Wall" in activities
        assert "Expression-Label Matching Games" in activities
        assert "Emotion Vocabulary Journals" in activities

    def test_emt4_strategies_content(self):
        """Test EMT4 strategies content."""
        emt4 = InterventionPrompt.EMT_STRATEGIES["EMT4"]
        assert emt4["focus"] == "Emotion Label Comprehension"
        assert "Verbal label to visual expression matching difficulties" in emt4["description"]
        
        # Check specific activities
        activities = [s["activity"] for s in emt4["strategies"]]
        assert "Emotion Word-to-Face Games" in activities
        assert "Verbal Emotion Cues Practice" in activities
        assert "Group Emotion Word Activities" in activities

    def test_example_response_structure(self):
        """Test EXAMPLE_RESPONSE has correct structure."""
        example = InterventionPrompt.EXAMPLE_RESPONSE
        
        # Test required fields
        assert "analysis" in example
        assert "strategies" in example
        assert "timeline" in example
        assert "success_metrics" in example
        
        # Test strategies structure
        assert isinstance(example["strategies"], list)
        assert len(example["strategies"]) > 0
        
        strategy = example["strategies"][0]
        assert "activity" in strategy
        assert "implementation" in strategy
        assert "expected_outcomes" in strategy
        assert "time_allocation" in strategy
        assert "resources" in strategy
        
        # Test timeline structure
        assert isinstance(example["timeline"], dict)
        assert "week1" in example["timeline"]
        
        # Test success metrics structure
        metrics = example["success_metrics"]
        assert "quantitative" in metrics
        assert "qualitative" in metrics
        assert "assessment_methods" in metrics

    def test_format_strategies_for_prompt_emt1(self):
        """Test _format_strategies_for_prompt with EMT1."""
        strategy_info = InterventionPrompt.EMT_STRATEGIES["EMT1"]
        formatted = InterventionPrompt._format_strategies_for_prompt(strategy_info)
        
        assert "Focus: Visual Emotion Recognition" in formatted
        assert "Description: Visual-to-visual emotion matching difficulties" in formatted
        assert "Available Strategies:" in formatted
        assert "1. Emotion Flashcard Pairs" in formatted
        assert "Implementation:" in formatted
        assert "Resources:" in formatted

    def test_format_strategies_for_prompt_emt2(self):
        """Test _format_strategies_for_prompt with EMT2."""
        strategy_info = InterventionPrompt.EMT_STRATEGIES["EMT2"]
        formatted = InterventionPrompt._format_strategies_for_prompt(strategy_info)
        
        assert "Focus: Situation-to-Expression Connection" in formatted
        assert "1. Story-Based Emotion Discussions" in formatted
        assert "2. Scenario Cards with Emotional Contexts" in formatted
        assert "3. Role-Playing Emotional Situations" in formatted

    def test_format_strategies_for_prompt_emt3(self):
        """Test _format_strategies_for_prompt with EMT3."""
        strategy_info = InterventionPrompt.EMT_STRATEGIES["EMT3"]
        formatted = InterventionPrompt._format_strategies_for_prompt(strategy_info)
        
        assert "Focus: Emotion Vocabulary Building" in formatted
        assert "1. Emotion Word Wall" in formatted
        assert "2. Expression-Label Matching Games" in formatted
        assert "3. Emotion Vocabulary Journals" in formatted

    def test_format_strategies_for_prompt_emt4(self):
        """Test _format_strategies_for_prompt with EMT4."""
        strategy_info = InterventionPrompt.EMT_STRATEGIES["EMT4"]
        formatted = InterventionPrompt._format_strategies_for_prompt(strategy_info)
        
        assert "Focus: Emotion Label Comprehension" in formatted
        assert "1. Emotion Word-to-Face Games" in formatted
        assert "2. Verbal Emotion Cues Practice" in formatted
        assert "3. Group Emotion Word Activities" in formatted

    def test_get_prompt_gemini_provider(self):
        """Test get_prompt with Gemini provider."""
        data = {
            'class_id': 'TEST_001',
            'num_students': 25,
            'deficient_area': 'EMT1',
            'emt1_avg': 45.0,
            'emt2_avg': 75.0,
            'emt3_avg': 70.0,
            'emt4_avg': 68.0
        }
        
        prompt = InterventionPrompt.get_prompt('gemini', data)
        
        # Test basic structure
        assert 'TEST_001' in prompt
        assert '25' in prompt
        assert 'EMT1' in prompt
        assert '45.00%' in prompt
        
        # Test EMT1 specific content
        assert 'Visual Emotion Recognition' in prompt
        assert 'Emotion Flashcard Pairs' in prompt
        
        # Test Gemini-specific content
        assert 'FINAL CHECK:' in prompt
        assert 'opening curly brace' in prompt

    def test_get_prompt_openai_provider(self):
        """Test get_prompt with OpenAI provider."""
        data = {
            'class_id': 'TEST_002',
            'num_students': 30,
            'deficient_area': 'EMT2',
            'emt1_avg': 75.0,
            'emt2_avg': 45.0,
            'emt3_avg': 70.0,
            'emt4_avg': 68.0
        }
        
        prompt = InterventionPrompt.get_prompt('openai', data)
        
        # Test basic structure
        assert 'TEST_002' in prompt
        assert '30' in prompt
        assert 'EMT2' in prompt
        assert '45.00%' in prompt
        
        # Test EMT2 specific content
        assert 'Situation-to-Expression Connection' in prompt
        assert 'Story-Based Emotion Discussions' in prompt
        
        # Test OpenAI-specific content
        assert 'Format your response as a JSON object' in prompt

    def test_get_prompt_default_provider(self):
        """Test get_prompt with unknown provider defaults to base template."""
        data = {
            'class_id': 'TEST_003',
            'num_students': 20,
            'deficient_area': 'EMT3',
            'emt1_avg': 70.0,
            'emt2_avg': 68.0,
            'emt3_avg': 45.0,
            'emt4_avg': 75.0
        }
        
        prompt = InterventionPrompt.get_prompt('unknown_provider', data)
        
        # Test basic structure
        assert 'TEST_003' in prompt
        assert '20' in prompt
        assert 'EMT3' in prompt
        assert '45.00%' in prompt
        
        # Test EMT3 specific content
        assert 'Emotion Vocabulary Building' in prompt
        assert 'Emotion Word Wall' in prompt

    def test_get_prompt_all_emt_areas(self):
        """Test get_prompt with all EMT areas as deficient."""
        base_data = {
            'class_id': 'TEST_ALL',
            'num_students': 25,
            'emt1_avg': 70.0,
            'emt2_avg': 70.0,
            'emt3_avg': 70.0,
            'emt4_avg': 70.0
        }
        
        emt_areas = ['EMT1', 'EMT2', 'EMT3', 'EMT4']
        expected_focuses = [
            'Visual Emotion Recognition',
            'Situation-to-Expression Connection',
            'Emotion Vocabulary Building',
            'Emotion Label Comprehension'
        ]
        
        for i, area in enumerate(emt_areas):
            data = {**base_data, 'deficient_area': area}
            prompt = InterventionPrompt.get_prompt('gemini', data)
            
            assert area in prompt
            assert expected_focuses[i] in prompt

    def test_get_prompt_invalid_deficient_area(self):
        """Test get_prompt with invalid deficient area."""
        data = {
            'class_id': 'TEST_INVALID',
            'num_students': 25,
            'deficient_area': 'INVALID_EMT',
            'emt1_avg': 70.0,
            'emt2_avg': 70.0,
            'emt3_avg': 70.0,
            'emt4_avg': 70.0
        }
        
        prompt = InterventionPrompt.get_prompt('gemini', data)
        
        # Should contain fallback message
        assert 'No specific strategies available for this area' in prompt

    def test_get_prompt_includes_schema(self):
        """Test get_prompt includes JSON schema."""
        data = {
            'class_id': 'TEST_SCHEMA',
            'num_students': 25,
            'deficient_area': 'EMT1',
            'emt1_avg': 45.0,
            'emt2_avg': 75.0,
            'emt3_avg': 70.0,
            'emt4_avg': 68.0
        }
        
        prompt = InterventionPrompt.get_prompt('gemini', data)
        
        # Should contain schema information
        assert '"type": "object"' in prompt
        assert '"properties"' in prompt
        assert '"analysis"' in prompt
        assert '"strategies"' in prompt

    def test_get_prompt_includes_example(self):
        """Test get_prompt includes example response."""
        data = {
            'class_id': 'TEST_EXAMPLE',
            'num_students': 25,
            'deficient_area': 'EMT1',
            'emt1_avg': 45.0,
            'emt2_avg': 75.0,
            'emt3_avg': 70.0,
            'emt4_avg': 68.0
        }
        
        prompt = InterventionPrompt.get_prompt('gemini', data)
        
        # Should contain example response
        assert '"analysis":' in prompt
        assert '"Emotion Word Wall"' in prompt
        assert '"week1":' in prompt

    def test_get_prompt_safety_guidelines(self):
        """Test get_prompt includes safety guidelines."""
        data = {
            'class_id': 'TEST_SAFETY',
            'num_students': 25,
            'deficient_area': 'EMT1',
            'emt1_avg': 45.0,
            'emt2_avg': 75.0,
            'emt3_avg': 70.0,
            'emt4_avg': 68.0
        }
        
        prompt = InterventionPrompt.get_prompt('gemini', data)
        
        # Should contain safety guidelines
        assert 'SAFETY GUIDELINES - CRITICAL:' in prompt
        assert 'positive, encouraging, and age-appropriate language' in prompt
        assert 'safe and suitable for the classroom' in prompt

    def test_get_prompt_formatting_requirements(self):
        """Test get_prompt includes formatting requirements."""
        data = {
            'class_id': 'TEST_FORMAT',
            'num_students': 25,
            'deficient_area': 'EMT1',
            'emt1_avg': 45.0,
            'emt2_avg': 75.0,
            'emt3_avg': 70.0,
            'emt4_avg': 68.0
        }
        
        prompt = InterventionPrompt.get_prompt('gemini', data)
        
        # Should contain formatting requirements
        assert 'IMPORTANT REQUIREMENTS:' in prompt
        assert 'Return ONLY the JSON object' in prompt
        assert 'valid JSON' in prompt

    def test_base_template_placeholders(self):
        """Test BASE_TEMPLATE contains all required placeholders."""
        template = InterventionPrompt.BASE_TEMPLATE
        
        required_placeholders = [
            '{class_id}',
            '{num_students}',
            '{deficient_area}',
            '{emt1_avg:.2f}',
            '{emt2_avg:.2f}',
            '{emt3_avg:.2f}',
            '{emt4_avg:.2f}',
            '{focused_strategies}',
            '{schema}',
            '{example}'
        ]
        
        for placeholder in required_placeholders:
            assert placeholder in template

    def test_gemini_template_extends_base(self):
        """Test GEMINI_TEMPLATE extends BASE_TEMPLATE."""
        assert InterventionPrompt.BASE_TEMPLATE in InterventionPrompt.GEMINI_TEMPLATE
        assert 'FINAL CHECK:' in InterventionPrompt.GEMINI_TEMPLATE

    def test_openai_template_extends_base(self):
        """Test OPENAI_TEMPLATE extends BASE_TEMPLATE."""
        assert InterventionPrompt.BASE_TEMPLATE in InterventionPrompt.OPENAI_TEMPLATE
        assert 'Format your response as a JSON object' in InterventionPrompt.OPENAI_TEMPLATE 