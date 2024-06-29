import logging
import time

import colorlog

from app.config import settings

logger = logging.getLogger()


class UTCFormatter(colorlog.ColoredFormatter):
    converter = time.gmtime


formatter = UTCFormatter(
    "[%(white)s%(asctime)s%(reset)s] [%(log_color)s%(levelname)s%(reset)s] - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

stream_handler = colorlog.StreamHandler()
stream_handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG if settings.env.debug else logging.INFO)
logger.addHandler(stream_handler)
