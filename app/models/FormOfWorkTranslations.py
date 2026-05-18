from django.db import models
from django_ulidfield import ULIDField

class FormOfWorkTranslations(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    form_of_work = models.ForeignKey('FormOfWork', on_delete=models.CASCADE, related_name="translations", db_column='FormOfWorkId')
    language_code = models.CharField(db_column='LanguageCode', max_length=5, null=True)
    name = models.CharField(db_column='Name', max_length=255, null=True)

    class Meta:
        db_table = 'FormOfWorkTranslations'