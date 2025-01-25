import json
from rest_framework import (status, permissions)
from rest_framework.response import Response
from rest_framework.views import APIView
from app_crawl.hotel.main import Hotel
from app_utils.validation import check_full_body
from app_report.manager import add_search_report


class HotelApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # --- body
        fields = [
            {"key": "start_date", "required": True, "format": "date"},
            {"key": "end_date", "required": True, "format": "date"},
            {"key": "source", "required": True, "format": "text"},
            {"key": "target", "required": True, "format": "text"},
            {"key": "adults", "required": True, "format": "int"},
        ]
        check_body = check_full_body(fields, request.data)
        if not check_body['status']:
            return Response(
                check_body,
                status=check_body['response_status']
            )
        # ---
        source = request.data['source']
        target = request.data['target']
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        adults = request.data['adults']
        # ---
        hotel = Hotel(source=source, target=target, start_date=start_date, end_date=end_date, adults=adults)
        result = hotel.get_result()
        # ---
        report_data = {
            "user_id": request.user.id,
            "search_type": 3,
            "source": source,
            "target": target,
            "start_date": start_date,
            "end_date": end_date,
            "night_count": 3,
            "use_cache": False,
            "is_analyse": True,
            "result": json.dumps(result)
        }
        add_search_report.after_response(report_data)
        # ---
        return Response(
            result,
            status=status.HTTP_200_OK
        )
