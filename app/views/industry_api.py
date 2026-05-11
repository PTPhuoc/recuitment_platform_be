from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from django.db import models

from app.models import Industry, IndustryTranslations
from app.serializers.industry_serializer import IndustrySerializer, IndustryTranslationSerializer


class IndustryAPI(viewsets.ModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

    @action(methods=['get'], detail=False)
    def many_search(self, request):
        lang = request.query_params.get('lang')
        name = request.query_params.get('name')
        slug = request.query_params.get('slug')
        queryset = self.get_queryset().order_by('slug')
        if lang:
            queryset = queryset.prefetch_related(
                models.Prefetch("translations", queryset=IndustryTranslations.objects.filter(language_code=lang))
            )
        if name:
            queryset = queryset.prefetch_related(
                models.Prefetch("translations", queryset=IndustryTranslations.objects.filter(name=name))
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
                models.Prefetch('translations', queryset=IndustryTranslations.objects.filter(language_code=lang))
            )
        serializer = IndustrySerializer(queryset, many=True)
        return Response({'status': "Success", "industry": serializer.data})

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def save(self, request):
        user = request.user
        if user.role != 'admin':
            return Response({'status': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        industry_id = data.get('id')
        slug = data.get('slug')
        lang = data.get('lang')
        name = data.get('name')
        if not lang or not name:
            return Response({'status': 'Empty value', 'message': 'lang and name are required'}, status=400)

        if industry_id:
            industry = get_object_or_404(Industry, id=industry_id)
            industry_serializer = IndustrySerializer(industry, data=data, partial=True)
            industry_serializer.is_valid(raise_exception=True)
            industry = industry_serializer.save()
            created_industry = False
        elif slug:
            industry = Industry.objects.filter(slug=slug).first()
            if not industry:
                industry_serializer = IndustrySerializer(data=data)
                industry_serializer.is_valid(raise_exception=True)
                industry = industry_serializer.save()
                created_industry = True
            else:
                created_industry = False
        else:
            industry_serializer = IndustrySerializer(data=data)
            industry_serializer.is_valid(raise_exception=True)
            industry = industry_serializer.save()
            created_industry = True

        translation, created_trans = IndustryTranslations.objects.update_or_create(
            industry_id=industry,
            language_code=lang,
            defaults={'name': name}
        )

        if created_industry or created_trans:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK

        return Response({'status': 'Success'}, status=status_code)

    @action(methods=['delete'], detail=False, permission_classes=[IsAuthenticated])
    def slug(self, request):
        user = request.user
        if user.role != 'admin':
            return Response({'status': 'Not permitted'}, status=status.HTTP_401_UNAUTHORIZED)

        industry_id = request.query_params.get('id')
        if not industry_id:
            return Response({'status': 'Empty value', 'message': 'Require ID of industry'},
                            status=status.HTTP_400_BAD_REQUEST)

        industry = get_object_or_404(Industry, id=industry_id)
        industry.delete()
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

        translation = get_object_or_404(IndustryTranslations, id=translation_id)
        translation.delete()
        return Response({'status': 'Success'}, status=status.HTTP_200_OK)
