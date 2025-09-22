# FastAPI Hugging Face Chat API

A robust text generation chat API built with FastAPI and Hugging Face Transformers. This API provides conversational AI capabilities using pre-trained language models from Hugging Face.

## Features

- 🤖 **Chat Endpoint**: Generate conversational responses using Hugging Face models
- 🔧 **Model Configuration**: Dynamic model loading and switching
- 📊 **Health Monitoring**: Built-in health checks and status endpoints
- 🛡️ **Error Handling**: Comprehensive error handling and logging
- 📝 **API Documentation**: Auto-generated OpenAPI/Swagger docs
- 🚀 **GPU Support**: Automatic GPU detection and usage when available

## Quick Start

### 1. Install Python
Make sure Python 3.8+ is installed on your system:
```bash
python --version
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the API Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the provided scripts:
- Windows: `start.bat`
- Linux/Mac: `./start.sh`

### 4. Access the API
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## API Endpoints

### POST /chat
Generate a conversational response.

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "max_tokens": 100,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "response": "Hello! I'm doing well, thank you for asking. How can I help you today?",
  "model_info": "microsoft/DialoGPT-medium"
}
```

### GET /health
Check API and model status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### POST /load-model
Dynamically load a different model.

**Request Body:**
```json
{
  "model_name": "microsoft/DialoGPT-large"
}
```

## Testing

Run the test client to verify the API:
```bash
python test_client.py
```

## Configuration

### Model Selection
You can change the default model in `app/main.py` or use the `/load-model` endpoint:

```python
# Popular Hugging Face models for chat:
- microsoft/DialoGPT-medium
- microsoft/DialoGPT-large
- microsoft/DialoGPT-small
- facebook/blenderbot-400M-distill
- google/flan-t5-base
- EleutherAI/gpt-neo-1.3B
```

### Parameters
- `max_tokens`: Maximum response length (default: 100)
- `temperature`: Response creativity 0.0-2.0 (default: 0.7)

## Dependencies

- **FastAPI**: Modern web framework for APIs
- **Transformers**: Hugging Face transformers library for NLP models
- **PyTorch**: Deep learning framework
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for FastAPI

## Production Deployment

For production use:

1. **Use a production ASGI server:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

2. **Set environment variables:**
```bash
export MODEL_NAME="microsoft/DialoGPT-medium"
export MAX_TOKENS=150
export TEMPERATURE=0.7
```

3. **Use Docker:**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Python Not Found
If you get "python: command not found":
1. Install Python from https://python.org
2. Make sure "Add Python to PATH" is checked during installation
3. Restart your terminal

### Model Loading Issues
- Ensure you have sufficient RAM (4GB+ recommended)
- Check internet connection for model downloads
- Try smaller models like `microsoft/DialoGPT-small`

### Port Already in Use
Change the port in the uvicorn command:
```bash
uvicorn app.main:app --reload --port 8001
```

## License

MIT License - Feel free to use and modify!

---

Built with ❤️ using FastAPI and Hugging Face Transformers
