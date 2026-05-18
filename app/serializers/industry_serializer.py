from rest_framework import serializers

from app.models import Industry, IndustryTranslations


class IndustryTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryTranslations
        fields = ['id', 'industry', 'language_code', 'name']


class IndustrySerializer(serializers.ModelSerializer):
    translations = IndustryTranslationSerializer(many=True, read_only=True)

    class Meta:
        model = Industry
        fields = ['id', 'slug', 'translations']
