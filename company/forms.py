from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'tax_id', 'address', 'is_active']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'tax_id': 'Tax Identification Number'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Company.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("A company with this name already exists.")
        return name