from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
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
chat_pipeline = None

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    response: str
    model_info: str

class ModelConfig(BaseModel):
    model_name: str

# Initialize model on startup
@app.on_event("startup")
async def startup_event():
    global model, tokenizer, chat_pipeline
    try:
        logger.info("Loading Hugging Face model...")
        model_name = "microsoft/DialoGPT-medium"
        
        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Create text generation pipeline
        chat_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )
        
        logger.info(f"Model {model_name} loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        model = None
        tokenizer = None
        chat_pipeline = None

@app.get("/")
async def root():
    return {
        "message": "Hugging Face Chat API",
        "version": "1.0.0",
        "status": "running" if model else "model not loaded"
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
        
        # Encode the input message
        input_ids = tokenizer.encode(request.message + tokenizer.eos_token, return_tensors='pt')
        
        # Generate response
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_length=input_ids.shape[1] + request.max_tokens,
                temperature=request.temperature,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode the response
        response = tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        return ChatResponse(
            response=response.strip(),
            model_info="microsoft/DialoGPT-medium"
        )
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@app.post("/load-model")
async def load_model(config: ModelConfig):
    global model, tokenizer, chat_pipeline
    try:
        logger.info(f"Loading new model: {config.model_name}")
        
        # Load new tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        model = AutoModelForCausalLM.from_pretrained(config.model_name)
        
        # Create new pipeline
        chat_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )
        
        return {"message": f"Model {config.model_name} loaded successfully"}
    except Exception as e:
        logger.error(f"Failed to load model {config.model_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")
