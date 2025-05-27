from django.contrib import admin
from .models import TaxTier, PensionConfiguration, StatutoryDeduction

@admin.register(TaxTier)
class TaxTierAdmin(admin.ModelAdmin):
    list_display = ("lower_bound", "upper_bound", "rate", "additional_amount")
    ordering = ("lower_bound",)

@admin.register(PensionConfiguration)
class PensionConfigurationAdmin(admin.ModelAdmin):
    list_display = ("employee_rate", "employer_rate", "effective_date", "is_active")
    list_filter = ("is_active",)
    ordering = ("-effective_date",)
    def has_add_permission(self, request, obj=None):
        return not PensionConfiguration.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(StatutoryDeduction)
class StatutoryDeductionAdmin(admin.ModelAdmin):
    list_display = ("name", "rate", "calculation_base", "is_active", "created_at")
    list_filter = ("is_active",)