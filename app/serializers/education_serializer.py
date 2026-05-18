from rest_framework import serializers

from app.models import EducationTranslations, Education


class EducationTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationTranslations
        fields = ['id', 'education', 'language_code', 'name']


class EducationSerializer(serializers.ModelSerializer):
    translations = EducationTranslationSerializer(many=True, read_only=True)
    class Meta:
        model = Education
        fields = ['id', 'slug', 'translations']