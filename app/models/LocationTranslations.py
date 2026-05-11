from django.db import models
from django_ulidfield import ULIDField

from app.models import Locations


class LocationTranslations(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    location_id = models.ForeignKey(Locations, on_delete=models.CASCADE, related_name='translations', db_column='locationId')
    language_code = models.CharField(max_length=5, db_column="languageCode", null=True)
    name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'LocationTranslations'