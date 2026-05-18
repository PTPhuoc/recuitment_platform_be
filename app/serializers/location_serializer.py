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