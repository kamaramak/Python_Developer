from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import SYMBOLS, get_unique_short_id


@app.route("/api/id/", methods=["POST"])
def create_short_link():
    """
    Создание коротких ссылок.
    """
    if not request.data:
        raise InvalidAPIUsage("Отсутствует тело запроса")
    data = request.get_json()
    if "url" not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    url = data["url"]
    if "custom_id" in data:
        custom_id = data["custom_id"]
        if (
            URLMap.query.filter_by(short=custom_id).first() is not None
            or custom_id == "files"
        ):
            raise InvalidAPIUsage(
                "Предложенный вариант короткой ссылки уже существует."
            )
        if len(custom_id) > 16 or any([c not in SYMBOLS for c in custom_id]):
            raise InvalidAPIUsage(
                "Указано недопустимое имя для короткой ссылки"
            )
    else:
        custom_id = get_unique_short_id()
    urlmap = URLMap(original=url, short=custom_id)
    db.session.add(urlmap)
    db.session.commit()
    short_link = "http://localhost/" + urlmap.short
    return jsonify({"url": url, "short_link": short_link}), HTTPStatus.CREATED


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_original_link(short_id):
    """
    Получение оригинальной ссылки по короткой.
    """
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage("Указанный id не найден", HTTPStatus.NOT_FOUND)
    url = urlmap.original
    return jsonify({"url": url}), HTTPStatus.OK
