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