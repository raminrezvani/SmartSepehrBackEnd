import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    national_code = models.CharField(max_length=30, verbose_name=_("national code"))
    phone_number = models.CharField(max_length=300, verbose_name=_("phone number"), null=True, blank=True)
    plan_usage = models.IntegerField(default=0, verbose_name=_("plan usage"))
    plan_max = models.IntegerField(default=0, verbose_name=_("plan max"))
    plan_expire = models.DateTimeField(null=True, blank=True, verbose_name=_("plan expire"))

    def is_expired_plan(self):
        # now_datetime = datetime.datetime.now()
        # return self.plan_expire < now_datetime
        return True

    def can_search(self) -> bool:
        """
        check if user can search or not
        :return: True => user can search
        """
        if self.plan_usage < self.plan_max:
           return True
        return False
