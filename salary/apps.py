from django.apps import AppConfig


class SalaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'salary'

    def ready(self):
        # Import signals after models are loaded
        from . import signals
        from .models import PayGradeComponent
        from django.db.models.signals import pre_save
        
        # Connect signals
        pre_save.connect(signals.validate_positive_amount, sender=PayGradeComponent)
        pre_save.connect(signals.validate_component_type, sender=PayGradeComponent)
