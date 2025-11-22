from typing import Any
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response, JSONResponse
from chatkit.server import StreamingResult

from .config import get_settings
from .chatkit_server import chatkit_server

app = FastAPI(title="Chat UI Backend")
settings = get_settings()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Chat UI Backend with ChatKit SDK"}


@app.post("/api/chatkit")
async def chatkit_endpoint(request: Request):
    """
    ChatKit endpoint - processes all requests through the ChatKit server.
    """
    try:
        # Read the request body
        body = await request.body()
        
        # Create context (empty dict for now)
        context: dict[str, Any] = {}
        
        # Process the request
        result = await chatkit_server.process(body, context)
        
        # Handle streaming vs non-streaming responses
        if isinstance(result, StreamingResult):
            return StreamingResponse(
                result,
                media_type="text/event-stream",
            )
        else:
            return Response(
                content=result.json,
                media_type="application/json",
            )
    except Exception as e:
        logging.exception("Error processing ChatKit request")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "type": type(e).__name__},
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
