from django.db import models
from django_ulidfield import ULIDField

class Locations(models.Model):
    LOCATION_TYPES = [
        ('country', 'Country'),
        ('city', 'City'),
        ('district', 'District'),
    ]

    id = ULIDField(primary_key=True, db_index=True)
    type = models.CharField(max_length=20, choices=LOCATION_TYPES, db_index=True)
    slug = models.CharField(max_length=100, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, db_index=True, related_name='children', db_column='parentId', null=True)

    class Meta:
        db_table = 'Locations'