import json
from pydantic import BaseModel
from typing import List, Optional

class BoundingBox(BaseModel):
    height: int
    width: int
    x: int
    y: int
    
class FaceBase(BaseModel):
    bounding_box: str
    gender: str
    age: float

class Face(FaceBase):
    id: int

    class Config:
        from_attributes = True

class ImageBase(BaseModel):
    filename: str

class Image(ImageBase):
    id: int
    faces: List[Face] = []

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    id: int
    images: List[Image] = []
    total_faces: int
    total_men: int
    total_women: int
    avg_age_men: Optional[float]
    avg_age_women: Optional[float]

    class Config:
        from_attributes = True

class Task(BaseModel):
    id: int
    images: List[Image] = []
    
    class Config:
        from_attributes = True
