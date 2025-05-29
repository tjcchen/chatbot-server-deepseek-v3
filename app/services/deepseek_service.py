import httpx
import json
from typing import List, Dict, Any, AsyncGenerator, Optional
from datetime import datetime

from app.core.config import get_settings
from app.models.chat import Message, ChatResponse


class DeepSeekService:
    """Service for interacting with the DeepSeek API"""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.DEEPSEEK_API_KEY
        self.base_url = self.settings.DEEPSEEK_API_BASE_URL
        self.model = self.settings.DEEPSEEK_MODEL
    
    async def chat_completion(
        self, 
        messages: List[Message], 
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stream: bool = False
    ) -> ChatResponse:
        """
        Send a request to the DeepSeek API for chat completion
        
        Args:
            messages: List of messages in the conversation
            model: Model to use (defaults to configured model)
            temperature: Sampling temperature
            max_tokens: Maximum number of tokens to generate
            stream: Whether to stream the response
            
        Returns:
            ChatResponse object with the assistant's response
        """
        if not self.api_key:
            raise ValueError("DeepSeek API key is not configured")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "messages": [msg.dict() for msg in messages],
            "model": model or self.model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            
            if response.status_code != 200:
                error_detail = response.text
                try:
                    error_json = response.json()
                    error_detail = error_json.get("error", {}).get("message", error_detail)
                except:
                    pass
                raise Exception(f"DeepSeek API error: {response.status_code} - {error_detail}")
            
            response_data = response.json()
            
            # Create chat response
            assistant_message = Message(
                role="assistant",
                content=response_data["choices"][0]["message"]["content"]
            )
            
            return ChatResponse(
                message=assistant_message,
                model=response_data.get("model", self.model),
                created_at=datetime.utcnow().isoformat()
            )
    
    async def stream_chat_completion(
        self, 
        messages: List[Message], 
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> AsyncGenerator[str, None]:
        """
        Stream a chat completion response from the DeepSeek API
        
        Args:
            messages: List of messages in the conversation
            model: Model to use (defaults to configured model)
            temperature: Sampling temperature
            max_tokens: Maximum number of tokens to generate
            
        Yields:
            Chunks of the assistant's response as they are generated
        """
        if not self.api_key:
            raise ValueError("DeepSeek API key is not configured")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "messages": [msg.dict() for msg in messages],
            "model": model or self.model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }
        
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            ) as response:
                if response.status_code != 200:
                    error_detail = await response.aread()
                    try:
                        error_json = json.loads(error_detail)
                        error_detail = error_json.get("error", {}).get("message", error_detail)
                    except:
                        pass
                    raise Exception(f"DeepSeek API error: {response.status_code} - {error_detail}")
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        line = line[6:]  # Remove the "data: " prefix
                        
                        if line.strip() == "[DONE]":
                            break
                        
                        try:
                            chunk = json.loads(line)
                            content = chunk["choices"][0]["delta"].get("content", "")
                            if content:
                                yield content
                        except Exception as e:
                            print(f"Error parsing streaming response: {e}")
                            continue
