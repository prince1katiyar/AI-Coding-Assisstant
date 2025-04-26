import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize FastAPI app
app = FastAPI()

# Define request model
class CodeRequest(BaseModel):
    language: str
    topic: str
    level: str

def explain_code(language: str, topic: str, level: str) -> str:
    """Explain the given topic in the specified language at the selected level."""
    prompt = f"Explain {topic} in {language} at {level} level."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content  # Extracting response correctly

def debug_code(language: str, topic: str) -> str:
    """Find errors and debug the given code topic in the specified language."""
    prompt = f"Find errors and debug this {language} code related to {topic}."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_code(language: str, topic: str, level: str) -> str:
    """Generate a code snippet based on the given topic, language, and difficulty level."""
    prompt = f"Generate a {level}-level {language} code example on {topic}."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@app.post("/explain")
async def explain(data: CodeRequest):
    return {"response": explain_code(data.language, data.topic, data.level)}

@app.post("/debug")
async def debug(data: CodeRequest):
    try:
        response = debug_code(data.language, data.topic)  # Call debug_code() directly
        if not response:
            return {"response": "⚠️ No debug results found. Please check input."}
        return {"response": response}
    except Exception as e:
        return {"error": f"⚠️ Debugging failed: {str(e)}"}


@app.post("/generate")
async def generate(data: CodeRequest):
    return {"response": generate_code(data.language, data.topic, data.level)}
