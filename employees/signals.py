from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee
from salary.models import PayGradeComponent
from .models import EmployeeSalaryComponent

@receiver(post_save, sender=Employee)
def assign_pay_grade_components(sender, instance, created, **kwargs):
    if instance.pay_grade and created:
        for pgc in instance.pay_grade.paygradecomponent_set.all():
            EmployeeSalaryComponent.objects.create(
                employee=instance,
                component=pgc.component,
                amount=pgc.amount,
                is_custom=False,
            )