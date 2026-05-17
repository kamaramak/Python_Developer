"""Пермишены, используемые в проекте."""

import re

from rest_framework import permissions


class IsCurrentUserOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только к объектам авторства текущего пользователя,
    или только на чтение.
    """

    def has_permission(self, request, view):
        path = request.path
        if re.match("^.+/me/$|^.+/me/avatar/$", path):
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ("PUT", "DELETE", "POST"):
            return request.user == obj
        return False


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешает доступ только автору объекта или только на чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ("PATCH", "DELETE"):
            return request.user == obj.author
        return False
