"""Дефолтный модуль Django"""

from django.apps import AppConfig


class InteractionsConfig(AppConfig):
    """Дефолтный класс Django"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "interactions"
