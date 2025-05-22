"""Curriculum intervention gateway implementation."""

import json
from tenacity import retry, stop_after_attempt, wait_exponential

from app.llm.gateway import LLMGateway
from app.schemas.curriculum import CurriculumRequest, CurriculumResponse
from app.prompts.curriculum import CurriculumPrompt

class CurriculumGateway(LLMGateway):
    """Gateway for curriculum-based intervention generation."""

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_curriculum_plan(self, request: CurriculumRequest) -> CurriculumResponse:
        """Generate a curriculum-based intervention plan.
        
        Args:
            request: The curriculum request containing grade level and score
            
        Returns:
            A curriculum response with recommended interventions
            
        Raises:
            ValueError: If the LLM response cannot be parsed
        """
        # Prepare data for prompt
        prompt_data = {
            'grade_level': request.grade_level,
            'skill_areas': [area.value for area in request.skill_areas],
            'score': request.score
        }
        
        # Get prompt from template
        prompt = CurriculumPrompt.get_prompt(self._get_provider_name(), prompt_data)
        
        # Generate response
        response = self._generate_content(prompt)
        
        # Parse and validate response
        try:
            response_json = json.loads(response)
            return CurriculumResponse(**response_json)
        except Exception as e:
            raise ValueError(f"Failed to parse LLM response as valid CurriculumResponse: {str(e)}")

    def _get_provider_name(self) -> str:
        """Get the name of the LLM provider."""
        return "gemini"  # Override in specific implementations 