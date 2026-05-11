from datetime import datetime
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from app.models import Account, Candidate, Employer, JobSaved
from app.serializers import AccountSerializer, RoleUpdateSerializer, ImageUploadSerializer, JobSavedSerializer
import cloudinary.uploader


class AccountAPI(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=['patch'], detail=False)
    def set_role(self, request):
        user = request.user
        if user.role != 'pending':
            return Response({'status': 'Not permission', 'message': 'Only pending role can be changed'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = RoleUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_role = serializer.validated_data['role']
        user.role = new_role
        user.save()
        return Response({'status': 'Success'}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def info(self, request):
        return Response({'status': 'Success', 'user': AccountSerializer(request.user).data}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, parser_classes=[MultiPartParser, FormParser])
    def upload_image(self, request):
        user = request.user
        if user.role not in ['candidate', 'employer']:
            return Response(
                {'status': 'Invalid role', 'message': 'User not allowed upload image'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data['image']
        try:
            uploaded_image = cloudinary.uploader.upload(
                file=image,
                folder='Media',
                public_id=f'user_{user.id}',
                overwrite=True,
                format='webp'
            )
            image_url = uploaded_image['secure_url']
        except Exception as e:
            return Response({'status': 'Error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if user.role == 'candidate':
            candidate = get_object_or_404(Candidate, id=user.id)
            candidate.image_url = image_url
            candidate.save()
        elif user.role == 'employer':
            employer = get_object_or_404(Employer, id=user.id)
            employer.image_url = image_url
            employer.save()

        return Response({'status': 'Success', 'imageUrl': image_url}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def many_search(self, request):
        user = request.user
        email = request.GET.get('email')
        role = request.GET.get('role')
        status = request.GET.get('status')
        date_created = request.GET.get('dateCreated')
        if user.role != "admin":
            return Response({'status': 'Not permitted', 'message': 'Your authentication not permission'},
                            status=status.HTTP_403_FORBIDDEN)
        queryset = self.queryset.order_by('-date_created')
        if role:
            queryset = queryset.filter(role=role)
        if email:
            queryset = queryset.filter(email=email)
        if status:
            queryset = queryset.filter(status=status)
        if date_created:
            match_date = datetime.strptime(date_created, '%d/%m/%Y').date()
            queryset = queryset.filter(date_created=match_date)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AccountSerializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data["status"] = "Success"
            return response
        serializer = AccountSerializer(queryset, many=True)
        return Response({'status': 'Success', 'accounts': serializer.data}, status=status.HTTP_200_OK)


