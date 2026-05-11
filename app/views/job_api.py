from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from app.models import Job, JobReq, JobDesc
from app.serializers import JobSerializer, JobReqSerializer, JobDescSerializer, JobSavedSerializer


class JobAPI(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    @action(methods=['get'], detail=False)
    def many_search(self, request):
        queryset = self.get_queryset().order_by('-name')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data["status"] = "Success"
            return response
        serializer = self.get_serializer(queryset, many=True)
        return Response({'status': 'Success', 'job': serializer.data}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def detail(self, request, pk=None):
        job_req = get_object_or_404(JobReq, jobId=pk)
        job_desc = get_list_or_404(JobDesc, jobId=pk)
        req_serializer = JobReqSerializer(job_req, many=False)
        desc_serializer = JobDescSerializer(job_desc, many=True)
        return Response({'status': 'Success', 'require': req_serializer.data, 'description': desc_serializer.data},
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def save(self, request):
        data = request.data
        user = request.user

        if user.role != "admin":
            return Response({'status': 'Not permitted', 'message': 'Your authentication not permission'},
                            status=status.HTTP_403_FORBIDDEN)

        if data.get('id'):
            job = get_object_or_404(Job, id=data.id)
            serializer = JobSerializer(job, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 'Success', 'job': serializer.data}, status=status.HTTP_200_OK)
        else:
            serializer = JobSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 'Success', 'job': serializer.data}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False)
    def require(self, request):
        data = request.data
        user = request.user

        if user.role != "admin":
            return Response({'status': 'Not permitted', 'message': 'Your authentication not permission'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if data.get('id'):
            job_req = get_object_or_404(JobReq, id=data.id)
            serializer = JobReqSerializer(job_req, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 'Success', 'jobReq': serializer.data}, status=status.HTTP_200_OK)

        else:
            serializer = JobReqSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 'Success', 'jobReq': serializer.data}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def desc(self, request):
        data = request.data
        user = request.user
        if user.role != "admin":
            return Response({'status': 'Not permitted', 'message': 'Your authentication not permission'},
                            status=status.HTTP_403_FORBIDDEN)

        if data.get('id'):
            job_desc = get_object_or_404(JobDesc, id=data.id)
            serializer = JobDescSerializer(job_desc, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 'Success', 'jobDesc': serializer.data}, status=status.HTTP_200_OK)
        else:
            serializer = JobDescSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 'Success', 'jobDesc': serializer.data}, status=status.HTTP_200_OK)

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
