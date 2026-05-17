"""
Модели приложения users:
    - User,
    - Follow.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants import ADMIN, MAX_ROLE_LENGTH, ROLE_CHOICES, USER


class User(AbstractUser):
    """Кастомная модель для работы с пользователем."""

    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to="users/",
        null=True,
        default=None,
        verbose_name="Аватар",
    )
    role = models.CharField(
        max_length=MAX_ROLE_LENGTH,
        choices=ROLE_CHOICES,
        default="user",
        verbose_name="Роль",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def is_admin(self):
        """Возвращает True если пользователь является администратором."""
        return self.is_staff or self.role == ADMIN

    @property
    def is_user(self):
        """Возвращает True если пользователь является юзером."""
        return self.role == USER

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Follow(models.Model):
    """Модель для работы с подписками пользователей."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follow_user"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follow_following"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ("following",)
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["user", "following"],
            ),
        ]

    def __str__(self):
        return f"{self.user} подписан на {self.following}"
