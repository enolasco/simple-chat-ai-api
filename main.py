from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv
import openai
from openai import AzureOpenAI
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Simple Chat AI API",
    description="An example of an API that uses a Text generation model from Microsoft",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Azure OpenAI client
try:
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo")
    logger.info("Azure OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Azure OpenAI client: {e}")
    client = None

# Pydantic models
class Message(BaseModel):
    role: str = Field(..., description="Role of the message sender (system, user, or assistant)")
    content: str = Field(..., description="Content of the message")

class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="List of messages in the conversation")
    max_tokens: Optional[int] = Field(default=150, description="Maximum number of tokens to generate")
    temperature: Optional[float] = Field(default=0.7, description="Temperature for response generation")

class ChatResponse(BaseModel):
    message: str = Field(..., description="Generated response message")
    usage: Optional[dict] = Field(default=None, description="Token usage information")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status")
    service: str = Field(..., description="Service name")

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Simple Chat AI API",
        "description": "An example of an API that uses a Text generation model from Microsoft",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Azure OpenAI service is not properly configured"
        )
    
    return HealthResponse(
        status="healthy",
        service="Simple Chat AI API with Microsoft Text Generation"
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Generate a chat response using Microsoft's text generation model
    """
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Azure OpenAI service is not available. Please check your configuration."
        )
    
    try:
        # Convert Pydantic messages to OpenAI format
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Make request to Azure OpenAI
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        # Extract the generated message
        generated_message = response.choices[0].message.content
        
        # Prepare usage information
        usage_info = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        } if response.usage else None
        
        logger.info(f"Successfully generated response with {usage_info['total_tokens'] if usage_info else 'unknown'} tokens")
        
        return ChatResponse(
            message=generated_message,
            usage=usage_info
        )
        
    except openai.RateLimitError:
        logger.error("Rate limit exceeded")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    except openai.AuthenticationError:
        logger.error("Authentication failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed. Please check your API key."
        )
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)