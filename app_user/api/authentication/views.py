from rest_framework import (status, permissions)
from rest_framework.response import Response
from rest_framework.views import APIView

from app_user.api.authentication.manager import (login_user, get_user_profile)


class LoginUserApi(APIView):
    def post(self, request):
        # --- check authenticated
        if request.user.is_authenticated:
            return Response(
                {"status": False, "message": [{'id': 1006}]},
                status=status.HTTP_403_FORBIDDEN
            )
        # ---
        login = login_user(data=request.data)
        # ---
        return Response(
            login,
            status=login['response_status']
        )


class UserProfileApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # ---
        profile = get_user_profile(user_id=request.user.id)
        # ---
        return Response(
            profile,
            status=profile['response_status']
        )
