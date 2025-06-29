# Generated by Django 5.2.1 on 2025-05-27 14:01

import core.utils
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PayGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SalaryComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('component_type', models.CharField(choices=[('E', 'Earning'), ('D', 'Deduction')], max_length=1)),
                ('is_taxable', models.BooleanField(default=False)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PayGradeComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[core.utils.validate_positive_amount])),
                ('pay_grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salary.paygrade')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salary.salarycomponent')),
            ],
            options={
                'unique_together': {('pay_grade', 'component')},
            },
        ),
    ]
