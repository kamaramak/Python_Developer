import asyncio
import urllib
from http import HTTPStatus

import aiohttp

from .constants import AUTH_HEADERS, DOWNLOAD_LINK, UPLOAD_LINK
from .utils import read_file


async def async_upload_files_to_API(files: list):
    """
    Асинхронная загрузка файлов на Яндекс.Диск.
    Возвращает список прямых ссылок для скачивания.
    """
    if not files:
        return []

    tasks = []
    async with aiohttp.ClientSession(headers=AUTH_HEADERS) as session:
        for file in files:
            tasks.append(
                asyncio.create_task(
                    upload_file_and_get_link_to_download(session, file)
                )
            )
        locations = await asyncio.gather(*tasks)
    return locations


async def upload_file_and_get_link_to_download(
    session: aiohttp.ClientSession, file
):
    """
    Загрузка одного файла на Диск и получение ссылки на него.
    """
    if hasattr(file, "filename"):
        filename = file.filename
    elif hasattr(file, "name"):
        filename = file.name
    else:
        filename = "unknown"

    upload_url = await get_upload_url(session, filename)
    file_content = await read_file(file)
    await upload_file(session, upload_url, file_content)
    location = await get_download_link(session, filename)
    return location, filename


async def get_upload_url(session: aiohttp.ClientSession, filename: str):
    """
    Получение URL для загрузки файла.
    """
    payload = {"path": f"app:/{filename}", "overwrite": "False"}  # noqa
    async with session.get(UPLOAD_LINK, params=payload) as response:
        data = await response.json()
        if response.status != HTTPStatus.OK:
            message = data.get("message", "Unknown error")
            raise Exception(f"Ошибка получения URL: {message}")
        return data["href"]


async def upload_file(
    session: aiohttp.ClientSession, upload_url: str, content: bytes
):
    """
    Загрузка файла на диск по полученной ссылке.
    """
    async with session.put(upload_url, data=content) as response:
        if response.status not in (HTTPStatus.OK, HTTPStatus.CREATED):
            text = await response.text()
            raise Exception(
                f"Ошибка загрузки файла: {response.status} - {text}"
            )


async def get_download_link(session: aiohttp.ClientSession, filename: str):
    """
    Получение прямой ссылки на скачивание файлов из Диска.
    """
    payload = {"path": f"app:/{filename}"}  # noqa
    async with session.get(DOWNLOAD_LINK, params=payload) as response:
        data = await response.json()
        if response.status != HTTPStatus.OK:
            message = data.get("message", "Unknown error")
            raise Exception(f"Ошибка получения ссылки: {message}")
        location = data["href"]
        location = urllib.parse.unquote(location)
        return location
