from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class Contact(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    company: Optional[str] = None
    message: str = Field(..., min_length=5, max_length=2000)
    budget: Optional[str] = None


class CaseStudy(BaseModel):
    title: str
    client: str
    summary: str
    impact: List[str] = []
    image: Optional[str] = None
    url: Optional[str] = None


class Service(BaseModel):
    name: str
    description: str
    highlights: List[str] = []
    icon: Optional[str] = None
