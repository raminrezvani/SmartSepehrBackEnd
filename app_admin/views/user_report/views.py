from django.views import View
from app_utils.render import c_render
from datetime import datetime, timedelta
from app_report.models import SearchReport
import jdatetime


class UserReportView(View):
    def __init__(self, *args, **kwargs):
        super(UserReportView, self).__init__(*args, **kwargs)
        self.template_name = "admin/user_report/user_report.html"

    def get(self, request, pk):
        # ---
        days_result = {}
        now_date = datetime.now()
        days = 10
        for day in range(days):
            date = now_date - timedelta(days=day)
            persian_date = jdatetime.datetime.fromtimestamp(date.timestamp()).strftime("%Y-%m-%d")
            # ---
            report_length = len(SearchReport.objects.filter(soft_delete=False, user_id=pk, created=date))
            # ---
            days_result[persian_date] = report_length
        print("--------------------------------------")
        print(days_result)
        # ---
        context = {
            "title": "User Report",
            "days": days_result,
            "last_search": SearchReport.objects.filter(soft_delete=False, user_id=pk)[:15]
        }
        return c_render(request, self.template_name, context, show_error=False)
