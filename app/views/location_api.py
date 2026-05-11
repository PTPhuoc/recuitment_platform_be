from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from django.db import models

from app.models import Locations, LocationTranslations
from app.serializers.location_serializer import LocationsSerializer, LocationTranslationsSerializer


class LocationAPI(viewsets.ModelViewSet):
    queryset = Locations.objects.all()
    serializer_class = LocationsSerializer

    @action(methods=['get'], detail=False)
    def many(self, request):
        lang = request.query_params.get('lang')
        queryset = self.get_queryset().order_by('slug')
        if lang:
            queryset = queryset.prefetch_related(
                models.Prefetch('translations', queryset=LocationTranslations.objects.filter(language_code=lang))
            )

        serializer = LocationsSerializer(queryset, many=True)
        return Response({'status': "Success", 'locations': serializer.data})

    @action(methods=['get'], detail=False)
    def many_search(self, request):
        lang = request.query_params.get('lang')
        location_type = request.query_params.get('location_type')
        name = request.query_params.get('name')
        slug = request.query_params.get('slug')
        queryset = self.get_queryset().order_by('slug')
        if lang:
            queryset = queryset.prefetch_related(
                models.Prefetch('translations', queryset=LocationTranslations.objects.filter(language_code=lang))
            )
        if name:
            queryset = queryset.prefetch_related(
                models.Prefetch('translations', queryset=LocationTranslations.objects.filter(name=name))
            )
        if slug:
            queryset = queryset.filter(slug=slug)
        if location_type:
            queryset = queryset.filter(type=location_type)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        response.data['status'] = "Success"
        return response

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def save(self, request):
        user = request.user
        if user.role != 'admin':
            return Response({'status': 'Not permitted'}, status=status.HTTP_403_FORBIDDEN)

        lang = request.data.get('lang')
        location_id = request.data.get('id')
        location_type = request.data.get('type')
        name = request.data.get('name')
        slug = request.data.get('slug')

        if not name or not slug or not location_type:
            return Response({'status': "Empty value", 'message': "name, slug, type are required"}, status=400)

        if location_type not in ['country', 'city', 'district']:
            return Response({'status': "Invalid value", 'message': "type must be country, city, or district"},
                            status=400)

        if location_id:
            location = get_object_or_404(Locations, id=location_id)
            location_serializer = LocationsSerializer(location, data=request.data, partial=True)
            location_serializer.is_valid(raise_exception=True)
            location = location_serializer.save()
            create_location = False
        else:
            location = self.get_queryset().filter(slug=slug).first()
            if not location:
                location_serializer = LocationsSerializer(location, data=request.data, partial=True)
                location_serializer.is_valid(raise_exception=True)
                location = location_serializer.save()
                create_location = True
            else:
                create_location = False

        translation, created_trans = LocationTranslations.objects.update_or_create(
            location_id=location,
            language_code=lang,
            defaults={'name': name},
        )
        if create_location or created_trans:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK

        return Response({'status': 'Success', 'location': LocationsSerializer(location).data}, status=status_code)

    @action(methods=['delete'], detail=False)
    def item(self, request):
        user = request.user
        if user.role != "admin":
            return Response({"status": "Not permitter", "message": "Only Admin can delete"},
                            status=status.HTTP_403_FORBIDDEN)

        location_id = request.query_params.get('id')
        if not location_id:
            return Response({"status": "Empty value", "message": "id is required"}, status=400)

        location = get_object_or_404(Locations, id=location_id)
        location.delete()
        return Response({"status": "Success"}, status=status.HTTP_202_ACCEPTED)

    @action(methods=['delete'], detail=False)
    def translate(self, request):
        user = request.user
        if user != "admin":
            return Response({"status": "Not permitter", "message": "Only Admin can delete"},
                            status=status.HTTP_403_FORBIDDEN)
        translation_id = request.query_params.get('id')
        if not translation_id:
            return Response({"status": "Empty value", "message": "id is required"}, status=400)
        translation = get_object_or_404(LocationTranslations, id=translation_id)
        translation.delete()
        return Response({"status": "Success"}, status=status.HTTP_202_ACCEPTED)
