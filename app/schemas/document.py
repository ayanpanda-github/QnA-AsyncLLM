from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class DocumentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=1)


class DocumentOut(DocumentCreate):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
