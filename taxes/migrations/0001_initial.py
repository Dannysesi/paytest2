import django.core.validators
from decimal import Decimal
from django.db import migrations, models
from django.utils.timezone import now

def create_default_pension(apps, schema_editor):
    PensionConfiguration = apps.get_model('taxes', 'PensionConfiguration')
    PensionConfiguration.objects.create(
        employee_rate=Decimal("8.00"),
        employer_rate=Decimal("10.00"),
        effective_date=now().date(),
        is_active=True
    )



def create_default_statutory_deductions(apps, schema_editor):
    StatutoryDeduction = apps.get_model('taxes', 'StatutoryDeduction')
    StatutoryDeduction.objects.create(name='NHF', is_active=True)
    StatutoryDeduction.objects.create(name='NSITF', is_active=True)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PensionConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_rate', models.DecimalField(decimal_places=2, default=Decimal('8.00'), help_text='Employee contribution percentage (7-20%)', max_digits=5, validators=[django.core.validators.MinValueValidator(7), django.core.validators.MaxValueValidator(20)])),
                ('employer_rate', models.DecimalField(decimal_places=2, default=Decimal('10.00'), help_text='Employer contribution percentage (7-20%)', max_digits=5, validators=[django.core.validators.MinValueValidator(7), django.core.validators.MaxValueValidator(20)])),
                ('is_active', models.BooleanField(default=True)),
                ('effective_date', models.DateField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Pension (PENCOM) Configuration',
                'verbose_name_plural': 'Pension (PENCOM) Configurations',
            },
        ),
        migrations.RunPython(create_default_pension),


        migrations.CreateModel(
            name='StatutoryDeduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, choices=[
                    ('NHF', 'National Housing Fund (2.5% of basic)'),
                    ('NSITF', 'Employee Compensation (1% of gross)')
                ], unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Statutory Deduction',
                'verbose_name_plural': 'Statutory Deductions',
            },
        ),
        migrations.RunPython(create_default_statutory_deductions),

        migrations.CreateModel(
            name='TaxTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lower_bound', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('upper_bound', models.DecimalField(blank=True, decimal_places=2, help_text='Leave blank for no upper limit', max_digits=12, null=True)),
                ('rate', models.DecimalField(decimal_places=2, help_text='Tax rate percentage', max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('additional_amount', models.DecimalField(decimal_places=2, default=0, help_text='Additional fixed amount for this tier', max_digits=12)),
            ],
            options={
                'verbose_name': 'PAYE Tax Tier',
                'ordering': ['lower_bound'],
            },
        ),
    ]
