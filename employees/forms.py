from django import forms
from .models import Employee, EmployeeSalaryComponent
from company.models import Company
from salary.models import PayGrade

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['email', 'first_name', 'last_name', 'job_title', 'company', 'pay_grade', 'is_active']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'pay_grade': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter pay grades to only active ones
        self.fields['pay_grade'].queryset = PayGrade.objects.filter(is_active=True)

class EmployeeSalaryComponentForm(forms.ModelForm):
    class Meta:
        model = EmployeeSalaryComponent
        fields = ['component', 'amount', 'is_custom']
        widgets = {
            'is_custom': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['component'].queryset = self.fields['component'].queryset.order_by('name')

# Formset for salary components
EmployeeSalaryComponentFormSet = forms.inlineformset_factory(
    Employee,
    EmployeeSalaryComponent,
    form=EmployeeSalaryComponentForm,
    extra=1,
    can_delete=True,
)