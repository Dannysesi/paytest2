from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class TaxTier(models.Model):
    """PAYE Tax Tiers (company-wide)"""
    lower_bound = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    upper_bound = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Leave blank for no upper limit"
    )
    rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Tax rate percentage"
    )
    additional_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Additional fixed amount for this tier"
    )

    class Meta:
        ordering = ['lower_bound']
        verbose_name = "PAYE Tax Tier"

    def __str__(self):
        if self.upper_bound:
            return f"₦{self.lower_bound:,}-₦{self.upper_bound:,} @ {self.rate}% + ₦{self.additional_amount:,}"
        return f"Above ₦{self.lower_bound:,} @ {self.rate}% + ₦{self.additional_amount:,}"



class PensionConfiguration(models.Model):
    """Company-wide pension configuration"""
    employee_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("8.00"),
        validators=[MinValueValidator(7), MaxValueValidator(20)],
        help_text="Employee contribution percentage (7-20%)"
    )
    employer_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("10.00"),
        validators=[MinValueValidator(7), MaxValueValidator(20)],
        help_text="Employer contribution percentage (7-20%)"
    )
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pension (PENCOM) Configuration"
        verbose_name_plural = "Pension (PENCOM) Configurations"

    def __str__(self):
        return f"Pension: {self.employee_rate}% EE / {self.employer_rate}% ER (Effective {self.effective_date})"


class StatutoryDeduction(models.Model):
    """Other statutory deductions (NHF, NSITF)"""
    
    DEDUCTION_TYPES = [
        ('NHF', 'National Housing Fund (2.5% of basic)'),
        ('NSITF', 'Employee Compensation (1% of gross)'),
    ]

    name = models.CharField(
        max_length=10,
        choices=DEDUCTION_TYPES,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Statutory Deduction"
        verbose_name_plural = "Statutory Deductions"

    def __str__(self):
        return self.get_name_display()

    @property
    def rate(self):
        """Returns the fixed rate for each deduction type"""
        rates = {
            'NHF': Decimal('2.5'),    # 2.5% of basic
            'NSITF': Decimal('1.0'),  # 1% of gross
        }
        return rates.get(self.name, Decimal('0'))

    @property
    def calculation_base(self):
        """Returns what salary component this applies to"""
        return 'BASIC' if self.name == 'NHF' else 'GROSS'