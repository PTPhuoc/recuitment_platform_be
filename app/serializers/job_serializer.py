from rest_framework import serializers
from app.models import Job, JobSaved, JobDesc, JobReq


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


class JobSerializer(serializers.ModelSerializer):
    descriptions = JobDescSerializer(many=True, required=False)
    require = JobReqSerializer(required=False)

    class Meta:
        model = Job
        fields = ["id", "company", "name", "source_link", "description", "status", "date_created", "date_limited",
                  "descriptions", "require"]

    def create(self, validated_data):
        desc_data = validated_data.pop("descriptions", [])
        req_data = validated_data.pop("require", None)

        job = Job.objects.create(**validated_data)

        for desc_item in desc_data:
            JobDesc.objects.create(job=job, **desc_item)

        if req_data:
            JobReq.objects.create(job=job, **req_data)

        return job

    def update(self, instance, validated_data):
        desc_data = validated_data.pop("descriptions", None)
        req_data = validated_data.pop("require", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if desc_data is not None:
            current_ids = set(instance.desc.values_list('id', flat=True))
            new_ids = set()
            for desc_item in desc_data:
                desc_id = desc_item.get('id')
                if desc_id:
                    desc = instance.desc.get(id=desc_id)
                    desc_serializer = JobDescSerializer(desc, data=desc_item, partial=True)
                    desc_serializer.is_valid(raise_exception=True)
                    desc_serializer.save()
                    new_ids.add(desc_id)
                else:
                    new_desc = JobDesc.objects.create(job=instance, **desc_item)
                    new_ids.add(new_desc.id)
            to_delete = current_ids - new_ids
            if to_delete:
                instance.desc.filter(id__in=to_delete).delete()

        if req_data is not None:
            req_data.pop('job', None)
            JobReq.objects.update_or_create(job=instance, defaults=req_data)

        return instance
