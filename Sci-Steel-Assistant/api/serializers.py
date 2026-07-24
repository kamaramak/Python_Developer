from rest_framework import serializers
from rest_framework.fields import Field

from navigate.models import AIQuery, MainDoc, Org


class BinaryToTextField(Field):
    """Кастомное поле для сериализатра.

    Преобразует бинарные данные в текстовые."""
    def to_representation(self, value):
        return value.decode('utf-8')


class MainDocSerializer(serializers.ModelSerializer):
    # doc_text = BinaryToTextField()
    orgs = serializers.StringRelatedField(many=True)

    class Meta:
        model = MainDoc
        fields = ('doc_id', 'doc_name', 'doc_text', 'doc_year', 'orgs')


class OrgSerializer(serializers.ModelSerializer):
    docs = serializers.StringRelatedField(many=True)

    class Meta:
        model = Org
        fields = ('org_id', 'org_name', 'docs')


class AIQueryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AIQuery
        fields = (
            'id',
            'label'
        )


class AIQueryUpdateSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.label = validated_data.get('label', instance.label)

    class Meta:
        model = AIQuery
        fields = ('label', )
