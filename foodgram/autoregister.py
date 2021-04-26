from importlib import import_module

from django.contrib import admin
from django.apps import apps


class ListAdminMixin:
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        self.empty_value_display = '-пусто-'
        super(ListAdminMixin, self).__init__(model, admin_site)


def autoregister(*app_list):
    for app_name in app_list:
        admin_module = import_module(f'{app_name}.admin')
        app_config = apps.get_app_config(app_name)
        for model in app_config.get_models():
            model_admin = getattr(
                admin_module, f'{model.__name__}Admin', admin.ModelAdmin
            )
            admin_class = type(
                f'{model.__name__}admin', (ListAdminMixin, model_admin), {}
            )
            try:
                admin.site.register(model, admin_class)
            except admin.sites.AlreadyRegistered:
                pass
