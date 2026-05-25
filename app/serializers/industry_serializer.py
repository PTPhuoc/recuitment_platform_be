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

class IndustryWithTransSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Industry
        fields = ['id', 'name']

    def get_name(self, obj):
        lang = self.context.get('language_code', "vie")
        translation = obj.translations.filter(language_code=lang).first()
        if translation:
            return translation.name
        return "No translation"