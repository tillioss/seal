"""Curriculum intervention gateway implementation."""

import json
import os
import uuid
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
import google.generativeai as genai
from dotenv import load_dotenv

from app.llm.gateway import LLMGateway
from app.schemas.curriculum import CurriculumRequest, CurriculumResponse
from app.schemas import InterventionRequest, InterventionPlan
from app.prompts.curriculum import CurriculumPrompt
from app.safety.guardrails import LLMSafetyValidator
from app.safety.config import DEFAULT_SAFETY_CONFIG
import typing_extensions as typing

logger = logging.getLogger(__name__)

class Implementation(typing.TypedDict):
    steps: typing.List[str]
    materials: typing.Optional[typing.List[str]]
    time_allocation: typing.Optional[str]

class CurriculumIntervention(typing.TypedDict):
    name: str
    grade_levels: typing.List[typing.Literal["1", "2", "5"]]
    skill_area: typing.Literal["emotional_awareness", "emotional_regulation", "anger_management"]
    summary: str
    implementation: Implementation
    intended_purpose: str

class CurriculumResponseSchema(typing.TypedDict):
    recommended_interventions: typing.List[CurriculumIntervention]
    skill_focus: typing.List[str]
    implementation_order: typing.List[str]

class CurriculumGateway(LLMGateway):
    """Gateway for curriculum-based intervention generation."""

    @retry(stop=stop_after_attempt(1), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_curriculum_plan(self, request: CurriculumRequest):
        """Generate validated curriculum plan with safety checks."""
        # Generate unique request ID for tracking
        request_id = str(uuid.uuid4())
        
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
            # First try direct JSON parsing
            response_json = json.loads(response)
        except json.JSONDecodeError:
            # If that fails, try to find JSON in the text
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                response_json = json.loads(json_str)
            else:
                raise ValueError("Could not find valid JSON in response")

        # Safety validation
        is_safe, violation = self.safety_validator.validate_content(response_json)
        
        if not is_safe:
            error_msg = violation.message if violation else "Content safety validation failed"
            raise ValueError(f"Safety violation: {error_msg}")

        logger.info("Validated curriculum response generated", extra={
            "request_id": request_id,
            "grade_level": request.grade_level,
            "skill_areas": [area.value for area in request.skill_areas]
        })

        return response_json

    def generate_intervention(self, request: InterventionRequest) -> InterventionPlan:
        """Implement the abstract method from LLMGateway."""
        raise NotImplementedError("This gateway does not support intervention generation")

    def health_check(self) -> bool:
        """Implement the abstract method from LLMGateway."""
        try:
            # Simple test generation
            response = self._generate_content("Return the word 'healthy' if you're working.")
            return "healthy" in response.lower()
        except Exception:
            return False

    def _get_provider_name(self) -> str:
        """Get the name of the LLM provider."""
        return "gemini"  # Override in specific implementations

    def _generate_content(self, prompt: str) -> str:
        """Generate content using the LLM."""
        raise NotImplementedError("_generate_content must be implemented by concrete classes")

class GeminiCurriculumGateway(CurriculumGateway):
    """Gemini-specific implementation of the curriculum gateway."""
    
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-pro')
        
        # Initialize safety validator
        self.safety_validator = LLMSafetyValidator(DEFAULT_SAFETY_CONFIG)

    def _generate_content(self, prompt: str) -> str:
        """Generate content using the Gemini model."""
        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=CurriculumResponseSchema,
        ))
        
        if not response.text:
            raise ValueError("Empty response from LLM")
        
        return response.candidates[0].content.parts[0].text