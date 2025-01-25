from rest_framework import (status, permissions)
from rest_framework.response import Response
from rest_framework.views import APIView
from app_crawl.calendar.main import CalendarData
from app_utils.validation import check_full_body


class CalendarApi(APIView):
    permission_classes = [permissions.AllowAny]


    def post(self, request):
        # --- body
        fields = [
            {"key": "source", "required": True, "format": "text"},
            {"key": "target", "required": True, "format": "text"},
            {"key": "skip_month", "required": True, "format": "int"},
        ]
        check_body = check_full_body(fields, request.data)
        if not check_body['status']:
            return Response(
                check_body,
                status=check_body['response_status']
            )
        # ----


        source = request.data.get('source', "MHD")
        target = request.data.get('target', "KIH")
        skip_month = request.data.get("skip_month", 0)

        # #======= Check Target ===
        # if (target=="GSM"):
        #     source="THR"
        # #==============

        #
        # ---
        result = CalendarData(source=source, target=target, skip_month=skip_month)
        # ---
        return Response(
            result.get_result(),
            status=status.HTTP_200_OK
        )
