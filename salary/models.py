from django.db import models
from core.models import TimeStampedModel
from core.utils import validate_positive_amount

class SalaryComponent(TimeStampedModel):
    EARNING = 'E'
    DEDUCTION = 'D'
    TYPE_CHOICES = [
        (EARNING, 'Earning'),
        (DEDUCTION, 'Deduction'),
    ]
    name = models.CharField(max_length=50, unique=True)
    component_type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    is_taxable = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_component_type_display()})"

class PayGrade(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

class PayGradeComponent(models.Model):
    pay_grade = models.ForeignKey(PayGrade, on_delete=models.CASCADE)
    component = models.ForeignKey(SalaryComponent, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[validate_positive_amount]
    )
    class Meta:
        unique_together = ('pay_grade', 'component') 
