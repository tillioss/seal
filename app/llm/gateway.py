from abc import ABC, abstractmethod
import os
import json
import logging
import uuid
from typing import Tuple, Dict, Any, AsyncGenerator
from tenacity import retry, stop_after_attempt, wait_exponential, before_log, after_log
import google.generativeai as genai
from dotenv import load_dotenv
import typing_extensions as typing

from app.schemas import InterventionRequest, InterventionPlan
from app.prompts.intervention import InterventionPrompt
from app.safety.guardrails import LLMSafetyValidator
from app.safety.config import DEFAULT_SAFETY_CONFIG

# Import from tilli_prompts for streaming endpoint
try:
    from tilli_prompts.prompts.intervention import InterventionPrompt as TilliInterventionPrompt
    from tilli_prompts.schemas.base import InterventionRequest as TilliInterventionRequest
except ImportError:
    # Fallback to local imports if tilli_prompts not available
    TilliInterventionPrompt = InterventionPrompt
    TilliInterventionRequest = InterventionRequest

logger = logging.getLogger(__name__)

class Strategy(typing.TypedDict):
    title: str
    description: str
    implementationPlan: typing.List[str]
    successMetrics: typing.List[str]

class WeeklyPlan(typing.TypedDict):
    week: int
    focus: str
    activities: typing.List[str]

class InterventionPlanResponse(typing.TypedDict):
    classId: str
    numberOfStudents: int
    deficientArea: str
    strategies: typing.List[Strategy]  # Min 3, Max 5 strategies
    timeline: typing.List[WeeklyPlan]  # 4 weeks
    overallSuccessMetrics: typing.List[str]

