from django.db import models
from django_ulidfield import ULIDField

# models/Company.py
class Company(models.Model):
    id = ULIDField(primary_key=True, db_index=True)
    name = models.CharField(max_length=255, db_index=True, default="")
    slug = models.CharField(max_length=255, db_index=True, default="")
    trading_name = models.CharField(max_length=20, db_column="tradingName", default="", null=True)
    website_url = models.TextField(null=True)
    logo_public_id = models.TextField(null=True)
    cover_public_id = models.TextField(null=True)
    company_size = models.CharField(max_length=100, null=True, default="")
    description = models.TextField()
    email_domain = models.CharField(max_length=20, db_column='emailDomain', default="@name.com")
    is_claimed = models.BooleanField(default=False, db_column='isClaimed')
    is_verified = models.BooleanField(default=False, db_column='isVerified')
    date_created = models.DateTimeField(auto_now_add=True, db_column='dateCreated')

    industries = models.ManyToManyField(
        'Industry',
        through='CompanyIndustry',
        related_name='companies',
    )
    locations = models.ManyToManyField(
        'Locations',
        through='CompanyLocation',
        related_name='companies',
    )

    class Meta:
        db_table = 'Company'
