from django.db import models
from django_ulidfield import ULIDField

class JobLevelTranslations(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    job_level_id = models.ForeignKey('JobLevel', on_delete=models.CASCADE, related_name='translations', db_column="jobLevelId")
    language_code = models.CharField(max_length=5, db_column="languageCode", null=True)
    name = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'JobLevelTranslations'