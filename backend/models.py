from pydantic import BaseModel

class CodeRequest(BaseModel):
    language: str
    topic: str
    level: str
