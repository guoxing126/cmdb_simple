from django.apps import AppConfig


class SmartAdminConfig(AppConfig):
    name = 'smart_admin'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('smart_admin')