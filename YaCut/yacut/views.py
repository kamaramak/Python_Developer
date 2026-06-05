from flask import flash, redirect, render_template

from . import app, db
from .constants import SYMBOLS
from .disk import async_upload_files_to_API
from .forms import ShortLinkForm, UploadFilesForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route("/", methods=["GET", "POST"])
def short_link_view():
    """Создание короткой ссылки."""
    form = ShortLinkForm()
    result = None
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        if custom_id:
            if (
                URLMap.query.filter_by(short=custom_id).first() is not None
                or custom_id == "files"
            ):
                flash("Предложенный вариант короткой ссылки уже существует.")
                return render_template("index.html", form=form, result=result)
            for char in custom_id:
                if char not in SYMBOLS:
                    flash("Указано недопустимое имя для короткой ссылки")
                    return render_template(
                        "index.html", form=form, result=result
                    )
        else:
            custom_id = get_unique_short_id()
        urlmap = URLMap(original=original_link, short=custom_id)
        db.session.add(urlmap)
        db.session.commit()
        result = urlmap.short
    return render_template("index.html", form=form, result=result)


@app.route("/<string:short_id>", methods=["GET", "POST"])
def redirect_view(short_id):
    """Перенаправление на оригинальный адрес через короткую ссылку."""
    urlmap = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(urlmap.original)


@app.route("/files", methods=["GET", "POST"])
async def upload_files_view():
    """Загрузка файлов."""
    form = UploadFilesForm()
    files = None
    if form.validate_on_submit():
        urls = await async_upload_files_to_API(form.files.data)
        files = []
        for url in urls:
            short_id = get_unique_short_id()
            urlmap = URLMap(original=url[0], short=short_id)
            db.session.add(urlmap)
            db.session.commit()
            files.append((urlmap.short, url[1]))
    return render_template("upload_files.html", form=form, files=files)
