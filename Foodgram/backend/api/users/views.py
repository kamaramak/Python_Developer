"""Представления для приложения users."""

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Follow, User

from .serializers import (
    FollowReadSerializer,
    FollowWriteSerializer,
    SignUpSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """Работа с пользователями."""

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return SignUpSerializer
        return UserSerializer

    @action(
        detail=False,
        methods=["put", "delete"],
        permission_classes=[
            permissions.IsAuthenticated,
        ],
        url_path="me/avatar",
    )
    def avatar(self, request):
        """Добавление и изменение аватара текущего пользователя."""
        if request.method == "PUT":
            data = request.data.copy()
            if "avatar" in data:
                data = {
                    "avatar": data.pop("avatar"),
                }
            serializer = self.get_serializer(
                request.user,
                data=data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"avatar": serializer.data.get("avatar")})
        if request.method == "DELETE":
            user = User.objects.get(id=request.user.id)
            user.avatar.delete()
            return Response(status=204)
        return Response(
            {"error": "Метод не разрешен"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class FollowViewSet(viewsets.ModelViewSet):
    """Работа с подписками: оформление и удаление подписки."""

    SERIALIZERS = {
        "write": FollowWriteSerializer,
        "read": FollowReadSerializer,
    }

    permission_classes = [
        IsAuthenticated,
    ]
    http_method_names = ["get", "post", "delete"]

    def get_serializer_class(self):
        if self.action == "list":
            return self.SERIALIZERS["read"]
        return self.SERIALIZERS["write"]

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        following = kwargs.get("pk")
        # Проверка на существование пользователя, на которого подписка
        get_object_or_404(User, id=following)
        data = {"following": following}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=self.request.user)
        serializer = self.SERIALIZERS["read"](
            instance, context=self.get_serializer_context()
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        following = get_object_or_404(User, id=kwargs.get("pk"))
        instance = Follow.objects.filter(
            user=request.user, following=following
        )
        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Вы не подписаны на этого пользователя!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
