from django.db import models
from django_ulidfield import ULIDField

class IndustryTranslations(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    industry = models.ForeignKey('Industry', on_delete=models.CASCADE, related_name='translations', db_column="industryId")
    language_code = models.CharField(db_column="languageCode", max_length=5, null=True)
    name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'IndustryTranslations'