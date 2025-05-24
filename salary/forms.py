from django import forms
from .models import SalaryComponent, PayGrade, PayGradeComponent
from django.forms import inlineformset_factory

class SalaryComponentForm(forms.ModelForm):
    class Meta:
        model = SalaryComponent
        fields = ['name', 'component_type', 'is_taxable', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'component_type': forms.RadioSelect(choices=SalaryComponent.TYPE_CHOICES),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if SalaryComponent.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A component with this name already exists.")
        return name

class PayGradeForm(forms.ModelForm):
    class Meta:
        model = PayGrade
        fields = ['name', 'is_active']

    

class PayGradeComponentForm(forms.ModelForm):
    class Meta:
        model = PayGradeComponent
        fields = ['component', 'amount']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['component'].queryset = SalaryComponent.objects.all()
        

PayGradeComponentFormSet = inlineformset_factory(
    PayGrade,
    PayGradeComponent,
    form=PayGradeComponentForm,
    extra=1,
    can_delete=True,
    min_num=1,  # At least one component required
    validate_min=True
)