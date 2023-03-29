from pydantic import BaseModel

class HelloModel(BaseModel):
    title: str
    content: str