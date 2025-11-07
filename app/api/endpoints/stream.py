from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator, Dict, Any
import json

from app.llm.gateway import build_prompt_and_model

router = APIRouter()

@router.post("/stream")
async def stream_intervention(request: Request) -> StreamingResponse:
    try:
        payload: Dict[str, Any] = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    async def event_stream() -> AsyncGenerator[str, None]:
        # get model + prompt
        model, prompt = await build_prompt_and_model(payload)

        # start model streaming (pseudo API; adapt to your model client)
        async for token in model.stream(prompt):
            # Each SSE event must end with double newline
            yield f"data: {json.dumps({'token': token})}\n\n"

        yield f"data: {json.dumps({'status': 'complete'})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

