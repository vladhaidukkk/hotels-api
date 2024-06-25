from pathlib import Path

from PIL import Image

from app.tasks.celery_app import celery_app


@celery_app.task
def process_image(path: str) -> None:
    img_path = Path(path)
    img = Image.open(img_path)
    for width, height in [(1000, 500), (200, 100)]:
        resized_img = img.resize(size=(width, height))
        resized_img.save(f"app/static/images/resized_{width}_{height}_{img_path.name}")
