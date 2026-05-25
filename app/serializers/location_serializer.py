from rest_framework import serializers

from app.models import LocationTranslations, Locations


class LocationTranslationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationTranslations
        fields = ['id', 'language_code', 'location', 'name']


class LocationsSerializer(serializers.ModelSerializer):
    translations = LocationTranslationsSerializer(many=True, read_only=True)
    class Meta:
        model = Locations
        fields = ['id', 'type', 'slug', 'parent_id', 'translations']

class LocationWithTransSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Locations
        fields = ["id", "name", "parent_id"]

    def get_name(self, obj):
        lang = self.context.get('language_code', "vie")
        translation = obj.translations.filter(language_code=lang).first()
        if translation:
            return translation.name
        return "No translation"
