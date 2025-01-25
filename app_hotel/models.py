from app_utils.main_model import MainModel, models
from django.utils.translation import gettext_lazy as _


class Hotel(MainModel):
    name = models.CharField(max_length=300, verbose_name=_("name"))
    city_code = models.CharField(max_length=300, verbose_name=_("city code"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Hotel")
        verbose_name_plural = _("Hotels")
