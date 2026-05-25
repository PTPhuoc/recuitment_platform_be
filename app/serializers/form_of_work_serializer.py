from rest_framework import serializers

from app.models import FormOfWork, FormOfWorkTranslations

class FormOfWorkTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormOfWorkTranslations
        fields = ["id",'form_of_work', 'language_code', 'name']

class FormOfWorkSerializer(serializers.ModelSerializer):
    translations = FormOfWorkTranslationSerializer(many=True, read_only=True)
    class Meta:
        model = FormOfWork
        fields = ['id', 'slug', "translations"]

class FormOfWorkWithTransSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = FormOfWork
        fields = ['id', 'slug', "name"]

    def get_name(self, obj):
        lang = self.context.get("language_code", "vie")
        translation = obj.translations.filter(language_code=lang).first()
        if translation:
            return translation.name
        return "No translation"