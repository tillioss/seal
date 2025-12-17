"""Basic LLM safety validation for educational content."""

import json
import logging
import os
from typing import Dict, Any, Tuple
from dataclasses import dataclass

import google.generativeai as genai
from dotenv import load_dotenv

from .config import SafetyConfig, DEFAULT_SAFETY_CONFIG, DEV_SAFETY_CONFIG

logger = logging.getLogger(__name__)

@dataclass
class SafetyViolation:
    """Represents a safety violation found in content."""
    message: str
    suggestion: str = ""

class LLMSafetyValidator:
    """Basic LLM safety validator for educational content."""
    
    SAFETY_PROMPT = """You are a content safety validator for educational materials designed for children.

Evaluate if this content is appropriate for teachers to use with children in educational settings.

CONTENT:
{content}

Respond with ONLY a JSON object:
{{
  "is_safe": true
}}

OR if unsafe:
{{
  "is_safe": false,
  "reason": "brief explanation of why it's unsafe",
  "suggestion": "how to make it appropriate"
}}"""

    def __init__(self, config: SafetyConfig = None):
        self.config = config or self._get_config_from_env()
        
        # Initialize Gemini model
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-pro')
    
    def _get_config_from_env(self) -> SafetyConfig:
        """Get safety configuration based on environment."""
        env = os.getenv('ENVIRONMENT', 'production').lower()
        return DEV_SAFETY_CONFIG if env == 'development' else DEFAULT_SAFETY_CONFIG
    
    def validate_content(self, content: Dict[str, Any]) -> Tuple[bool, SafetyViolation]:
        """Validate content for safety using LLM."""
        if not self.config.enabled:
            return True, None
        
        try:
            # Convert content to string
            content_str = json.dumps(content, indent=2)
            
            # Get LLM safety assessment
            prompt = self.SAFETY_PROMPT.format(content=content_str)
            response = self.model.generate_content(prompt)
            
            if not response.text:
                return False, SafetyViolation("Safety validation failed", "Retry the request")
            
            # Parse response
            result = json.loads(self._clean_json(response.text))
            is_safe = result.get("is_safe", False)
            
            if is_safe:
                return True, None
            else:
                violation = SafetyViolation(
                    message=result.get("reason", "Content not appropriate for children"),
                    suggestion=result.get("suggestion", "Review and revise content")
                )
                return False, violation
                
        except Exception as e:
            logger.error(f"Safety validation error: {str(e)}")
            return False, SafetyViolation("Safety validation failed", "Contact administrator")
    
    def _clean_json(self, text: str) -> str:
        """Extract JSON from response."""
        text = text.strip()
        if text.startswith('```'):
            text = text[3:]
        if text.startswith('json'):
            text = text[4:]
        if text.endswith('```'):
            text = text[:-3]
        
        start = text.find('{')
        end = text.rfind('}')
        if start >= 0 and end > start:
            return text[start:end + 1]
        return text.strip() 