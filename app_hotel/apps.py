from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppHotelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_hotel'
    verbose_name = _("Hotel")
