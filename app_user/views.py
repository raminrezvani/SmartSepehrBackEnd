from rest_framework import (status, permissions)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from app_user.models import User


class UserLoginAPI(APIView):
    def post(self, request):
        # --- check request body
        try:
            username = request.data['username']
            password = request.data['password']
        except:
            return Response(
                {'message': "request body is incorrect"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        # --- queryset for username
        qs_user = User.objects.filter(username=username)
        if not qs_user:
            return Response(
                {'message': "کاربری با این نام کاربری یافت نشد"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = qs_user.last()
        # --- check password
        if not user.check_password(password):
            return Response(
                {'message': "کلمه عبور اشتباه است"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # ---
        refresh = RefreshToken.for_user(user)
        return Response(
            {'access': str(refresh.access_token), "refresh": str(refresh)},
            status=status.HTTP_200_OK
        )


class CheckUserSearchPermissionAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_permission = user.can_search()
        if user_permission:
            user.plan_usage -= 1
            user.save()
        return Response(
            {'can_search': user_permission},
            status=status.HTTP_200_OK if user_permission else status.HTTP_406_NOT_ACCEPTABLE
        )
