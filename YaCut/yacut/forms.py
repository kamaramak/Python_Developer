from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class ShortLinkForm(FlaskForm):
    """Форма для создания короткой ссылки."""

    original_link = URLField(
        "Длинная ссылка",
        validators=[
            Length(1, 2083),
            DataRequired(message="Обязательное поле"),
        ],
    )
    custom_id = URLField(
        "Ваш вариант короткой ссылки", validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField("Создать")


class UploadFilesForm(FlaskForm):
    """Форма для загрузки файлов."""

    files = MultipleFileField(DataRequired(message="Файл не выбран"))
    submit = SubmitField("Загрузить")
