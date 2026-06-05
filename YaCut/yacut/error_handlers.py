from http import HTTPStatus

from flask import jsonify, render_template

from . import app


class InvalidAPIUsage(Exception):
    """
    Кастомный класс ошибок.
    """

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {"message": self.message}


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """
    Универсальный обработчик ошибок, возвращающий сообщение и код ошибки.
    """
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    """Кастомный обработчик ошибки 404."""
    return render_template("404.html"), HTTPStatus.NOT_FOUND
