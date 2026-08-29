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
        name = request.query_params.get('name')
        industry = request.query_params.get("industry")
        location = request.query_params.get('location')
        job_status = request.query_params.get('status')
        form_of_work = request.query_params.getlist('form_of_work')
        educations = request.query_params.getlist('educations')
        experience = request.query_params.get('experience')
        queryset = self.get_queryset().order_by('-date_created')
        filters = Q()
        if name:
            filters |= Q(name__icontains=name)
        if industry:
            filters |= Q(require__industries__id=industry)
        if location:
            filters |= Q(require__location__id=location)
        if experience:
            try:
                exp_val = int(experience)
            except ValueError:
                return Response(
                    {'status': 'Error', 'message': 'Experience must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            filters &= Q(require__min_experience__lte=exp_val) & (
                    Q(require__max_experience=0) | Q(require__max_experience__gte=exp_val))
        if len(educations) > 0:
            filters &= Q(require__educations__id__in=educations)
        if len(form_of_work) > 0:
            filters &= Q(require__form_of_work__id__in=form_of_work)
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

    @action(methods=["get"], detail=False)
    def latest(self, request):
        limit = request.query_params.get('limit', 3)
        try:
            limit = int(limit)
        except ValueError:
            limit = 3
        limit = min(max(limit, 1), 10)
        queryset = self.get_queryset().order_by('-date_created')[:limit]
        serializer = JobSerializer(queryset, many=True)
        return Response({"status": "Success", "jobs": serializer.data}, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def items_company(self, request):
        company_id = request.query_params.get('id')
        if not company_id:
            return Response(
                {'status': 'Error', 'message': 'Company ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        queryset = self.get_queryset().filter(company=company_id).order_by("-date_created")
        serializer = JobSerializer(queryset, many=True)
        return Response(
            {"status": "Success", "jobs": serializer.data},
            status=status.HTTP_200_OK
        )

    @action(methods=["get"], detail=False)
    def item_detail(self, request):
        job_id = request.query_params.get('id')
        if not job_id:
            return Response({'status': 'Empty Value', 'message': 'Require ID of job'}, )
        job = get_object_or_404(Job, id=job_id)
        serializer = JobSerializer(job)
        return Response({'status': 'Success', 'job': serializer.data}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def save(self, request):
        user = request.user
        if user.role not in ["admin", "employer"]:
            return Response({'status': 'Not permitted', 'message': 'Your authentication not permission'},
                            status=status.HTTP_403_FORBIDDEN)

        data = request.data

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
            return Response({'status': 'Empty Value', 'message': 'Require ID of job'}, )
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
