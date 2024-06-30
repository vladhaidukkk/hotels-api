import logging
import time

import colorlog
import logtail

from app.config import settings

logger = logging.getLogger(settings.env.mode)


class ColoredUTCFormatter(colorlog.ColoredFormatter):
    converter = time.gmtime


formatter = ColoredUTCFormatter(
    "[%(white)s%(asctime)s%(reset)s] [%(log_color)s%(levelname)s%(reset)s] - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

stream_handler = colorlog.StreamHandler()
stream_handler.setFormatter(formatter)
logtail_handler = logtail.LogtailHandler(
    source_token=settings.app.bs.token, level=logging.INFO
)

logger.addHandler(stream_handler)
if settings.app.bs.enabled:
    logger.addHandler(logtail_handler)

logger.setLevel(logging.DEBUG if settings.env.debug else logging.INFO)
