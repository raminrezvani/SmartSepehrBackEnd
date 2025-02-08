import json
from rest_framework import (status, permissions)
from rest_framework.response import Response
from rest_framework.views import APIView
from app_crawl.build_tour.main import BuildTour, BuildTourAnalysis
from app_report.manager import add_search_report
from app_utils.validation import check_full_body
import timeout_decorator


class BuildTourApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def correctTime(self,datetimee):
        #------------ Correct times --------------
        year, month, day = datetimee.split('-')
        # Convert month and day to integers and back to strings, adding zero only if needed
        formatted_date = f"{year}-{month.zfill(2) if len(month) == 1 else month}-{day.zfill(2) if len(day) == 1 else day}"
        return formatted_date
        #------------------------
    def post(self, request):
        # --- body
        fields = [
            {"key": "start_date", "required": True, "format": "date"},
            {"key": "end_date", "required": True, "format": "date"},
            {"key": "source", "required": True, "format": "text"},
            {"key": "target", "required": True, "format": "text"},
            {"key": "adults", "required": True, "format": "int"},
            {"key": "use_cache", "required": False, "format": "bool"},
        ]

        request.data['start_date']=self.correctTime(request.data['start_date'])
        request.data['end_date']=self.correctTime(request.data['end_date'])

        check_body = check_full_body(fields, request.data)
        if not check_body['status']:
            return Response(
                check_body,
                status=check_body['response_status']
            )
        # ---
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        source = request.data.get('source')
        target = request.data.get('target')
        adults = request.data.get('adults')
        use_cache = request.data.get('use_cache', True)

        # #=== check target ===
        # if (target=="GSM"):
        #     source="THR"
        # #=========

        # ---
        tour = BuildTour(source=source, target=target, start_date=start_date, end_date=end_date, adults=adults)
        result = tour.get_result(use_cache=use_cache)
        # ---
        report_data = {
            "user_id": request.user.id if request.user.is_authenticated else 1,
            "search_type": 5,
            "source": source,
            "target": target,
            "start_date": start_date,
            "end_date": end_date,
            "night_count": 3,
            "use_cache": use_cache,
            "is_analyse": False,
            "result": json.dumps(result)
        }


        #===== back to MHD for source ===
        report_data['source']="MHD"
        #+===

        add_search_report.after_response(report_data)
        # ---
        return Response(
            result,
            status=status.HTTP_200_OK
        )



class BuildTourAnalysisApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def correctTime(self,datetimee):
        #------------ Correct times --------------
        year, month, day = datetimee.split('-')
        # Convert month and day to integers and back to strings, adding zero only if needed
        formatted_date = f"{year}-{month.zfill(2) if len(month) == 1 else month}-{day.zfill(2) if len(day) == 1 else day}"
        return formatted_date
        #------------------------

    # @timeout_decorator.timeout(300)  # Set timeout to 5 minutes
    def post(self, request):
        # --- body
        fields = [
            {"key": "start_date", "required": True, "format": "date"},
            {"key": "end_date", "required": True, "format": "date"},
            {"key": "source", "required": True, "format": "text"},
            {"key": "target", "required": True, "format": "text"},
            {"key": "adults", "required": True, "format": "int"},
            # {"key": "stay", "required": True, "format": "int"},

            {"key": "use_cache", "required": False, "format": "bool"},
        ]

        request.data['start_date']=self.correctTime(request.data['start_date'])
        request.data['end_date']=self.correctTime(request.data['end_date'])

        check_body = check_full_body(fields, request.data)
        if not check_body['status']:
            return Response(
                check_body,
                status=check_body['response_status']
            )
        # ---
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        source = request.data.get('source', None)
        target = request.data.get('target', None)
        adults = request.data.get('adults', None)
        night_count = request.data.get("night_count", None)
        hotelstarAnalysis = request.data.get("hotelstarAnalysis", [])
        # stay = request.data.get('stay',None)
        range_number=7
        use_cache = request.data.get('use_cache', True)

        #=== check target ===
        if (target=="THR" or target=="MHD"):
            return Response(
                "MHD and THR not allowed!",
                status=status.HTTP_200_OK
            )
        #=========

        # ---
        tourAnalysis = BuildTourAnalysis(start_date=start_date,end_date=end_date,source=source, target=target,night_count=night_count, adults=adults)
        result = tourAnalysis.get_analysis(start_date=start_date,end_date=end_date,range_number=range_number,use_cache=use_cache,hotelstarAnalysis=hotelstarAnalysis)

        # result = tour_collector.get_analysis(source, target,range_number=range_number, use_cache=use_cache)   # ready_tour



        # ---
        report_data = {
            "user_id": request.user.id if request.user.is_authenticated else 1,
            "search_type": 5,
            "source": source,
            "target": target,
            "start_date": start_date,
            "end_date": end_date,
            "night_count": 3,
            "use_cache": use_cache,
            "is_analyse": False,
            "result": json.dumps(result)
        }


        # #===== back to MHD for source ===
        # report_data['source']="MHD"
        # #+===

        add_search_report.after_response(report_data)
        # ---
        return Response(
            result,
            status=status.HTTP_200_OK
        )

