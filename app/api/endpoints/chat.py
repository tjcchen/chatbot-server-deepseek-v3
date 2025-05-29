from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import List, Optional

from app.models.chat import ChatRequest, ChatResponse, Message, ErrorResponse
from app.services.deepseek_service import DeepSeekService

router = APIRouter()


@router.post(
    "/chat", 
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def create_chat_completion(
    chat_request: ChatRequest,
    deepseek_service: DeepSeekService = Depends(lambda: DeepSeekService())
):
    """
    Create a chat completion with the DeepSeek API
    """
    try:
        if not chat_request.messages:
            raise HTTPException(
                status_code=400,
                detail={"error": "No messages provided", "details": "At least one message is required"}
            )
        
        return await deepseek_service.chat_completion(
            messages=chat_request.messages,
            model=chat_request.model,
            temperature=chat_request.temperature,
            max_tokens=chat_request.max_tokens,
            stream=chat_request.stream
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"error": "Invalid request", "details": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Server error", "details": str(e)}
        )


@router.post("/chat/stream")
async def create_streaming_chat_completion(
    chat_request: ChatRequest,
    deepseek_service: DeepSeekService = Depends(lambda: DeepSeekService())
):
    """
    Create a streaming chat completion with the DeepSeek API
    """
    try:
        if not chat_request.messages:
            raise HTTPException(
                status_code=400,
                detail={"error": "No messages provided", "details": "At least one message is required"}
            )
        
        # Force stream to be True for this endpoint
        chat_request.stream = True
        
        async def generate():
            async for chunk in deepseek_service.stream_chat_completion(
                messages=chat_request.messages,
                model=chat_request.model,
                temperature=chat_request.temperature,
                max_tokens=chat_request.max_tokens
            ):
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"error": "Invalid request", "details": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Server error", "details": str(e)}
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok"}
