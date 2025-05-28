from django.contrib import admin
from .models import Employee, EmployeeSalaryComponent


class EmployeeSalaryComponentInline(admin.TabularInline):
    model = EmployeeSalaryComponent
    extra = 1
    fields = ('component', 'amount', 'is_custom')
    readonly_fields = ('is_custom',)
    
    def get_queryset(self, request):
        return super().get_queryset(request)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'job_title', 'pay_grade', 'is_active', 'get_gross_salary')
    list_select_related = ('pay_grade', 'company')
    list_filter = ('pay_grade', 'is_active', 'company')
    search_fields = ('first_name', 'last_name', 'email', 'job_title')
    inlines = (EmployeeSalaryComponentInline,)
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Full Name"

    @admin.display(description="Gross Salary")
    def get_gross_salary(self, obj):
        return obj.calculate_payroll().get('gross_salary', 'N/A')

@admin.register(EmployeeSalaryComponent)
class EmployeeSalaryComponentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'component', 'amount', 'is_custom')
    list_filter = ('is_custom', 'component__component_type')
    raw_id_fields = ('employee', 'component')

