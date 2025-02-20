from django.apps import AppConfig
import sys
from django.core.signals import request_finished
# import gc

# def clean_up_memory(sender, **kwargs):
#     gc.collect()  # Force garbage collection after request


class AppApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_api'

    # def ready(self):
    #     print('Garbage CleanUP...')
    #     request_finished.connect(clean_up_memory)  # Connect signal

