from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    Represents a message in a chat conversation
    """
    role: str = Field(..., description="The role of the message sender: 'system', 'user', or 'assistant'.")
    content: str = Field(..., description="The content of the message.")


class ChatRequest(BaseModel):
    """
    Request model for chat completions
    """
    messages: List[Message] = Field(..., description="A list of messages comprising the conversation so far.")
    model: str = Field("deepseek-v3", description="ID of the model to use.")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature between 0 and 2.")
    max_tokens: Optional[int] = Field(1024, description="Maximum number of tokens to generate.")
    stream: Optional[bool] = Field(False, description="Whether to stream the response.")


class ChatResponse(BaseModel):
    """
    Response model for chat completions
    """
    id: str = Field(..., description="Unique identifier for the completion.")
    object: str = Field("chat.completion", description="The object type.")
    created: int = Field(..., description="The Unix timestamp (in seconds) of when the completion was created.")
    model: str = Field(..., description="The model used for the completion.")
    choices: List[Dict[str, Any]] = Field(..., description="The generated completions.")
    usage: Dict[str, Any] = Field(..., description="Usage statistics for the completion request.")


class ErrorResponse(BaseModel):
    """
    Error response model
    """
    error: str = Field(..., description="Error message.")
    details: Optional[str] = Field(None, description="Additional error details.")