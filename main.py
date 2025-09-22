from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Hugging Face Chat API",
    description="A text generation chat API using Hugging Face Transformers",
    version="1.0.0"
)

# Global variables to store the model and tokenizer
model = None
tokenizer = None

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    max_tokens: Optional[int] = 50
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    response: str
    model_info: str

# Initialize model on startup
@app.on_event("startup")
async def startup_event():
    global model, tokenizer
    try:
        logger.info("Loading Hugging Face model...")
        model_name = "microsoft/DialoGPT-small"  # Using small model for faster loading
        
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Add pad token if it doesn't exist
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        logger.info(f"Model {model_name} loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        model = None
        tokenizer = None

@app.get("/")
async def root():
    return {
        "message": "Hugging Face Chat API",
        "version": "1.0.0",
        "status": "running" if model else "model not loaded",
        "endpoints": ["/chat", "/health", "/docs"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if model else "unhealthy",
        "model_loaded": model is not None,
        "cuda_available": torch.cuda.is_available()
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        logger.info(f"Processing chat request: {request.message[:50]}...")
        
        # Encode the input message with proper formatting
        input_text = request.message + tokenizer.eos_token
        input_ids = tokenizer.encode(input_text, return_tensors='pt')
        
        # Generate response
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_length=input_ids.shape[1] + request.max_tokens,
                temperature=request.temperature,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                no_repeat_ngram_size=2
            )
        
        # Decode the response (only the new tokens)
        response = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        # Clean up the response
        response = response.strip()
        if not response:
            response = "I understand. How can I help you further?"
        
        return ChatResponse(
            response=response,
            model_info="microsoft/DialoGPT-small"
        )
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)