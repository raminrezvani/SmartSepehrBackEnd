from django.urls import path
from app_user.api.authentication import views as auth_views

app_name = "User"
urlpatterns = [
    # ---
    path('api/v1/user/login/', auth_views.LoginUserApi.as_view()),
    path('api/v1/user/profile/', auth_views.UserProfileApi.as_view()),
]
