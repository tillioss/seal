from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import os
import json
from tenacity import retry, stop_after_attempt, wait_exponential
import google.generativeai as genai
from dotenv import load_dotenv

from app.schemas import InterventionRequest, InterventionPlan
from app.prompts.intervention import InterventionPrompt

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
        self.model = genai.GenerativeModel('gemini-pro')

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_intervention(self, request: InterventionRequest) -> InterventionPlan:
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
        
        # Generate response
        response = self.model.generate_content(prompt)
        
        # Parse response and validate against schema
        try:
            response_json = json.loads(response.text)
            return InterventionPlan(**response_json)
        except Exception as e:
            raise ValueError(f"Failed to parse LLM response as valid InterventionPlan: {str(e)}")

    def health_check(self) -> bool:
        try:
            # Simple test generation
            response = self.model.generate_content("Return the word 'healthy' if you're working.")
            return "healthy" in response.text.lower()
        except Exception:
            return False

class LLMGatewayFactory:
    """Factory for creating LLM gateway instances."""
    
    @staticmethod
    def create(provider: str = "gemini") -> LLMGateway:
        if provider == "gemini":
            return GeminiGateway()
        raise ValueError(f"Unsupported LLM provider: {provider}") 