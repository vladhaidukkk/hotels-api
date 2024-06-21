import shutil

from fastapi import APIRouter, UploadFile, status

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/image", status_code=status.HTTP_201_CREATED)
def upload_image(image: UploadFile):
    with open(f"app/static/images/{image.filename}", "wb") as file_obj:
        shutil.copyfileobj(image.file, file_obj)
