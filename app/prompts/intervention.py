"""Prompt templates for intervention generation."""

from typing import Dict, Any
import json
from app.schemas import InterventionPlan

class InterventionPrompt:
    """Manages prompt templates for intervention generation."""
    
    EXAMPLE_RESPONSE = {
        "analysis": "The class shows significant deficiency in EMT3 (Expression Labeling) with an average score of 65%, indicating difficulties in labeling emotional expressions accurately.",
        "strategies": [
            {
                "activity": "Emotion Expression Match",
                "implementation": [
                    "Display emotion cards with facial expressions",
                    "Students take turns matching expressions to emotion labels",
                    "Practice expressing emotions in pairs"
                ],
                "expected_outcomes": [
                    "Improved accuracy in labeling expressions",
                    "Enhanced emotional vocabulary",
                    "Better recognition of subtle expressions"
                ],
                "time_allocation": "30 minutes per session, 3 times per week",
                "resources": [
                    "Emotion expression cards",
                    "Emotion label cards",
                    "Mirror for practice"
                ]
            }
        ],
        "timeline": {
            "week1": ["Introduction to basic emotions", "Practice with clear expressions"],
            "week2": ["Work on subtle expressions", "Peer practice sessions"],
            "week3": ["Group activities", "Real-world application"],
            "week4": ["Assessment", "Reinforcement activities"]
        },
        "success_metrics": {
            "quantitative": ["10% improvement in EMT3 scores", "80% participation rate"],
            "qualitative": ["Increased confidence in expression labeling", "Better peer interactions"],
            "assessment_methods": ["Weekly mini-assessments", "Observation records", "Student feedback"]
        }
    }
    
    BASE_TEMPLATE = """You are an expert Educational Intervention Specialist focusing on emotional intelligence development in children.

TASK: Create a detailed intervention plan for a class showing difficulties in emotional recognition and expression.

SAFETY GUIDELINES - CRITICAL:
- Use ONLY positive, encouraging, and age-appropriate language
- Focus on growth, learning, and development opportunities
- Avoid any negative, harmful, or inappropriate content
- Use simple language that children can understand
- Ensure all activities are safe and suitable for the classroom
- Promote inclusivity and respect for all students

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

Your response MUST be a valid JSON object matching this schema EXACTLY:
{schema}

Here's an example of a valid response structure (adapt content to the current situation):
{example}

IMPORTANT INSTRUCTIONS:
1. Return ONLY the JSON object, no other text
2. Ensure the JSON structure matches the schema exactly
3. Include at least 3 strategies (maximum 5)
4. Make all strategies specific to the deficient area ({deficient_area})
5. Include a 4-week timeline
6. Provide measurable success metrics
7. Double-check that your response is valid JSON
8. ENSURE ALL CONTENT IS POSITIVE, SAFE, AND AGE-APPROPRIATE

Focus on creating specific, actionable strategies that address the deficient area while maintaining development in other areas. All content must be suitable for teachers to use with children in educational settings."""

    GEMINI_TEMPLATE = BASE_TEMPLATE + """
FINAL CHECK:
1. Your response must start with '{'
2. Your response must end with '}'
3. Use double quotes for all strings
4. No trailing commas
5. No comments or additional text"""

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
        # Add schema and example to data
        data['schema'] = json.dumps(InterventionPlan.model_json_schema(), indent=2)
        data['example'] = json.dumps(cls.EXAMPLE_RESPONSE, indent=2)
        
        # Select template based on provider
        template = {
            'gemini': cls.GEMINI_TEMPLATE,
            'openai': cls.OPENAI_TEMPLATE
        }.get(provider, cls.BASE_TEMPLATE)

        return template