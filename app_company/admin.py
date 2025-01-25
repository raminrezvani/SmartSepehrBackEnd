from app_utils.main_model import MainModelAdmin, admin, custom_titled_filter
from app_company.models import Company, CompanyAccountSign, Provider
from django.utils.translation import gettext_lazy as _


@admin.register(Provider)
class ProviderAdmin(MainModelAdmin):
    list_display = ("name", "code", "link", "detail_content")
    search_fields = ("name", "code", "link")


@admin.register(Company)
class CompanyAdmin(MainModelAdmin):
    list_display = ("name", "owner_name", "address", "detail_content")
    search_fields = ("name", "address", "phone_number")

    @admin.display(description=_("owner"))
    def owner_name(self, obj):
        return obj.owner.get_full_name()


@admin.register(CompanyAccountSign)
class CompanyAccountSignAdmin(MainModelAdmin):
    list_display = ("company", "provider", "detail_content")
    list_filter = (
        ('company__name', custom_titled_filter(_("company"))),
        ('provider__name', custom_titled_filter(_("provider")))
    )
