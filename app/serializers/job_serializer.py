from rest_framework import serializers
from app.models import Job, JobSaved, JobDesc, JobReq

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True},
            'source_link': {'required': True},
            'company': {'required': True},
        }

class JobSavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSaved
        fields = '__all__'
        extra_kwargs = {
            'account': {'required': True},
            'job': {'required': True},
        }

class JobDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDesc
        fields = '__all__'
        extra_kwargs = {
            'job': {'required': True},
            'title': {'required': True},
            'description': {'required': True},
        }

class JobReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobReq
        fields = '__all__'
        extra_kwargs = {
            'job': {'required': True},
        }
