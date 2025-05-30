"""Basic safety configuration for LLM validation."""

from dataclasses import dataclass

@dataclass
class SafetyConfig:
    """Basic configuration for LLM safety validation."""
    
    # Whether to enable safety validation
    enabled: bool = True
    
    # Whether to include violation details in error messages
    include_violation_details: bool = False

# Default safety configuration
DEFAULT_SAFETY_CONFIG = SafetyConfig()

# Development configuration (shows violation details)
DEV_SAFETY_CONFIG = SafetyConfig(
    enabled=True,
    include_violation_details=True
) 