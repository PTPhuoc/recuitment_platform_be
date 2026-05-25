from rest_framework import serializers

from app.models import JobLevelTranslations, JobLevel


class JobLevelTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobLevelTranslations
        fields = ['id', 'job_level', 'language_code', 'name']


class JobLevelSerializer(serializers.ModelSerializer):
    translations = JobLevelTranslationSerializer(many=True, read_only=True)

    class Meta:
        model = JobLevel
        fields = ['id', 'slug', 'translations']

class JobLevelWithTransSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = JobLevel
        fields = ['id', 'name']

    def get_name(self, obj):
        lang = self.context.get('language_code', "vie")
        translation = obj.translations.filter(language_code=lang).first()
        if translation:
            return translation.name
        return "No translation"
