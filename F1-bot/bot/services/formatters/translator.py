from googletrans import Translator
from googletrans.models import Translated

from bot.core import cache
from bot.core.constants import TRANSLATE_CACHE_TTL

translator = Translator()


async def translate(text: str, src="en", dest="ru") -> str:
    """Перевод с кэшированием"""
    cache_key = f"{src}->{dest}:{text}"

    cached = await cache.get(cache_key)
    if cached:
        return cached

    translation: Translated = await translator.translate(
        text, src=src, dest=dest
    )
    await cache.set(cache_key, translation.text, TRANSLATE_CACHE_TTL)
    return translation.text
