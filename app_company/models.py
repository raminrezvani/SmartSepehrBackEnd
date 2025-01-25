from app_utils.main_model import MainModel, models
from app_user.models import User
from django.utils.translation import gettext_lazy as _


class Company(MainModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_("owner"))
    name = models.CharField(max_length=300, verbose_name=_("company name"))
    phone_number = models.CharField(max_length=300, verbose_name=_("phone number"))
    address = models.TextField(verbose_name=_("address"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Company")


class Provider(MainModel):
    _PROVIDER_TYPE = (
        (1, _("sepehr")),
        (2, _("booking")),
        (3, _("allwin")),
        (4, _("deltaban"))
    )
    provider_type = models.IntegerField(default=1, choices=_PROVIDER_TYPE, verbose_name=_("provider type"))
    code = models.SlugField(max_length=300, verbose_name=_("unique code"),
                            help_text=_("for change this, please call to the developer first"))
    name = models.CharField(max_length=300, verbose_name=_("name"))
    link = models.URLField(max_length=300, verbose_name=_("link"))

    def get_clear_link(self):
        link = self.link
        link.replace("http://", "")
        link.replace("https://", "")
        return link

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Provider")
        verbose_name_plural = _("Provider")


class CompanyAccountSign(MainModel):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name=_("company"))
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, verbose_name=_("provider"))
    username = models.CharField(max_length=300, verbose_name=_("username"), default="username")
    password = models.CharField(max_length=300, verbose_name=_("password"))

    def __str__(self):
        return self.company.name

    class Meta:
        verbose_name = _("Company Account Sign")
        verbose_name_plural = _("Company Account Sign")
