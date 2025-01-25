from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from app_utils.date_helper import get_current_time
from app_utils.main_model_manager import get_deleted_objects
from .generator import generate_unique_u_id


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


class MainModelAdmin(admin.ModelAdmin):
    actions = None

    def get_deleted_objects(self, objs, request):
        return get_deleted_objects(objs, request, self.admin_site)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(soft_delete=False)

    def detail_content(self, obj):
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        title = _("Detail")
        return format_html(
            f'<a href="{url}" title="{title}" class="text-dark"><i class="fas fa-eye"></i></a>'
        )

    detail_content.allow_tags = True
    detail_content.short_description = _("Detail")


class MainModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(soft_delete=False)

    def all(self):
        return self.get_queryset().filter(soft_delete=False)


class MainModel(models.Model):
    u_id = models.CharField(editable=False, null=True, blank=True, max_length=250)
    soft_delete = models.BooleanField(default=False, editable=False, verbose_name=_("soft delete"))
    created = models.DateTimeField(null=True, blank=True, editable=False, verbose_name=_("created"))
    updated = models.DateTimeField(null=True, blank=True, editable=False, verbose_name=_("updated"))
    deleted = models.DateTimeField(editable=False, null=True, blank=True, verbose_name=_("deleted"))
    # ---
    objects = MainModelManager()

    def __str__(self):
        return self.u_id

    def save(self, *args, **kwargs):
        now_date = get_current_time()
        # --- handle created
        if not self.created:
            self.created = now_date
        # --- handle updated
        self.updated = now_date
        # --- u_id
        if not self.u_id:
            # --- finally
            self.u_id = generate_unique_u_id()
        super(MainModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.soft_delete = True
        self.deleted = get_current_time()
        self.save()
        return True

    class Meta:
        verbose_name = _("Main Model")
        verbose_name_plural = _("Main Model")
        abstract = True
        ordering = ['soft_delete', '-updated']
