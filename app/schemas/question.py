from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class QuestionCreate(BaseModel):
    question: str = Field(min_length=1)


class QuestionOut(BaseModel):
    id: int
    document_id: int
    question: str
    answer: Optional[str] = None
    status: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class QuestionResponse(BaseModel):
    question_id: int
    status: str
