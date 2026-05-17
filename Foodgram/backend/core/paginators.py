"""Пагинаторы, используемые в проекте."""

from rest_framework.pagination import PageNumberPagination


class PageLimitNumberPagination(PageNumberPagination):
    """
    Дефолтный пагинатор PageNumberPagination с переопределенным названием поля,
    отвечающего за количество результатов в выдаче.
    """

    page_size_query_param = "limit"
