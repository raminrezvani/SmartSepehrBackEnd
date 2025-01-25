from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("app_api.urls", namespace="Api")),
    path('', include("app_user.urls", namespace="User")),
    path('', include("app_admin.urls", namespace="Admin")),
    path('admin/', admin.site.urls),
]
