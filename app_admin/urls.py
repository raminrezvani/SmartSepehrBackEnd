from django.urls import path
from app_admin.views.user_report import views as user_report_views

app_name = "Admin"
urlpatterns = [
    path('admin/app_user/user/<int:pk>/report/', user_report_views.UserReportView.as_view(), name="user_report"),
]
