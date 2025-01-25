from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppCompanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_company'
    verbose_name = _("Company")
