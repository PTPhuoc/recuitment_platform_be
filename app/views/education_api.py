from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from django.db import models

from app.models import Education, EducationTranslations
from app.serializers.education_serializer import EducationSerializer


class EducationAPI(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    @action(methods=['get'], detail=False)
    def many_search(self, request):
        lang = request.query_params.get('lang')
        name = request.query_params.get('name')
        slug = request.query_params.get('slug')
        queryset = self.get_queryset().order_by('slug')
        if lang:
            queryset = queryset.prefetch_related(
                models.Prefetch("translations", queryset=EducationTranslations.objects.filter(language_code=lang))
            )
        if name:
            queryset = queryset.prefetch_related(
                models.Prefetch("translations", queryset=EducationTranslations.objects.filter(name=name))
            )
        if slug:
            queryset = queryset.filter(slug=slug)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        response.data['status'] = "Success"
        return response

    @action(methods=['get'], detail=False)
    def many(self, request):
        lang = request.query_params.get('lang')
        queryset = self.get_queryset().order_by('-slug')
        if lang:
            queryset = queryset.prefetch_related(
                models.Prefetch('translations', queryset=EducationTranslations.objects.filter(language_code=lang))
            )
        serializer = EducationSerializer(queryset, many=True)
        return Response({'status': "Success", "education": serializer.data})

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def save(self, request):
        user = request.user
        if user.role != 'admin':
            return Response({'status': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        education_id = data.get('id')
        slug = data.get('slug')
        lang = data.get('lang')
        name = data.get('name')
        if not lang or not name:
            return Response({'status': 'Empty value', 'message': 'lang and name are required'}, status=400)

        if education_id:
            education = get_object_or_404(Education, id=education_id)
            education_serializer = EducationSerializer(education, data=data, partial=True)
            education_serializer.is_valid(raise_exception=True)
            education = education_serializer.save()
            created_education = False
        elif slug:
            education = Education.objects.filter(slug=slug).first()
            if not education:
                education_serializer = EducationSerializer(data=data)
                education_serializer.is_valid(raise_exception=True)
                education = education_serializer.save()
                created_education = True
            else:
                created_education = False
        else:
            education_serializer = EducationSerializer(data=data)
            education_serializer.is_valid(raise_exception=True)
            education = education_serializer.save()
            created_education = True

        translation, created_trans = EducationTranslations.objects.update_or_create(
            education_id=education,
            language_code=lang,
            defaults={'name': name}
        )
        if created_education or created_trans:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK

        return Response({'status': 'Success'}, status=status_code)

    @action(methods=['delete'], detail=False, permission_classes=[IsAuthenticated])
    def slug(self, request):
        user = request.user
        if user.role != 'admin':
            return Response({'status': 'Not permitted'}, status=status.HTTP_401_UNAUTHORIZED)

        education_id = request.query_params.get('id')
        if not education_id:
            return Response({'status': 'Empty value', 'message': 'Require ID of education'},
                            status=status.HTTP_400_BAD_REQUEST)

        education = get_object_or_404(Education, id=education_id)
        education.delete()
        return Response({'status': 'Success'}, status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=False, permission_classes=[IsAuthenticated])
    def translation(self, request):
        user = request.user
        if user.role != 'admin':
            return Response({'status': 'Not permitted'}, status=status.HTTP_401_UNAUTHORIZED)

        translation_id = request.query_params.get('id')
        if not translation_id:
            return Response({'status': 'Empty value', 'message': 'Require ID of translation'},
                            status=status.HTTP_400_BAD_REQUEST)

        translation = get_object_or_404(EducationTranslations, id=translation_id)
        translation.delete()
        return Response({'status': 'Success'}, status=status.HTTP_200_OK)