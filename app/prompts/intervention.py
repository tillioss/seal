"""Prompt templates for intervention generation."""

from typing import Dict, Any
import json
from app.schemas import InterventionPlan

class InterventionPrompt:
    """Manages prompt templates for intervention generation."""
    
    BASE_TEMPLATE = """You are an expert Educational Intervention Specialist focusing on emotional intelligence development in children.

TASK: Create a detailed intervention plan for a class showing difficulties in emotional recognition and expression.

CLASS INFORMATION:
- Class ID: {class_id}
- Number of Students: {num_students}
- Primary Area Needing Intervention: {deficient_area}

CURRENT PERFORMANCE:
EMT Score Averages:
- EMT1 (Visual Matching): {emt1_avg:.2f}%
- EMT2 (Emotion Description): {emt2_avg:.2f}%
- EMT3 (Expression Labeling): {emt3_avg:.2f}%
- EMT4 (Label Matching): {emt4_avg:.2f}%

Your response MUST be in valid JSON format matching this schema:
{schema}

Focus on creating specific, actionable strategies that address the deficient area while maintaining development in other areas.
Ensure all response fields are properly filled and match the schema exactly."""

    GEMINI_TEMPLATE = BASE_TEMPLATE + """
Note: Ensure your response is a single, valid JSON object."""

    OPENAI_TEMPLATE = BASE_TEMPLATE + """
Note: Format your response as a JSON object without any additional text or explanation."""

    @classmethod
    def get_prompt(cls, provider: str, data: Dict[str, Any]) -> str:
        """Get formatted prompt for specified provider.
        
        Args:
            provider: LLM provider name ('gemini', 'openai', etc.)
            data: Dictionary containing template variables
            
        Returns:
            Formatted prompt string
        """
        # Add schema to data
        data['schema'] = json.dumps(InterventionPlan.model_json_schema(), indent=2)
        
        # Select template based on provider
        template = {
            'gemini': cls.GEMINI_TEMPLATE,
            'openai': cls.OPENAI_TEMPLATE
        }.get(provider, cls.BASE_TEMPLATE)
        
        return template.format(**data) 