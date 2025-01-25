import json
from rest_framework import (status, permissions)
from rest_framework.response import Response
from rest_framework.views import APIView
from app_crawl.kih.get_cookie_data import get_all_cookie
from app_crawl.kih.main import TourCollector as TourCollectorKIH, hotels
from app_crawl.gsm.main import TourCollector as TourCollectorGSM
from app_crawl.cookie.cookie_data import (DAYAN, SEPID_PARVAZ, MEHRAB, TAK_SETAREH, BOOKING, RAHBAL, )
from app_report.manager import add_search_report
from datetime import datetime, timedelta

from app_utils.validation import check_full_body


class GetCookieDataApi(APIView):
    def get(self, request):
        return Response(
            {
                "dayan": DAYAN,
                "sepid_parvaz": SEPID_PARVAZ,
                "mehrab": MEHRAB,
                "tak_setareh": TAK_SETAREH,
                "rahbal": RAHBAL,
                "booking": BOOKING
            },
            status=status.HTTP_200_OK
        )


class UpdateCookieDataApi(APIView):
    def get(self, get):
        get_all_cookie.after_response()
        return Response(
            {"message": "ok"},
            status=status.HTTP_200_OK
        )


class GetSingleDataApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        # # --- check plan
        # can_search = user.can_search()
        # if not can_search:
        #     return Response(
        #         {'message': "متاسفانه پلن شما به اتمام رسیده است."},
        #         status=status.HTTP_403_FORBIDDEN
        #     )


        # --- body
        fields = [
            {"key": "source", "required": True, "format": "text"},
            {"key": "target", "required": True, "format": "text"},
            {"key": "start_date", "required": True, "format": "date"},
            {"key": "night_count", "required": True, "format": "int"},
            {"key": "hotel_star", "required": False, "format": "int"},
            {"key": "adults", "required": False, "format": "int"},
            {"key": "use_cache", "required": False, "format": "bool"},

        ]
        check_body = check_full_body(fields, request.data)
        if not check_body['status']:
            return Response(
                check_body,
                status=check_body['response_status']
            )
        # ---
        target = request.data.get('target', None)
        source = request.data.get('source', None)
        start_date = request.data.get('start_date', None)
        night_count = request.data.get("night_count", None)
        hotel_star = request.data.get('hotel_star', None)
        use_cache = request.data.get('use_cache', True)
        adults = int(request.data.get('adults', 2))
        # --- check body
        if not target or not start_date or not night_count or not hotel_star:
            return Response(
                {'message': "request body is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )
        print("--------------------------------------")
        print(start_date)


        #=====
        tour_collector = TourCollectorKIH(source, target, start_date, night_count, hotel_star, adults=adults)
        result = tour_collector.get_single_result(source, target, show_providers=True, use_cache=use_cache)
        #+===

        # ---
        # if target == "KIH":
        #     tour_collector = TourCollectorKIH(source,target,start_date, night_count, hotel_star, adults=adults)
        #     result = tour_collector.get_single_result(source,target,show_providers=True, use_cache=use_cache)
        # elif target == "GSM":
        #     tour_collector = TourCollectorGSM(start_date, night_count, hotel_star)
        #     result = tour_collector.get_single_result(show_providers=True)
        # else:
        #     return Response(
        #         {"message": "target is invalid"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        # ---
        report_data = {
            "user_id": request.user.id,
            "search_type": 4,
            "source": "MHD",
            "target": target,
            "start_date": start_date,
            "end_date": datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=int(night_count)),
            "night_count": night_count,
            "use_cache": use_cache,
            "is_analyse": False,
            "result": json.dumps(result)
        }
        add_search_report.after_response(report_data)
        user.plan_usage += 1
        user.save()
        # --- response
        return Response(
            {"message": "ok", **result, "adults": adults},
            status=status.HTTP_200_OK
        )


class GetAnalyticsDataApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # --- body
        fields = [
            {"key": "source", "required": True, "format": "text"},
            {"key": "target", "required": True, "format": "text"},
            {"key": "start_date", "required": True, "format": "date"},
            {"key": "night_count", "required": True, "format": "int"},
            {"key": "range_number", "required": False, "format": "int"},
            {"key": "use_cache", "required": False, "format": "bool"},
            {"key": "adults", "required": False, "format": "int"},
        ]
        check_body = check_full_body(fields, request.data)
        if not check_body['status']:
            return Response(
                check_body,
                status=check_body['response_status']
            )
        # ---
        target = request.data.get('target', None)
        source = request.data.get('source', None)

        start_date = request.data.get('start_date', None)
        night_count = request.data.get("night_count", None)
        range_number = request.data.get('range_number', None)
        use_cache = request.data.get('use_cache', True)
        adults = int(request.data.get('adults', 2))
        # --- check body
        if not target or not start_date or not night_count or not range_number:
            return Response(
                {'message': "request body is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # New One
        #======
        #=====
        tour_collector = TourCollectorKIH(source, target, start_date, night_count, 3, adults=adults)
        result = tour_collector.get_analysis(source, target,range_number=range_number, use_cache=use_cache)
        #+===

        # # ---
        # if target == "KIH":
        #     tour_collector = TourCollectorKIH(start_date, night_count, 3, adults=adults)
        #     result = tour_collector.get_analysis(range_number=range_number, use_cache=use_cache)
        # elif target == "GSM":
        #     tour_collector = TourCollectorGSM(start_date, night_count, 3)
        #     result = tour_collector.get_analysis(range_number)
        # else:
        #     return Response(
        #         {"message": "target is invalid"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        # # ---
        report_data = {
            "user_id": request.user.id,
            "search_type": 4,
            "source": "MHD",
            "target": target,
            "start_date": start_date,
            "end_date": datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=int(night_count)),
            "night_count": night_count,
            "use_cache": use_cache,
            "is_analyse": True,
            "result": json.dumps(result)
        }
        add_search_report.after_response(report_data)
        # --- response
        return Response(
            {"message": "ok", "data": result},
            status=status.HTTP_200_OK
        )


class GetHotelsDataApi(APIView):
    def get(self, request):
        return Response(
            list(hotels.keys()),
            status=status.HTTP_200_OK
        )
