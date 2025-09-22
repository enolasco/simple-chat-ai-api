# Simple Chat AI API

An example of an API that uses a Text generation model from Microsoft (Azure OpenAI Service).

This project demonstrates how to build a simple chat API using FastAPI and Microsoft's Azure OpenAI Service for text generation capabilities.

## Features

- RESTful API built with FastAPI
- Integration with Microsoft Azure OpenAI Service
- Chat completion endpoint with conversation history
- Configurable parameters (temperature, max tokens)
- Health check endpoint
- Comprehensive error handling
- CORS support for web applications
- Automatic API documentation

## Setup

### Prerequisites

- Python 3.8 or higher
- Azure OpenAI Service account with deployed model
- API key and endpoint from Azure OpenAI

### Installation

1. Clone the repository:
```bash
git clone https://github.com/enolasco/simple-chat-ai-api.git
cd simple-chat-ai-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env file with your Azure OpenAI credentials
```

4. Update the `.env` file with your Azure OpenAI configuration:
```env
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2023-12-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
```

### Running the API

Start the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- **GET** `/health` - Check if the service is running and properly configured

### Chat Completion
- **POST** `/chat` - Generate chat responses using Microsoft's text generation model

### Documentation
- **GET** `/docs` - Interactive API documentation (Swagger UI)
- **GET** `/redoc` - Alternative API documentation

## Usage Examples

### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

Response:
```json
{
  "status": "healthy",
  "service": "Simple Chat AI API with Microsoft Text Generation"
}
```

### Chat Completion
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is the capital of France?"}
    ],
    "max_tokens": 150,
    "temperature": 0.7
  }'
```

Response:
```json
{
  "message": "The capital of France is Paris. It is located in the north-central part of the country and is known for its iconic landmarks such as the Eiffel Tower, Louvre Museum, and Notre-Dame Cathedral.",
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 35,
    "total_tokens": 60
  }
}
```

### Conversation Example
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful assistant that explains things simply."},
      {"role": "user", "content": "Explain machine learning in simple terms."},
      {"role": "assistant", "content": "Machine learning is like teaching a computer to recognize patterns and make predictions by showing it lots of examples, similar to how you might learn to recognize different dog breeds by looking at many pictures of dogs."},
      {"role": "user", "content": "Can you give me a practical example?"}
    ],
    "max_tokens": 200,
    "temperature": 0.8
  }'
```

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| messages | Array | Yes | List of messages in the conversation |
| max_tokens | Integer | No | Maximum tokens to generate (default: 150) |
| temperature | Float | No | Response randomness 0.0-1.0 (default: 0.7) |

## Message Format

Each message in the `messages` array should have:
- `role`: "system", "user", or "assistant"
- `content`: The message content

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- `400` - Bad Request (invalid input)
- `401` - Unauthorized (invalid API key)
- `429` - Too Many Requests (rate limit exceeded)
- `503` - Service Unavailable (Azure OpenAI not configured)
- `500` - Internal Server Error

## Development

### Project Structure
```
simple-chat-ai-api/
├── main.py              # Main API application
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore file
└── README.md           # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes
5. Submit a pull request

## License

This project is provided as an example implementation. Please ensure compliance with Microsoft Azure OpenAI Service terms of use.

## Support

For issues related to:
- Azure OpenAI Service: Check [Azure OpenAI documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/openai/)
- This implementation: Open an issue in this repository