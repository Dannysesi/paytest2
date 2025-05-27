from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Employee, EmployeeSalaryComponent
from .forms import EmployeeForm, EmployeeSalaryComponentFormSet
from django.http import JsonResponse
from django.shortcuts import render
from .models import PayGradeComponent


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 20

    def get_queryset(self):
        return Employee.objects.select_related('company', 'pay_grade').order_by('last_name')

class EmployeeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employees_list')
    success_message = "Employee created successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['components_formset'] = EmployeeSalaryComponentFormSet(
                self.request.POST,
                prefix='components'
            )
        else:
            context['components_formset'] = EmployeeSalaryComponentFormSet(
                prefix='components'
            )
        return context


    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['components_formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payroll_data'] = self.object.calculate_payroll()
        return context

class EmployeeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employees_list')
    success_message = "Employee updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['components_formset'] = EmployeeSalaryComponentFormSet(
                self.request.POST,
                instance=self.object,
                prefix='components',
                queryset=EmployeeSalaryComponent.objects.filter(employee=self.object, is_custom=True)
            )
        else:
            context['components_formset'] = EmployeeSalaryComponentFormSet(
                instance=self.object,
                prefix='components',
                queryset=EmployeeSalaryComponent.objects.filter(employee=self.object, is_custom=True)
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['components_formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employees_list')

def get_paygrade_components(request):
    paygrade_id = request.GET.get('paygrade_id')
    if paygrade_id:
        components = PayGradeComponent.objects.filter(pay_grade_id=paygrade_id)\
            .select_related('component')
        data = [{
            'name': pgc.component.name,
            'amount': str(pgc.amount),
            'type': pgc.component.component_type
        } for pgc in components]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)