from django.db import models
from django_ulidfield import ULIDField
from app.models import Account


class Employer(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    account_id = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='employer', db_column='accountId')
    name = models.CharField(max_length=100)
    image = models.TextField(null=True)
    description = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, db_column='dateCreated')

    class Meta:
        db_table = 'Employer'
