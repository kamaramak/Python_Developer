import random

from .constants import SYMBOLS
from .models import URLMap


def get_unique_short_id():
    """Создание уникального короткого id."""
    while True:
        short_id = "".join(random.choices(SYMBOLS, k=6))
        if URLMap.query.filter_by(short=short_id).first() is None:
            return short_id


async def read_file(file):
    """
    Чтение файла.
    """
    if hasattr(file, "read"):
        content = file.read()
        if hasattr(file, "seek"):
            file.seek(0)
        return content
    if hasattr(file, "file"):
        return await file.read()
    if isinstance(file, bytes):
        return file
    with open(file, "rb") as file:
        return file.read()
