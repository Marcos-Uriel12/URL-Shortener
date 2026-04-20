from pydantic import BaseModel, HttpUrl
from datetime import datetime

class UrlCreate(BaseModel):
    original_url: HttpUrl

class UrlResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True