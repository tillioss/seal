from typing import Dict, List, Optional
from pydantic import BaseModel, Field, validator

class EMTScores(BaseModel):
    EMT1: List[float] = Field(..., description="Visual Emotion Matching scores")
    EMT2: List[float] = Field(..., description="Emotion Description scores")
    EMT3: List[float] = Field(..., description="Expression Labeling scores")
    EMT4: List[float] = Field(..., description="Label Matching scores")

    @validator("*")
    def validate_scores(cls, v):
        if not all(0 <= score <= 100 for score in v):
            raise ValueError("All scores must be between 0 and 100")
        return v

class ClassMetadata(BaseModel):
    class_id: str = Field(..., description="Unique identifier for the class")
    deficient_area: str = Field(..., description="Primary area needing intervention")
    num_students: int = Field(..., description="Number of students in the class")

    @validator("deficient_area")
    def validate_deficient_area(cls, v):
        valid_areas = {"EMT1", "EMT2", "EMT3", "EMT4"}
        if v not in valid_areas:
            raise ValueError(f"deficient_area must be one of {valid_areas}")
        return v

class InterventionRequest(BaseModel):
    scores: EMTScores
    metadata: ClassMetadata

class InterventionStrategy(BaseModel):
    activity: str = Field(..., description="Name of the EMT activity")
    implementation: List[str] = Field(..., description="Implementation steps")
    expected_outcomes: List[str] = Field(..., description="Expected outcomes")
    time_allocation: str = Field(..., description="Time required for the activity")
    resources: List[str] = Field(..., description="Required resources")

class SuccessMetrics(BaseModel):
    quantitative: List[str] = Field(..., description="Quantitative targets")
    qualitative: List[str] = Field(..., description="Qualitative indicators")
    assessment_methods: List[str] = Field(..., description="Methods for assessment")

class InterventionPlan(BaseModel):
    analysis: str = Field(..., description="Analysis of performance data")
    strategies: List[InterventionStrategy] = Field(..., min_items=1, max_items=5)
    timeline: Dict[str, List[str]] = Field(..., description="4-week implementation timeline")
    success_metrics: SuccessMetrics

class HealthResponse(BaseModel):
    status: str = Field(..., description="Service health status")
    version: str = Field(..., description="Service version")
    llm_provider: str = Field(..., description="Current LLM provider") 