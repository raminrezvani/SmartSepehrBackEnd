from django.conf import settings
from django.http import JsonResponse
from django.urls import resolve
from rest_framework import status

from app_utils.lang_helper import is_valid_lang


class LangMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        match = resolve(request.path_info)
        params = request.GET
        # --- validation
        if match.route.startswith('api'):
            if "lang" in params:
                lang = request.GET.get('lang')
                valid_lang = is_valid_lang(lang)
                if not valid_lang:
                    return JsonResponse({
                        "status": False,
                        "data": [],
                        "message": [{'id': 1012, "field": "lang"}],
                        "response_status": status.HTTP_422_UNPROCESSABLE_ENTITY
                    }, status=422)
            # --- default lang
            else:
                request.GET._mutable = True
                request.GET['lang'] = settings.LANGUAGE_CODE
                request.GET._mutable = False
        # ---
        response = self.get_response(request)
        return response
