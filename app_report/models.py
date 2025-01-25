from app_utils.main_model import MainModel, models
from django.utils.translation import gettext_lazy as _


class SearchReport(MainModel):


    _SOURCE_TYPE = (
        (1, _("air")),
        # ---
        (3, _("hotel")),
        # ---
        (4, _("ready tour")),
        # ---
        (5, _("build tour"))
    )
    # ---
    # nn=models.CharField(max_length=10,default='ramin')

    user = models.ForeignKey("app_user.User", on_delete=models.PROTECT, verbose_name=_("user"))
    search_type = models.IntegerField(verbose_name=_("search type"), choices=_SOURCE_TYPE)
    source = models.CharField(max_length=300, verbose_name=_("source"))
    target = models.CharField(max_length=300, verbose_name=_("target"))
    start_date = models.DateField(verbose_name=_("start date"))
    end_date = models.DateField(verbose_name=_("end date"))
    night_count = models.IntegerField(verbose_name=_("night count"))
    use_cache = models.BooleanField(verbose_name=_("use cache"))
    is_analyse = models.BooleanField(default=False, verbose_name=_("is analyse"))
    result = models.TextField(null=True, blank=True, verbose_name=_("result"), editable=False)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = _("Search Report")
        verbose_name_plural = _("Search Report")
