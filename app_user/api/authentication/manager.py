from django.db.models import Q
from rest_framework import status as rest_status
from rest_framework_simplejwt.tokens import RefreshToken

from app_utils.validation import check_full_body
from app_user.models import User


# ---------------------------------------------------------------------------- LOGIN
def login_user(data) -> dict:
    """
   login user
    :param data: request data
    :return: status, message, response_status, data
    """
    # --- check body
    check_body_keys = [
        {"key": "username", "required": True, "format": "text"},
        {"key": "password", "required": True, "format": "text"},
    ]
    check_body = check_full_body(check_body_keys, data)
    if not check_body['status']:
        return check_body
    # ---
    username = data['username']
    password = data['password']
    # ---
    user_lookup = (
        Q(username=username)
    )
    qs_user = User.objects.filter(user_lookup)
    if not qs_user:
        return {
            "status": False,
            "data": None,
            "message": "کاربری با این کلمه عبور یافت نشد",
            "response_status": rest_status.HTTP_400_BAD_REQUEST
        }
    user = qs_user.last()
    # ---
    if not user.check_password(password):
        return {
            "status": False,
            "data": None,
            "message": "کلمه عبور اشتباه است",
            "response_status": rest_status.HTTP_400_BAD_REQUEST
        }
    # ---
    refresh = RefreshToken.for_user(user)
    result = {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "first_name": user.first_name,
        "last_name": user.last_name
    }
    # ---
    return {
        "status": True,
        "data": result,
        "message": "با موفقیت وارد شدید",
        "response_status": rest_status.HTTP_200_OK
    }


# ---------------------------------------------------------------------------- PROFILE
def get_user_profile(user_id):
    """
    get user profile
    :param user_id: int
    :return: status, message, data, response_status
    """
    user = User.objects.filter(id=user_id)
    if not user:
        return {
            "status": False,
            "data": None,
            "message": "کاربری با این اطلاعات یافت نشد",
            "response_status": rest_status.HTTP_400_BAD_REQUEST
        }
    # ---
    user = user.last()
    # ---
    result = {
        "phone_number": user.phone_number,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "national_code": user.national_code,
        "plan_usage": user.plan_usage,
        "plan_max": user.plan_max,
        "plan_expire": user.plan_expire,
        "can_search": user.can_search(),
        "expired_plan": user.is_expired_plan()
    }
    # ---
    return {
        "status": True,
        "data": result,
        "message": "ok",
        "response_status": rest_status.HTTP_200_OK
    }
