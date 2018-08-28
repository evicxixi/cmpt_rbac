from django.apps import AppConfig


class StarkConfig(AppConfig):
    name = 'stark'

    def readey(self):
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('stark')
