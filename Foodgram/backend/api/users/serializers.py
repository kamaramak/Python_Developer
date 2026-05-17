"""
Сериализаторы для приложения users для моделей:
    - User,
    - Follow.
"""

from rest_framework import serializers

from core.constants import (
    MAX_EMAIL_LENGTH,
    MAX_FIRST_NAME_LENGTH,
    MAX_LAST_NAME_LENGTH,
)
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe
from users.models import Follow, User


class SignUpSerializer(serializers.ModelSerializer):
    """Оформление подписки пользователем."""

    email = serializers.EmailField(max_length=MAX_EMAIL_LENGTH)
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(
        required=True, max_length=MAX_FIRST_NAME_LENGTH
    )
    last_name = serializers.CharField(
        required=True, max_length=MAX_LAST_NAME_LENGTH
    )

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        username = attrs["username"]
        email = attrs["email"]
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {
                    "username": (
                        f"Пользователь с именем {username} уже существует."
                    ),
                }
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {
                    "email": (f"Пользователь с email {email} уже существует."),
                }
            )
        return attrs

    def validate_username(self, value):
        """Имя пользователя не должно быть 'me'."""
        if value == "me":
            raise serializers.ValidationError(
                "В качестве имени пользователя запрещено использовать 'me'"
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    """Преобразование данных из модели User для чтения."""

    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "avatar",
        )

    def validate(self, attrs):
        if "avatar" not in attrs:
            raise serializers.ValidationError()
        return attrs

    def get_is_subscribed(self, obj):
        """Возвращает True если текущий пользователь подписан на автора."""
        request = self.context.get("request")
        return (
            request
            and request.user.is_authenticated
            and Follow.objects.filter(
                user=request.user, following=obj
            ).exists()
        )


class RecipeInPostSerializer(serializers.ModelSerializer):
    """Рецепт для выдачи в качестве одного из полей на POST запрос."""

    image = serializers.ImageField(
        allow_empty_file=False,
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class FollowWriteSerializer(serializers.ModelSerializer):
    """Создание подписки текущего пользователя на автора."""

    following = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    class Meta:
        model = Follow
        fields = ("following",)

    def validate(self, attrs):
        user = self.context.get("request").user
        id_to_follow = attrs.get("following").id
        if user.id == id_to_follow:
            raise serializers.ValidationError(
                "Невозможно оформить подписку на себя!"
            )
        if Follow.objects.filter(
            user=user, following__id=id_to_follow
        ).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя!"
            )
        return attrs


class FollowReadSerializer(serializers.ModelSerializer):
    """Выдача подписки текущего пользователя на автора."""

    email = serializers.ReadOnlyField(source="following.email")
    id = serializers.ReadOnlyField(source="following.id")
    username = serializers.ReadOnlyField(source="following.username")
    first_name = serializers.ReadOnlyField(source="following.first_name")
    last_name = serializers.ReadOnlyField(source="following.last_name")
    avatar = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
            "avatar",
        )
        read_only_fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
            "avatar",
        )

    def get_avatar(self, obj):
        """Возвращает адрес аватара пользователя."""
        avatar = obj.following.avatar
        return avatar.url or ""

    def get_recipes_count(self, obj):
        """Возвращает количество рецептов автора, на которого подписан юзер."""
        return Recipe.objects.filter(author=obj.following).count()

    def get_recipes(self, obj):
        """Возвращает рецепты автора, на которого подписан юзер."""
        request = self.context.get("request")
        recipes_limit = request.query_params.get("recipes_limit")
        if recipes_limit:
            recipes_limit = int(recipes_limit)
        recipes = Recipe.objects.filter(author=obj.following)[:recipes_limit]
        serializer = RecipeInPostSerializer(recipes, many=True)
        return serializer.data

    def get_is_subscribed(self, obj):
        """Возвращает True если текущий пользователь подписан на автора."""
        request = self.context.get("request")
        # Выполняю проверку разом всех 3 пунктов
        return (
            request
            and request.user.is_authenticated
            and Follow.objects.filter(
                user=request.user, following=obj.following
            ).exists()
        )
