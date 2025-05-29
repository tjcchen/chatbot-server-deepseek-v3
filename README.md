# Chatbot Server DeepSeek V3

A FastAPI backend for a chatbot application that integrates with the DeepSeek V3 API service.

## Features

- RESTful API built with FastAPI
- Integration with DeepSeek V3 API
- Support for both streaming and non-streaming chat completions
- Environment-based configuration
- CORS support for frontend integration

## Project Structure

```
/app
  /api
    /endpoints
      chat.py         # Chat API endpoints
    api.py            # API router
  /core
    config.py         # Application configuration
  /models
    chat.py           # Pydantic models
  /services
    deepseek_service.py # DeepSeek API integration
  main.py             # FastAPI application
main.py               # Entry point
requirements.txt      # Project dependencies
.env.example          # Example environment variables
```

## Getting Started

### Prerequisites

- Python 3.8+
- DeepSeek API key

### Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/chatbot-server-deepseek-v3.git
cd chatbot-server-deepseek-v3
```

2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip3 install -r requirements.txt
```

4. Set up environment variables

```bash
cp .env.example .env
```

Edit the `.env` file with your DeepSeek API key and other settings.

### Running the Application

```bash
python3 main.py
```

The API will be available at http://localhost:8000

- API Documentation: http://localhost:8000/docs
- OpenAPI Specification: http://localhost:8000/api/v1/openapi.json

## API Usage

### Chat Completion

```http
POST /api/v1/chat/
```

Request body:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Hello, how are you?"
    }
  ],
  "model": "deepseek-chat",
  "temperature": 0.7,
  "max_tokens": 1024,
  "stream": false
}
```

**Example curl command:**

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/chat/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  "model": "deepseek-chat",
  "temperature": 0.7,
  "max_tokens": 1024,
  "stream": false
}'
```

Example response:

```json
{
  "id": "a7134b3b-ca12-46c1-9505-3a9f957980a3",
  "object": "chat.completion",
  "created": 1748503357,
  "model": "deepseek-chat",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! 😊 How can I assist you today?"
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 11,
    "completion_tokens": 11,
    "total_tokens": 22,
    "prompt_tokens_details": {"cached_tokens": 0},
    "prompt_cache_hit_tokens": 0,
    "prompt_cache_miss_tokens": 11
  }
}
```

### Streaming Chat Completion

```http
POST /api/v1/chat/stream
```

Request body is the same as for the regular chat endpoint. The response will be a server-sent events stream.

**Example curl command:**

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/chat/stream' \
  -H 'accept: text/event-stream' \
  -H 'Content-Type: application/json' \
  --no-buffer \
  -d '{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Write a short poem about AI"}
  ],
  "model": "deepseek-chat",
  "temperature": 0.7,
  "max_tokens": 1024
}'
```

## License

This project is licensed under the MIT License.
