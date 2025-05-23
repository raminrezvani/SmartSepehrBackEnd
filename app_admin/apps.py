from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_admin'
    verbose_name = _("Admin")
