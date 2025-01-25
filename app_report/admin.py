from app_utils.main_model import MainModelAdmin, admin
from .models import SearchReport
import jdatetime


@admin.register(SearchReport)
class SearchReportAdmin(MainModelAdmin):
    list_display = ("user", "source", "target", "start_date_persian", "end_date_persian", "search_type", "search_date",
                    "detail_content")
    search_fields = ("start_date", "end_date", "source", "target", "result")
    list_filter = ("user__username", "source", "target", "search_type")
    readonly_fields = (
        "user", "search_type", "source", "target", "start_date", "end_date", "night_count", "use_cache", "created"
    )

    # list_display = ["nn"]
    # search_fields = ["nn"]
    # list_filter =["nn"]
    # readonly_fields = ["nn"]


    fields = readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_analyse=False, soft_delete=False)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(description="start date")
    def start_date_persian(self, obj):
        date = obj.start_date
        return jdatetime.datetime.fromgregorian(year=date.year, month=date.month, day=date.day).strftime("%Y-%m-%d")

    @admin.display(description="end date")
    def end_date_persian(self, obj):
        date = obj.end_date
        return jdatetime.datetime.fromgregorian(year=date.year, month=date.month, day=date.day).strftime("%Y-%m-%d")

    @admin.display(description="search date")
    def search_date(self, obj):
        return jdatetime.datetime.fromtimestamp(obj.created.timestamp()).strftime("%Y-%m-%d %H:%M")
