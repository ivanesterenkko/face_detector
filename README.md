Описание

Этот сервис предоставляет API для управления заданиями, которые включают загрузку изображений, обработку их с помощью стороннего сервиса FaceCloud для определения лиц на изображениях, а также для сбора статистики по лицам. Сервис поддерживает следующие операции: добавление задания, получение задания, удаление задания и добавление изображений в задания.

Технологии

Python 3.8+
FastAPI 
SQLAlchemy 
PostgreSQL 
FaceCloud API 
Docker и docker-compose

Установка

Убедитесь, что Docker и Docker Compose установлены на вашем компьютере.
Запустите контейнеры с помощью Docker Compose:

docker-compose up --build

Запуск сервиса:

uvicorn src.app:app --reload


Добавление задания POST /tasks
Ответ:
{
  "task_id": "task_id"
  "images": []
}

Получение задания GET /tasks/{task_id}
Тело запроса:
{
  "task_id": "id"
}
Ответ:
{
  "id": 1,
  "images": [
    {
      "filename": "photo_2024-08-19 18.47.40.jpeg",
      "id": 1,
      "faces": [
        {
          "bounding_box": "{\"height\": 244, \"width\": 187, \"x\": 644, \"y\": 223}",
          "gender": "male",
          "age": 23,
          "id": 1
        },
        {
          "bounding_box": "{\"height\": 232, \"width\": 174, \"x\": 391, \"y\": 348}",
          "gender": "female",
          "age": 23,
          "id": 2
        }
      ]
    }
  ],
  "total_faces": 2,
  "total_men": 1,
  "total_women": 1,
  "avg_age_men": 23,
  "avg_age_women": 23
}

Удаление задания DELETE /tasks/{task_id}
Тело запроса:
{
  "task_id": "id"
}
Ответ:
{
  "message": "Task deleted"
}

Добавление изображения (Сервис поддерживает только JPEG изображения) POST /tasks/{task_id}/images
Тело запроса:
{
  "task_id": "id"
  "file": "filename"
}
Ответ:
{
  "filename": "photo_2024-08-19 18.47.40.jpeg"
}
