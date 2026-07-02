from django.db.migrations import serializer
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from app.models import Job, JobReq, JobDesc, Company
from app.serializers import JobSerializer, JobReqSerializer, JobDescSerializer, JobSavedSerializer
from django.db.models import Q


class JobAPI(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    @action(methods=['get'], detail=False)
    def many_search(self, request):
        page_number = request.query_params.get('page')
        name = request.query_params.get('name')
        company_name = request.query_params.get('company')
        job_status = request.query_params.get('status')
        queryset = self.get_queryset().order_by('-date_created')
        filters = Q()
        if name:
            filters |= Q(name__icontains=name)
        if company_name:
            filters |= Q(company__name__icontains=company_name)
        if job_status:
            filters &= Q(status=job_status)
        if filters:
            queryset = queryset.filter(filters).distinct()

        queryset = queryset.select_related("company")
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        response.data["status"] = "Success"
        return response

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def save(self, request):
        user = request.user
        if user.role not in ["admin", "employer"]:
            return Response({'status': 'Not permitted', 'message': 'Your authentication not permission'},
                            status=status.HTTP_403_FORBIDDEN)

        data = request.data
        company_data = data.get('company')
        if isinstance(company_data, dict):
            data['company'] = company_data.get('id')

        if data.get('id'):
            job = get_object_or_404(Job, id=data.get("id"))
            serializer = JobSerializer(job, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 'Success', 'job': serializer.data}, status=status.HTTP_200_OK)
        else:
            serializer = JobSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 'Success', 'job': serializer.data}, status=status.HTTP_201_CREATED)

    @action(methods=["delete"], detail=False, permission_classes=[IsAuthenticated])
    def item(self, request):
        user = request.user
        if user.role not in ["admin", "employer"]:
            return Response({'status': 'Not permitted', 'message': 'Your authentication not permission'},
                            status=status.HTTP_403_FORBIDDEN)
        job_id = request.query_params.get('id')
        if not job_id:
            return Response({'status': 'Empty Value', 'message': 'Require ID of job'},)
        job = get_object_or_404(Job, id=job_id)
        job.delete()
        return Response({'status': 'Success'}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def follow(self, request):
        data = request.data
        user = request.user
        if user.role != 'candidate':
            return Response({'status': 'Invalid role', 'message': 'Only candidate can saved job'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = JobSavedSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'Success', 'jobSaved': serializer.data}, status=status.HTTP_200_OK)
