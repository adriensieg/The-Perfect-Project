from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import logging
from database import FirestoreDB

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Advanced Text Transformer API",
    description="A state-of-the-art text transformation service",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    Add security-related HTTP headers
    """
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# HTTP Bearer Token Authentication
security = HTTPBearer()

# Firestore Database instance
db = FirestoreDB()

# Request Models
class TextInput(BaseModel):
    text: str

# Routes
@app.post("/api/submit", status_code=status.HTTP_201_CREATED)
async def submit_text(input_data: TextInput, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Accept text input, convert to uppercase, save to Firestore, and return the result.
    """
    try:
        token = credentials.credentials  # Token can be validated if needed
        original_text = input_data.text
        if not original_text:
            raise HTTPException(status_code=400, detail="Text is required")

        processed_text = original_text.upper()
        logger.info(f"Processed text: {processed_text}")

        # Save to Firestore
        entry = db.create_entry(original_text, processed_text)
        return {"id": entry["id"], "original": original_text, "processed": processed_text}

    except Exception as e:
        logger.error(f"Error in /api/submit: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/history", status_code=status.HTTP_200_OK)
async def get_history(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Retrieve all history entries.
    """
    try:
        token = credentials.credentials
        history = db.read_all_entries()
        return history
    except Exception as e:
        logger.error(f"Error in /api/history: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/api/history/{entry_id}", status_code=status.HTTP_200_OK)
async def update_entry(entry_id: str, input_data: TextInput, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Update an existing entry with new text.
    """
    try:
        token = credentials.credentials
        new_text = input_data.text
        if not new_text:
            raise HTTPException(status_code=400, detail="Text is required")

        processed_text = new_text.upper()
        updated_entry = db.update_entry(entry_id, new_text, processed_text)
        return updated_entry

    except Exception as e:
        logger.error(f"Error in /api/history/{entry_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/api/history/{entry_id}", status_code=status.HTTP_200_OK)
async def delete_entry(entry_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Delete an entry from the history.
    """
    try:
        token = credentials.credentials
        db.delete_entry(entry_id)
        return {"message": "Entry deleted"}
    except Exception as e:
        logger.error(f"Error in /api/history/{entry_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
