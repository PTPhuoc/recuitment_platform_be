from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_403_FORBIDDEN
from django.db import models

from app.models import Education, EducationTranslations, FormOfWork, FormOfWorkTranslations, Industry, \
    IndustryTranslations, JobLevel, JobLevelTranslations, Locations, LocationTranslations, Company
from app.serializers import EducationSerializer, FormOfWorkSerializer, IndustrySerializer, JobLevelSerializer, \
    LocationsSerializer
from app.serializers.company_serializer import CompanyCategoriesSerializer


class WebAPI(viewsets.ModelViewSet):
    @action(methods=['get'], detail=False)
    def categories(self, request):
        lang = request.query_params.get('lang')
        education = Education.objects.all().order_by("-slug")
        form_of_work = FormOfWork.objects.all().order_by("-slug")
        industry = Industry.objects.all().order_by("-slug")
        jop_level = JobLevel.objects.all().order_by("-slug")
        location = Locations.objects.all().order_by("-slug")
        company = Company.objects.all().order_by("-name")
        if lang:
            education = education.prefetch_related(
                models.Prefetch("translations", queryset=EducationTranslations.objects.filter(language_code=lang))
            )
            form_of_work = form_of_work.prefetch_related(
                models.Prefetch("translations", queryset=FormOfWorkTranslations.objects.filter(language_code=lang))
            )
            industry = industry.prefetch_related(
                models.Prefetch("translations", queryset=IndustryTranslations.objects.filter(language_code=lang))
            )
            jop_level = jop_level.prefetch_related(
                models.Prefetch("translations", queryset=JobLevelTranslations.objects.filter(language_code=lang))
            )
            location = location.prefetch_related(
                models.Prefetch("translations", queryset=LocationTranslations.objects.filter(language_code=lang))
            )
        return Response({
            "education": EducationSerializer(education, many=True).data,
            "form_of_work": FormOfWorkSerializer(form_of_work, many=True).data,
            "industry": IndustrySerializer(industry, many=True).data,
            "job_level": JobLevelSerializer(jop_level, many=True).data,
            "location": LocationsSerializer(location, many=True).data,
            "company": CompanyCategoriesSerializer(company, many=True).data
        })
