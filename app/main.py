"""Main FastAPI application for SEAL API."""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.schemas import InterventionRequest, InterventionPlan, HealthResponse
from app.schemas.curriculum import CurriculumRequest, CurriculumResponse
from app.llm.gateway import LLMGatewayFactory
from app.llm.curriculum_gateway import GeminiCurriculumGateway

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize LLM gateways
llm_gateway = LLMGatewayFactory.create("gemini")
curriculum_gateway = GeminiCurriculumGateway()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting SEAL API", extra={
        "environment": os.getenv('ENVIRONMENT', 'production'),
        "llm_provider": os.getenv("LLM_PROVIDER", "gemini")
    })
    yield
    logger.info("Shutting down SEAL API")

# Create FastAPI app
app = FastAPI(
    title="SEAL API",
    description="Social Emotional Adaptive Learning API for generating intervention plans",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/score", response_model=InterventionPlan)
async def generate_intervention_plan(request: InterventionRequest):
    """Generate an intervention plan based on student scores."""
    try:
        logger.info("Generating intervention plan", extra={
            "class_id": request.metadata.class_id,
            "deficient_area": request.metadata.deficient_area
        })
        
        # Generate validated intervention plan directly
        plan = llm_gateway.generate_intervention(request)
        
        logger.info("Successfully generated intervention plan")
        
        return plan
    
    except ValueError as e:
        logger.error("Validation error", extra={"error": str(e)})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/curriculum", response_model=CurriculumResponse)
async def generate_curriculum_plan(request: CurriculumRequest):
    """Generate a curriculum-based intervention plan."""
    try:
        logger.info("Generating curriculum plan", extra={
            "grade_level": request.grade_level,
            "skill_areas": [area.value for area in request.skill_areas],
            "score": request.score
        })
        
        # Generate validated curriculum plan directly
        plan_data = curriculum_gateway.generate_curriculum_plan(request)
        plan = CurriculumResponse(**plan_data)
        
        logger.info("Successfully generated curriculum plan")
        
        return plan
    
    except ValueError as e:
        logger.error("Validation error", extra={"error": str(e)})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check service health."""
    llm_healthy = llm_gateway.health_check()
    curriculum_healthy = curriculum_gateway.health_check()
    
    if not (llm_healthy and curriculum_healthy):
        logger.error("Health check failed", extra={
            "llm_healthy": llm_healthy,
            "curriculum_healthy": curriculum_healthy
        })
        raise HTTPException(status_code=503, detail="Service unhealthy")
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        llm_provider=os.getenv("LLM_PROVIDER", "gemini")
    ) 