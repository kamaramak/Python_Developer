"""Модуль для загрузки ингредиентов и тегов из CSV файлов в базу данных."""

import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    """Главный класс для загрузки данных."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            default=os.path.join(settings.BASE_DIR, "data"),
        )

    def handle(self, *args, **options):
        path = options["path"]

        # Загрузка ингредиентов
        self.load_ingredients(os.path.join(path, "ingredients.csv"))

        # Загрузка тегов
        self.load_tags(os.path.join(path, "tags.csv"))

    def load_ingredients(self, file_path):
        """Загрузка ингредиентов из файла CSV."""
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            i = 1
            for row in reader:
                Ingredient.objects.get_or_create(
                    id=i,
                    defaults={
                        "name": row["name"],
                        "measurement_unit": row["measurement_unit"],
                    },
                )
                print(i)
                i += 1

    def load_tags(self, file_path):
        """Загрузка тегов из файла CSV."""
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            i = 1
            for row in reader:
                Tag.objects.get_or_create(
                    id=i,
                    defaults={
                        "name": row["name"],
                        "slug": row["slug"],
                    },
                )
                print(i)
                i += 1
