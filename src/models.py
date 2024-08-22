
from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from .db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    images = relationship("Image", back_populates="task", cascade="all, delete-orphan")

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship("Task", back_populates="images")
    faces = relationship("Face", back_populates="image", cascade="all, delete-orphan")

class Face(Base):
    __tablename__ = "faces"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey('images.id'))
    bounding_box = Column(String)
    gender = Column(String)
    age = Column(Float)
    image = relationship("Image", back_populates="faces")
