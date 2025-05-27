from django.db import models
from core.models import TimeStampedModel
from core.utils import validate_positive_amount
from django.conf import settings
from salary.models import PayGradeComponent
from decimal import Decimal


class Employee(TimeStampedModel):
    email = models.EmailField(unique=True)
    job_title = models.CharField(max_length=100)
    # hire_date = models.DateField()
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    pay_grade = models.ForeignKey(
        'salary.PayGrade',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    def get_salary_breakdown(self):
        components = []

        # Use only EmployeeSalaryComponent, regardless of pay grade
        salary_components = EmployeeSalaryComponent.objects.filter(
            employee=self
        )
        for comp in salary_components:
            components.append({
                'name': comp.component.name,
                'amount': comp.amount,
                'type': comp.component.component_type,
            })

        return components

    def calculate_dummy(self):
        from decimal import Decimal
        from django.db.models import Sum, Q

        # Single query to get all components with their types
        components = EmployeeSalaryComponent.objects.filter(
            employee=self
        ).select_related('component').values(
            'component__name',
            'component__component_type',
            'amount'
        )

        earnings = []
        deductions = []
        gross = Decimal('0.00')

        for comp in components:
            amount = Decimal(comp['amount'])
            entry = {
                'name': comp['component__name'],
                'amount': amount,
                'type': comp['component__component_type']
            }

            if comp['component__component_type'] == 'E':
                earnings.append(entry)
                gross += amount
            else:
                deductions.append(entry)

        return {
            "earnings": earnings,
            "deductions": deductions,
            "gross_salary": gross,
        }

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class EmployeeSalaryComponent(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    component = models.ForeignKey('salary.SalaryComponent', on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[validate_positive_amount]
    )
    is_custom = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employee', 'component')

    def __str__(self):
        return f"{self.employee.first_name}'s {self.component.name}: ₦{self.amount}"


class StatutoryDeduction(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # e.g. 0.08 for 8% (like pension)
    rate = models.DecimalField(max_digits=5, decimal_places=4)

    # What is this applied on? Gross salary or taxable income?
    BASE_CHOICES = [
        ('gross', 'Gross Salary'),
        ('taxable', 'Taxable Income'),
    ]
    base = models.CharField(max_length=10, choices=BASE_CHOICES)

    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