class LLMGateway(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate_intervention(self, request: InterventionRequest) -> InterventionPlan:
        """Generate an intervention plan based on the request."""
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check if the LLM service is healthy."""
        pass

class GeminiGateway(LLMGateway):
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.generation_config = {
            "temperature": 0.3,  # Lower temperature for more structured output
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        # Initialize safety validator
        self.safety_validator = LLMSafetyValidator(DEFAULT_SAFETY_CONFIG)

    @retry(
        stop=stop_after_attempt(1),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before=before_log(logger, logging.INFO),
        after=after_log(logger, logging.INFO)
    )
    def generate_intervention(self, request: InterventionRequest) -> InterventionPlan:
        """Generate validated intervention plan with safety checks."""
        try:
            # Generate unique request ID for tracking
            request_id = str(uuid.uuid4())
            
            # Calculate averages
            scores = request.scores
            prompt_data = {
                'class_id': request.metadata.class_id,
                'num_students': request.metadata.num_students,
                'deficient_area': request.metadata.deficient_area,
                'emt1_avg': sum(scores.EMT1) / len(scores.EMT1),
                'emt2_avg': sum(scores.EMT2) / len(scores.EMT2),
                'emt3_avg': sum(scores.EMT3) / len(scores.EMT3),
                'emt4_avg': sum(scores.EMT4) / len(scores.EMT4)
            }
            
            # Get prompt from template
            prompt = InterventionPrompt.get_prompt('gemini', prompt_data)
            
            # Create structured prompt parts
            parts = [
                {"text": "You are an expert Educational Intervention Specialist. Respond ONLY with a valid JSON object."},
                {"text": prompt}
            ]
            
            response = self.model.generate_content(
                parts,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=InterventionPlanResponse,
            ))
            
            if not response.text:
                raise ValueError("Empty response from LLM")
            
            # Debug: Log the raw response
            logger.info(f"Raw LLM response: {response.text[:200]}...")
            
            # Parse the response as JSON
            try:
                response_json = json.loads(response.text)
            except json.JSONDecodeError as e:
                # Try to extract JSON from the response if it's wrapped in other text
                logger.error(f"Initial JSON parse failed: {str(e)}")
                logger.error(f"Raw response: {response.text}")
                
                # Try to find JSON in the response
                start = response.text.find('{')
                end = response.text.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = response.text[start:end]
                    logger.info(f"Extracted JSON: {json_str[:200]}...")
                    response_json = json.loads(json_str)
                else:
                    raise ValueError(f"Could not find valid JSON in response: {response.text}")
            
            # Safety validation
            is_safe, violation = self.safety_validator.validate_content(response_json)
            
            if not is_safe:
                error_msg = violation.message if violation else "Content safety validation failed"
                raise ValueError(f"Safety violation: {error_msg}")
            
            # Convert the response to match InterventionPlan schema
            intervention_plan = {
                "analysis": f"Analysis for class {response_json['classId']} with {response_json['numberOfStudents']} students focusing on {response_json['deficientArea']}.",
                "strategies": [
                    {
                        "activity": strategy.get("title", ""),
                        "implementation": strategy.get("implementationPlan", []),
                        "expected_outcomes": strategy.get("successMetrics", []),
                        "time_allocation": "30 minutes per session",  # Default value
                        "resources": ["Emotion cards", "Activity materials"]  # Default values
                    }
                    for strategy in response_json["strategies"]
                ],
                "timeline": {
                    f"week{week['week']}": week.get("activities", [])
                    for week in response_json["timeline"]
                },
                "success_metrics": {
                    "quantitative": [m for m in response_json["overallSuccessMetrics"] if "%" in m],
                    "qualitative": [m for m in response_json["overallSuccessMetrics"] if "%" not in m],
                    "assessment_methods": ["Weekly assessments", "Observation records", "Student feedback"]
                }
            }

            logger.info("Validated intervention response generated", extra={
                "request_id": request_id,
                "class_id": request.metadata.class_id
            })

            # Validate and return the intervention plan
            return InterventionPlan(**intervention_plan)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            raise ValueError(f"Could not parse JSON from response: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating validated intervention: {str(e)}")
            raise ValueError(f"Failed to generate intervention: {str(e)}")

    def health_check(self) -> bool:
        try:
            response = self.model.generate_content(
                "Return ONLY the word 'healthy' if you're working.",
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema={"type": "string"},
                ))
            
            return "healthy" in response.text.lower()
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False

class StreamingModel:
    """Wrapper for Gemini model that supports streaming."""
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """Initialize streaming model with Gemini."""
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
    
    async def stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream tokens from the model."""
        try:
            # Use Gemini's streaming API
            response = self.model.generate_content(
                prompt,
                stream=True,
                generation_config=genai.GenerationConfig(
                    temperature=0.3,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2048,
                )
            )
            
            # Yield tokens as they arrive
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            logger.error(f"Error during streaming: {str(e)}")
            raise


async def build_prompt_and_model(payload: Dict[str, Any]) -> Tuple[StreamingModel, str]:
    """
    Build prompt and model for streaming endpoint.
    
    Args:
        payload: JSON payload containing InterventionRequest data
        
    Returns:
        Tuple of (model, prompt) where model supports streaming
    """
    # Ensure all required EMT scores are present (fill missing ones with empty lists)
    if "scores" in payload:
        scores = payload["scores"]
        for emt_field in ["EMT1", "EMT2", "EMT3", "EMT4"]:
            if emt_field not in scores:
                scores[emt_field] = []
    
    # Validate / coerce payload to the schema
    req = TilliInterventionRequest(**payload)
    
    # Calculate averages from scores (same as in generate_intervention)
    scores = req.scores
    prompt_data = {
        'class_id': req.metadata.class_id,
        'num_students': req.metadata.num_students,
        'deficient_area': req.metadata.deficient_area,
        'emt1_avg': sum(scores.EMT1) / len(scores.EMT1) if scores.EMT1 else 0.0,
        'emt2_avg': sum(scores.EMT2) / len(scores.EMT2) if scores.EMT2 else 0.0,
        'emt3_avg': sum(scores.EMT3) / len(scores.EMT3) if scores.EMT3 else 0.0,
        'emt4_avg': sum(scores.EMT4) / len(scores.EMT4) if scores.EMT4 else 0.0,
    }
    
    # Build prompt (provider 'gemini' assumed)
    prompt = TilliInterventionPrompt.get_prompt(provider="gemini", data=prompt_data)
    
    # Acquire the model client
    model_name = os.getenv("GENERATOR_MODEL", "gemini-2.5-flash")
    model = StreamingModel(model_name=model_name)
    
    return model, prompt


class LLMGatewayFactory:
    """Factory for creating LLM gateway instances."""
    
    @staticmethod
    def create(provider: str = "gemini") -> LLMGateway:
        if provider == "gemini":
            return GeminiGateway()
        raise ValueError(f"Unsupported LLM provider: {provider}") 