import json
from pathlib import Path
from sqlalchemy.orm import Session
from . import models, schemas

def create_task(db: Session):
    db_task = models.Task()
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def add_image_to_task(db: Session, task_id: int, filename: str):
    db_image = models.Image(filename=filename, task_id=task_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def add_face_to_image(db: Session, image_id: int, bounding_box: str, gender: str, age: float):
    bounding_box_str = json.dumps(bounding_box)
    db_face = models.Face(image_id=image_id, bounding_box=bounding_box_str, gender=gender, age=age)
    db.add(db_face)
    db.commit()
    db.refresh(db_face)
    return db_face

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    image_paths = [image.filename for image in task.images]
    db.delete(task)
    db.commit()
    for image_path in image_paths:
        path = Path(f"images/{image_path}")
        if path.is_file():
            path.unlink()
