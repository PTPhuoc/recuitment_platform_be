from rest_framework import serializers

from app.models import JobLevelTranslations, JobLevel


class JobLevelTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobLevelTranslations
        fields = ['id', 'job_level_id', 'language_code', 'name']


class JobLevelSerializer(serializers.ModelSerializer):
    translations = JobLevelTranslationSerializer(many=True, read_only=True)

    class Meta:
        model = JobLevel
        fields = ['id', 'slug', 'translations']
