import logging
import time

from app.config import settings

logger = logging.getLogger()


class UTCFormatter(logging.Formatter):
    converter = time.gmtime


formatter = UTCFormatter(
    "[%(asctime)s] [%(levelname)s] - %(message)s", datefmt="%Y-%m-%dT%H:%M:%S"
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG if settings.env.debug else logging.INFO)
logger.addHandler(stream_handler)
