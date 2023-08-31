from django.apps import AppConfig

class ReceptionistConfig(AppConfig):
    name = 'receptionist'

    def ready(self):
        import receptionist.models  # This will import models.py and register the signals

