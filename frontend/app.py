from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import os
from datetime import datetime

app = FastAPI()

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat(message: ChatMessage):
    # Split the message into words and add 'boogie' after each word
    words = message.message.split()
    boogie_message = ' '.join(f"{word} boogie" for word in words)
    return {"response": boogie_message}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Create a unique filename using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join("../images", filename)
        
        # Save the file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return JSONResponse(
            content={"message": "File uploaded successfully", "filename": filename},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"message": f"Error uploading file: {str(e)}"},
            status_code=500
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 