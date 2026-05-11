from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_403_FORBIDDEN

from mega.client import MegaNzClient
from asgiref.sync import async_to_sync
import cloudinary.api
import os


def get_cloudinary_quota():
    try:
        usage = cloudinary.api.usage()
        storage = usage["storage"]["usage"]
        total_file = usage['resources']
        credit_max = usage['credits']['limit']
        credit_used = usage['credits']['usage']
        bandwidth_used = usage['bandwidth']['usage']
        return {
            "storage": storage / 1024 ** 2 if storage > 0 else 0,
            "bandwidth": bandwidth_used / 1024 ** 2 if bandwidth_used > 0 else 0,
            "credit": {'max': credit_max, 'used': credit_used},
            "total_file": total_file
        }
    except cloudinary.exceptions.Error as e:
        print(str(e))
        raise Exception(str(e))


def get_mega_quota():
    mega_email = os.environ.get("MEGA_EMAIL")
    mega_password = os.environ.get("MEGA_PASSWORD")

    async def _fetch():
        async with MegaNzClient() as mega:
            await mega.login(email=mega_email, password=mega_password)
            state = await mega.get_account_stats()
            total_file = 0
            storage = state.storage.max
            used = state.storage.used
            for metric in state.metrics.values():
                total_file += metric.files
            return {
                "storage": storage / 1024 ** 3 if storage > 0 else 0,
                "usedSpace": used / 1024 ** 3 if used > 0 else 0,
                "totalFile": total_file
            }

    try:
        return async_to_sync(_fetch)()
    except Exception as e:
        print(str(e))
        raise Exception(str(e))


class AdminAPI(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=False)
    def cloud_quota(self, request):
        user = request.user
        if user.role != "admin":
            return Response({'status': 'Not permitted', 'message': 'Your authentication not permission'},
                            status=HTTP_403_FORBIDDEN)
        try:
            cloudinary_quota = get_cloudinary_quota()
            mega_quota = get_mega_quota()
            return Response({'status': "Success", 'cloudQuota': {'cloudinary': cloudinary_quota, 'mega': mega_quota}})
        except APIException as e:
            print(str(e))
            return Response({'status': 'Cloud error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
