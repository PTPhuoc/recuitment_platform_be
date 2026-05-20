import cloudinary
from rest_framework import serializers

from app.models import Company, Industry, Locations, CompanyLocation, CompanyIndustry


class CompanySerializer(serializers.ModelSerializer):
    industries = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Industry.objects.all(), required=False
    )
    locations = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Locations.objects.all(), required=False
    )
    logo_url = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'slug', 'trading_name', 'website_url', 'logo_public_id', 'logo_url',
            'cover_public_id', 'cover_url',
                  'company_size', 'description', 'email_domain', 'is_claimed', 'is_verified',
                  'date_created', 'industries', 'locations']
        extra_kwargs = {
            "name": {"required": True},
            "company_size": {"required": True},
            "industries": {"required": True},
            "locations": {"required": True},
            "email_domain": {"required": True},
        }

    def create(self, validated_data):
        industries = validated_data.pop('industries', [])
        locations = validated_data.pop('locations', [])
        company = Company.objects.create(**validated_data)
        company.industries.set(industries)
        company.locations.set(locations)
        return company

    def update(self, instance, validated_data):
        industries = validated_data.pop('industries', None)
        locations = validated_data.pop('locations', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if industries is not None:
            instance.industries.set(industries)
        if locations is not None:
            instance.locations.set(locations)
        return instance

    def get_logo_url(self, obj):
        if obj.logo_public_id:
            return cloudinary.CloudinaryImage(obj.logo_public_id).build_url()
        return None

    def get_cover_url(self, obj):
        if obj.cover_public_id:
            return cloudinary.CloudinaryImage(obj.cover_public_id).build_url()
        return None



class CompanyIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyIndustry
        fields = ["id", "company", "industry"]


class CompanyLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyLocation
        fields = ["id", "company", "location", "detail_address"]
