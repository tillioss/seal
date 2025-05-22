import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pythonjsonlogger import jsonlogger
import logging
import sys

from app.schemas import InterventionRequest, InterventionPlan, HealthResponse
from app.llm.gateway import LLMGatewayFactory

# Configure JSON logging
logger = logging.getLogger()
logHandler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Create FastAPI app
app = FastAPI(
    title="SEAL API",
    description="Social Emotional Adaptive Learning API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM gateway
try:
    llm_gateway = LLMGatewayFactory.create(os.getenv("LLM_PROVIDER", "gemini"))
except Exception as e:
    logger.error(f"Failed to initialize LLM gateway: {str(e)}")
    sys.exit(1)

@app.post("/score", response_model=InterventionPlan)
async def generate_intervention_plan(request: InterventionRequest):
    """Generate an intervention plan based on EMT scores."""
    try:
        logger.info("Generating intervention plan", extra={
            "class_id": request.metadata.class_id,
            "deficient_area": request.metadata.deficient_area
        })
        
        plan = llm_gateway.generate_intervention(request)
        
        logger.info("Successfully generated intervention plan", extra={
            "class_id": request.metadata.class_id,
            "num_strategies": len(plan.strategies)
        })
        
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
    
    if not llm_healthy:
        logger.error("LLM health check failed")
        raise HTTPException(status_code=503, detail="LLM service unavailable")
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        llm_provider=os.getenv("LLM_PROVIDER", "gemini")
    ) 