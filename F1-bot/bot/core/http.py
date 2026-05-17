import asyncio

import aiohttp
from aiohttp import ClientConnectorError, ClientResponseError


async def get_response(url: str):
    """Отправка асинхронного запроса к API."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # Проверяем статус ответа
                if response.status == 404:
                    print(f"❌ 404 Not Found: {url}")
                    return None

                # Другие ошибки (500, 403 и т.д.)
                if response.status >= 400:
                    print(f"❌ Ошибка {response.status}: {url}")
                    return None

                # Успешный ответ
                return await response.json()

    except ClientResponseError as e:
        print(f"❌ Ошибка ответа: {e.status} - {url}")
        return None
    except ClientConnectorError as e:
        print(f"❌ Ошибка подключения: {e} - {url}")
        return None
    except asyncio.TimeoutError:
        print(f"❌ Таймаут: {url}")
        return None
    except Exception as e:
        print(f"❌ Неизвестная ошибка: {e} - {url}")
        return None
