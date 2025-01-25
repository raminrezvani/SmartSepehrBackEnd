from django.db import models
from django.utils.translation import gettext_lazy as _


class CookieProvider(models.Model):
    name = models.CharField(max_length=300)
    recaptcha_code = models.CharField(max_length=300, null=True, blank=True)
    company = models.ForeignKey("app_company.Company", on_delete=models.PROTECT, null=True, blank=True,
                                verbose_name=_("company"))
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
