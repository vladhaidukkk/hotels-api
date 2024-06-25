import shutil

from fastapi import APIRouter, UploadFile, status

from app.tasks.tasks import process_image

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/image", status_code=status.HTTP_201_CREATED)
def upload_image(image: UploadFile):
    img_path = f"app/static/images/{image.filename}"
    with open(img_path, "wb") as file_obj:
        shutil.copyfileobj(image.file, file_obj)
    process_image.delay(img_path)
