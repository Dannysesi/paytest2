from django.contrib import admin
from .models import SalaryComponent, PayGrade, PayGradeComponent

class PayGradeComponentInline(admin.TabularInline):
    model = PayGradeComponent
    extra = 1
    fields = ('component', 'amount')
    raw_id_fields = ('component',)

@admin.register(SalaryComponent)
class SalaryComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'component_type', 'is_taxable')
    list_filter = ('component_type', 'is_taxable')
    search_fields = ('name',)

@admin.register(PayGrade)
class PayGradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'component_count', 'is_active')
    inlines = (PayGradeComponentInline,)
    
    def component_count(self, obj):
        return obj.paygradecomponent_set.count()
    component_count.short_description = "Components"

# Optional: Direct access to components if needed
@admin.register(PayGradeComponent)
class PayGradeComponentAdmin(admin.ModelAdmin):
    list_display = ('pay_grade', 'component', 'amount')
    list_filter = ('pay_grade', 'component__component_type')
    raw_id_fields = ('pay_grade', 'component')