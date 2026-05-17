"""Настройка админ-зоны проекта."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UsAdm

from .models import Follow, User


@admin.register(User)
class UserAdmin(UsAdm):
    """Админ-зона для модели User."""

    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
    )
    list_filter = ("role",)
    list_editable = ("role",)
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )


# Добавление дополнительных полей в админ-зону для модели User
UserAdmin.fieldsets += (
    (
        "Дополнительно",
        {
            "fields": (
                "avatar",
                "role",
            )
        },
    ),
)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Админ-зона для модели Follow."""

    list_display = ("user", "following")
