from django.db import models
from django.core.exceptions import ValidationError

def validate_positive_amount(value):
    if value <= 0:
        raise ValidationError("Amount must be positive.")