from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets

from app.models import Company
from app.serializers.company_serializer import CompanySerializer


class CompanyAPI(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @action(methods=['get'], detail=False)
    def many_search(self, request):
        queryset = self.get_queryset().order_by("-name")
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        response["status"] = "Success"
        return response

    @action(methods=["post"], detail=False)
    def save(self, request):
        user = request.user
        data = request.data
        company_id = data.get('company_id')
        if user.role not in ['employer', 'admin']:
            return Response({'status': "not permitted", 'message': 'Your authentication not permission'},
                            status=status.HTTP_403_FORBIDDEN)
        if company_id:
            company = get_object_or_404(Company, id=company_id)
            serializer = CompanySerializer(company, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status": "Success", "company": serializer.data}, status=status.HTTP_200_OK)

        serializer = CompanySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "Success", "company": serializer.data}, status=status.HTTP_201_CREATED)
