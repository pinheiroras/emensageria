from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.db import models
from django.forms import Select, Textarea
from django_currentuser.db.models import CurrentUserField
from rest_framework.serializers import ModelSerializer

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class BaseModelSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'created_by',
                            'updated_at', 'updated_by',)


class MultiFieldSortableChangeList(ChangeList):
    def get_ordering(self, request, queryset):
        ORDER_VAR = admin.views.main.ORDER_VAR
        params = self.params
        ordering = list(self.model_admin.get_ordering(
            request) or self._get_default_ordering())

        if ORDER_VAR in params:
            ordering = []
            order_params = params[ORDER_VAR].split('.')
            for p in order_params:
                try:
                    none, pfx, idx = p.rpartition('-')
                    field_name = self.list_display[int(idx)]
                    order_fields = self.get_ordering_field(field_name)

                    if type(order_fields) == str:
                        order_fields = [order_fields]

                    for order_field in order_fields:
                        if order_field:
                            ordering.append(pfx + order_field)
                except (IndexError, ValueError):
                    continue

        ordering.extend(queryset.query.order_by)

        pk_name = self.lookup_opts.pk.name
        if not (set(ordering) & set(['pk', '-pk', pk_name, '-' + pk_name])):
            ordering.append('-pk')

        return ordering


class BaseModel(models.Model):
    created_by = CurrentUserField(related_name='%(class)s_created_by')
    updated_by = CurrentUserField(on_update=True, related_name='%(class)s_updated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModelEsocial(models.Model):
    created_by = CurrentUserField(related_name='%(class)s_created_by_esocial')
    updated_by = CurrentUserField(on_update=True, related_name='%(class)s_updated_by_esocial')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModelReinf(models.Model):
    created_by = CurrentUserField(related_name='%(class)s_created_by_reinf')
    updated_by = CurrentUserField(on_update=True, related_name='%(class)s_updated_by_reinf')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditoriaAdmin(admin.ModelAdmin):
    readonly_fields = (
        'created_at',
        'created_by',
        'updated_at',
        'updated_by',
    )


class AuditoriaAdminInline(admin.TabularInline):
    readonly_fields = AuditoriaAdmin.readonly_fields
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={
                'rows': 4,
                'cols': 40
            })
        },
        models.ForeignKey: {
            'widget': Select(attrs={
                'style': 'width:150px'
            })
        },
    }


class AuditoriaAdminStackedInlineInline(admin.StackedInline):
    readonly_fields = AuditoriaAdmin.readonly_fields
