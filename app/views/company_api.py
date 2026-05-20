import json
import cloudinary.uploader
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from app.models import Company
from app.serializers.company_serializer import CompanySerializer


class CompanyAPI(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @action(methods=['get'], detail=False)
    def many_search(self, request):
        name = request.query_params.get('name')
        queryset = self.get_queryset().order_by("-name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        response.data["status"] = "Success"
        return response

    @action(methods=["get"], detail=False)
    def many(self, request):
        queryset = self.get_queryset().order_by("-name")
        return Response({"status": "Success", "company": CompanySerializer(queryset, many=True).data})

    @action(methods=["post"], detail=False, parser_classes=[MultiPartParser, FormParser, JSONParser])
    def save(self, request):
        user = request.user
        if user.role not in ['employer', 'admin']:
            return Response({'status': "Not permitted", 'message': 'Your authentication not permission'},
                            status=status.HTTP_403_FORBIDDEN)

        data_str = request.data.get('data') or request.POST.get('data')
        if not data_str:
            return Response({'status': 'Error', 'message': 'Missing "data" field'}, status=400)

        try:
            data = json.loads(data_str)
        except json.JSONDecodeError:
            return Response({'status': 'Error', 'message': 'Invalid JSON in data field'}, status=400)

        company_id = data.get('id')
        logo_file = request.FILES.get('logo')
        cover_file = request.FILES.get('coverImage')

        if company_id:
            company = get_object_or_404(Company, id=company_id)
            serializer = CompanySerializer(company, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            company = serializer.save()
            status_code = status.HTTP_200_OK
        else:
            serializer = CompanySerializer(data=data)
            serializer.is_valid(raise_exception=True)
            company = serializer.save()
            status_code = status.HTTP_201_CREATED

        updated = False
        if logo_file:
            upload_result = cloudinary.uploader.upload(
                logo_file,
                folder='company_logos',
                public_id=f"company_{company.id}_logo",
                overwrite=True
            )
            company.logo_public_id = upload_result['public_id']
            updated = True
        if cover_file:
            upload_result = cloudinary.uploader.upload(
                cover_file,
                folder='company_covers',
                public_id=f"company_{company.id}_cover",
                overwrite=True
            )
            company.cover_public_id = upload_result['public_id']
            updated = True
        if updated:
            company.save()

        return Response({"status": "Success", "company": CompanySerializer(company).data}, status=status_code)

    @action(methods=["delete"], detail=False)
    def item(self, request):
        user = request.user
        if user.role not in ['employer', 'admin']:
            return Response({'status': "Not permitted", 'message': 'Your authentication not permission'},
                            status=status.HTTP_403_FORBIDDEN)

        company_id = request.query_params.get('id')
        if not company_id:
            return Response({'status': 'Error', 'message': 'Missing "id" field'}, status=400)

        company = get_object_or_404(Company, id=company_id)
        if not company:
            return Response({'status': 'Error', 'message': 'Company not found'}, status=400)

        company.delete()
        return Response({"status": "Success"}, status=200)
