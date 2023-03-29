from pydantic import BaseModel


# Path: web\response.py
# Response model 만들기
class ResponseModel(BaseModel):
    code: int
    message: str
    data: list[dict] = []