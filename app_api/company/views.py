from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import (status, )
from app_company.models import Company


class CompanyListAPI(APIView):
    def get(self, request):
        result = Company.objects.filter(soft_delete=False).values("u_id", "name")
        # ---
        return Response(
            result,
            status=status.HTTP_200_OK
        )
