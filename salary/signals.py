from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import PayGradeComponent

def validate_positive_amount(sender, instance, **kwargs):  # Add **kwargs
    if instance.amount <= 0:
        raise ValidationError("Amount must be positive.")

@receiver(pre_save, sender=PayGradeComponent)
def validate_component_type(sender, instance, **kwargs):  # Add **kwargs
    if instance.component.component_type == 'D' and instance.amount > 0:
        raise ValidationError("Deductions must be negative.")