from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
import os
from . import schemas, crud
from .db import engine, Base, get_db
from .utils import detect_faces

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/tasks/", response_model=schemas.Task)
def create_task(db: Session = Depends(get_db)):
    return crud.create_task(db)

@app.get("/tasks/{task_id}", response_model=schemas.TaskBase)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    total_faces = 0
    total_men = 0
    total_women = 0
    total_age_men = 0
    total_age_women = 0

    for image in task.images:
        for face in image.faces:
            total_faces += 1
            if face.gender == 'male':
                total_men += 1
                total_age_men += face.age
            elif face.gender == 'female':
                total_women += 1
                total_age_women += face.age



    avg_age_men = total_age_men / total_men if total_men > 0 else None
    avg_age_women = total_age_women / total_women if total_women > 0 else None

    response_data = {
        "id": task.id,
        "images": task.images,
        "total_faces": total_faces,
        "total_men": total_men,
        "total_women": total_women,
        "avg_age_men": avg_age_men,
        "avg_age_women": avg_age_women
    }

    return response_data

@app.post("/tasks/{task_id}/images/")
async def add_image(task_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Invalid image type")

    file_path = f"images/{file.filename}"
    with open(file_path, "wb") as image:
        content = await file.read()
        image.write(content)

    image_record = crud.add_image_to_task(db, task_id, file.filename)
    faces_data = detect_faces(file_path)
    for face in faces_data:
        crud.add_face_to_image(db, image_record.id, face['bounding_box'], face['gender'], face['age'])

    return {"filename": file.filename}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    crud.delete_task(db, task_id)
    return {"message": "Task deleted"}
