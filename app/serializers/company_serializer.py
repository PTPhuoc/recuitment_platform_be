from rest_framework import serializers

from app.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        extra_kwargs = {
            "name": { "required": True },
            "company_size": { "required": True },
            "industry": { "required": True },
            "location": { "required": True },
            "email_domain": { "required": True },
        }