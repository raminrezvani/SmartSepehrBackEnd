from django.urls import path
from app_api.ready_tour.views import (GetCookieDataApi, UpdateCookieDataApi, GetSingleDataApi, GetAnalyticsDataApi, GetHotelsDataApi, )
from app_api.flight.views import FlightApi
from app_api.build_tour.views import BuildTourApi, BuildTourAnalysisApi
# from app_api.build_tour.views import BuildTourApi
from app_api.hotel.views import HotelApi
from app_api.cookie.views import SepehrCookieAPI, SepehrCookieProviderAPI
from app_api.calendar.views import CalendarApi
from app_api.company.views import CompanyListAPI

app_name = "Api"
urlpatterns = [
    # -------------- common
    path("get-cookie/", GetCookieDataApi.as_view()),
    path("update-cookie/", UpdateCookieDataApi.as_view()),
    path("get-data/", GetSingleDataApi.as_view()),
    # -------------- ready tour
    path("get-hotels/", GetHotelsDataApi.as_view()),
    path("get-analysis/", GetAnalyticsDataApi.as_view()),
    # -------------- flight
    path('get-flight/', FlightApi.as_view()),
    # -------------- build tour
    path('build-tour/', BuildTourApi.as_view()),
    path('build-tour-analyse/', BuildTourAnalysisApi.as_view()),

    # -------------- hotel
    path('get-hotel/', HotelApi.as_view()),
    # -------------- calendar
    path('get-calendar/', CalendarApi.as_view()),
    # -------------- company
    path('get-company-list/', CompanyListAPI.as_view()),
    # -------------- cookie
    path('cookie-providers/', SepehrCookieProviderAPI.as_view()),
    path('set-cookie/', SepehrCookieAPI.as_view()),
]
