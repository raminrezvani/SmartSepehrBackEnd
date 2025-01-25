from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from app_utils.date_helper import get_current_time
from app_report.models import SearchReport
import jdatetime

from app_user.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        "username", "full_name", "phone_number", "plan_max", "plan_usage", "remain_plan", "remain_day",
        "last_search", "detail_content")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (_("General"), {"fields": ("phone_number", "email", "password")}),
        (_("Search"), {"fields": ("plan_usage", "plan_max", "plan_expire")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name")}),
        (_("Permission"), {'fields': ("is_active", "is_staff", "is_superuser", "groups")}),
        (_("Important Dates"), {'fields': ("last_login", "date_joined")}),
    )

    actions = None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter()

    def has_delete_permission(self, request, obj=None):
        return False

    def get_fields(self, request, obj=None):
        fields = ("username", "first_name", "last_name", "password")
        # ---
        return fields

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ["last_login", "date_joined", "plan_usage"]
        if not request.user.is_superuser:
            readonly_fields.extend(["is_staff", "is_active", "is_superuser"])
        return readonly_fields

    @admin.display(description="full name")
    def full_name(self, obj):
        return obj.get_full_name()

    @admin.display(description="remain search")
    def remain_plan(self, obj):
        return obj.plan_max - obj.plan_usage

    @admin.display(description="remain day")
    def remain_day(self, obj):
        now_date = get_current_time()
        return timesince(now_date, now=obj.plan_expire)

    @admin.display(description="last search")
    def last_search(self, obj):
        qs = SearchReport.objects.filter(soft_delete=False, user_id=obj.id)
        # if qs:
        if qs.exists():
            qs = qs.last()
            return jdatetime.datetime.fromtimestamp(qs.created.timestamp()).strftime("%Y-%m-%d %H:%M")
        return '-'

    def detail_content(self, obj):
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        url_filter = f"/admin/app_report/searchreport/?user__username={obj.username}&q="
        # ---
        link_detail = f'<a href="{url}" class="text-dark"><i class="fas fa-eye"></i></a>'
        link_filter = f'<a href="{url_filter}" class="text-dark ml-1"><i class="fas fa-chart-pie"></i></a>'
        # ---
        return format_html(
            f"{link_detail} {link_filter}"
        )

    detail_content.allow_tags = True
    detail_content.short_description = _("Detail")
