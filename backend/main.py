from fastapi import FastAPI
from pydantic import BaseModel
from ai_engine import explain_code, debug_code, generate_code
import os
from dotenv import load_dotenv
from ai_engine import explain_code, debug_code, generate_code  
load_dotenv()
app = FastAPI()

class CodeRequest(BaseModel):
    language: str
    topic: str
    level: str

@app.post("/explain")
def explain(data: CodeRequest):
    return {"response": explain_code(data.language, data.topic, data.level)}

@app.post("/debug")
async def debug(data: CodeRequest):  # ✅ Use `data` instead of `request`
    try:
        response = debug_code(data.language, data.topic)  # ✅ Direct function call
        if not response:
            return {"response": "⚠️ No debug results found. Please check input."}
        return {"response": response}
    except Exception as e:
        return {"error": f"⚠️ Debugging failed: {str(e)}"}





@app.post("/generate")
def generate(data: CodeRequest):
    return {"response": generate_code(data.language, data.topic, data.level)}
