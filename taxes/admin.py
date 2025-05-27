from django.contrib import admin
from .models import TaxTier, PensionConfiguration

# Register your models here.
@admin.register(TaxTier)
class TaxTierAdmin(admin.ModelAdmin):
    list_display = ('lower_bound', 'upper_bound', 'rate', 'additional_amount')
    search_fields = ('lower_bound', 'upper_bound', 'rate')
    list_filter = ('rate',)
    ordering = ('lower_bound',)

@admin.register(PensionConfiguration)
class PensionConfigurationAdmin(admin.ModelAdmin):
    list_display = ('employee_rate', 'employer_rate', 'is_active', 'effective_date')
    search_fields = ('employee_rate', 'employer_rate')
    list_filter = ('is_active',)
    ordering = ('-effective_date',)

    def has_add_permission(self, request, obj=None):
        # Prevent adding new configurations, only allow editing the existing one
        return not PensionConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the configuration
        return False