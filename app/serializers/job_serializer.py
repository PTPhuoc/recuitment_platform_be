import cloudinary
from rest_framework import serializers
from app.models import Job, Company, JobSaved, JobDesc, JobReq, FormOfWork, Education, Industry, JobLevel


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
            'job': {'read_only': True},
            'title': {'required': True},
            'description': {'required': True},
        }


class JobReqSerializer(serializers.ModelSerializer):
    form_of_work = serializers.PrimaryKeyRelatedField(
        many=True, queryset=FormOfWork.objects.all(), required=False
    )
    educations = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Education.objects.all(), required=False
    )
    industries = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Industry.objects.all(), required=False
    )
    job_level = serializers.PrimaryKeyRelatedField(
        many=True, queryset=JobLevel.objects.all(), required=False
    )
    class Meta:
        model = JobReq
        fields = '__all__'
        extra_kwargs = {
            'job': {'read_only': True},
        }


class JobCompanySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Company
        fields = ["name", "image"]

    def get_image(self, obj):
        if obj.logo_public_id:
            return cloudinary.CloudinaryImage(obj.logo_public_id).build_url()
        return None


class JobSerializer(serializers.ModelSerializer):
    descriptions = JobDescSerializer(many=True, required=False)
    require = JobReqSerializer(required=False)
    company_detail = JobCompanySerializer(source='company', read_only=True)

    class Meta:
        model = Job
        fields = ["id", "company", "company_detail", "name", "source_link", "description", "status",
                  "date_created", "date_limited", "descriptions", "require"]

    def create(self, validated_data):
        desc_data = validated_data.pop("descriptions", [])
        req_data = validated_data.pop("require", None)

        job = Job.objects.create(**validated_data)

        for desc_item in desc_data:
            JobDesc.objects.create(job=job, **desc_item)

        if req_data:
            form_of_work = req_data.pop('form_of_work', [])
            educations = req_data.pop('educations', [])
            industries = req_data.pop('industries', [])
            job_level = req_data.pop('job_level', [])

            job_req = JobReq.objects.create(job=job, **req_data)

            job_req.form_of_work.set(form_of_work)
            job_req.educations.set(educations)
            job_req.industries.set(industries)
            job_req.job_level.set(job_level)

        return job

    def update(self, instance, validated_data):
        desc_data = validated_data.pop("descriptions", None)
        req_data = validated_data.pop("require", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if desc_data is not None:
            current_ids = set(instance.descriptions.values_list('id', flat=True))
            new_ids = set()
            for desc_item in desc_data:
                desc_id = desc_item.get('id')
                if desc_id:
                    desc = instance.descriptions.get(id=desc_id)
                    desc_serializer = JobDescSerializer(desc, data=desc_item, partial=True)
                    desc_serializer.is_valid(raise_exception=True)
                    desc_serializer.save()
                    new_ids.add(desc_id)
                else:
                    new_desc = JobDesc.objects.create(job=instance, **desc_item)
                    new_ids.add(new_desc.id)
            to_delete = current_ids - new_ids
            if to_delete:
                instance.descriptions.filter(id__in=to_delete).delete()

        if req_data is not None:
            req_data.pop('job', None)
            req_data.pop('id', None)

            form_of_work = req_data.pop('form_of_work', None)
            educations = req_data.pop('educations', None)
            industries = req_data.pop('industries', None)
            job_level = req_data.pop('job_level', None)

            job_req, created = JobReq.objects.update_or_create(job=instance, defaults=req_data)

            if form_of_work is not None:
                job_req.form_of_work.set(form_of_work)
            if educations is not None:
                job_req.educations.set(educations)
            if industries is not None:
                job_req.industries.set(industries)
            if job_level is not None:
                job_req.job_level.set(job_level)

        return instance
