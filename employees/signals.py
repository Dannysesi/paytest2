from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver
from .models import Employee, EmployeeSalaryComponent
from salary.models import PayGrade, PayGradeComponent

# --- TRACK PAY GRADE CHANGES BEFORE AN EMPLOYEE IS SAVED ---
@receiver(pre_save, sender=Employee)
def track_old_pay_grade(sender, instance, **kwargs):
    """
    This captures the employee's current pay grade *before* it is saved,
    so we can detect if the pay grade is being changed in post_save.
    """
    if instance.pk:
        instance._old_pay_grade = sender.objects.get(pk=instance.pk).pay_grade
    else:
        instance._old_pay_grade = None



# --- ASSIGN OR UPDATE EMPLOYEE SALARY COMPONENTS BASED ON PAY GRADE ---
@receiver(post_save, sender=Employee)
def assign_or_update_paygrade_components(sender, instance, created, **kwargs):
    """
    After saving an Employee:
    - If they were just created or their pay grade was changed,
    - Delete all non-custom salary components,
    - Reassign components from the new pay grade.
    """
    new_pg = instance.pay_grade
    old_pg = getattr(instance, '_old_pay_grade', None)

    if new_pg and (created or new_pg != old_pg):

        EmployeeSalaryComponent.objects.filter(employee=instance, is_custom=False).delete()

        for pgc in PayGradeComponent.objects.filter(pay_grade=new_pg):
            EmployeeSalaryComponent.objects.create(
                employee=instance,
                component=pgc.component,
                amount=pgc.amount,
                is_custom=False
            )


# --- WHEN A PAY GRADE IS DELETED ENTIRELY ---
@receiver([post_save, post_delete], sender=PayGradeComponent)
def update_employees_on_paygrade_change(sender, instance, **kwargs):
    """
    Whenever a PayGradeComponent is added changed, or deleted:
    - Update the salary components of all employees with that pay grade.
    - Rebuild their salary from the current state of the pay grade.
    """
    pay_grade = instance.pay_grade
    components = PayGradeComponent.objects.filter(pay_grade=pay_grade)
    employees = Employee.objects.filter(pay_grade=pay_grade)

    for emp in employees:
        # Remove old (non-custom) components
        EmployeeSalaryComponent.objects.filter(employee=emp, is_custom=False).delete()

        # Recreate from updated PayGrade
        for comp in components:
            EmployeeSalaryComponent.objects.create(
                employee=emp,
                component=comp.component,
                amount=comp.amount,
                is_custom=False
            )


@receiver(pre_delete, sender=PayGrade)
def reset_employees_on_paygrade_delete(sender, instance, **kwargs):
    """
    When a PayGrade is deleted:
    - Detach it from any employee that had it.
    - Delete all their non-custom salary components.
    """
    employees = Employee.objects.filter(pay_grade=instance)
    for emp in employees:
        emp.pay_grade = None
        emp.save(update_fields=["pay_grade"])
        EmployeeSalaryComponent.objects.filter(employee=emp, is_custom=False).delete()
