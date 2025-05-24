from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Company
from .forms import CompanyForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


def home(request):
    return render(request, 'company/home.html', {
        'title': 'Welcome to the Payroll System',
        'message': 'Manage salaries, pay grades, and payroll with ease!'
    })

def dashboard(request):
    return render(request, 'company/dashboard.html')

class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'company/company_list.html'
    context_object_name = 'companies'
    paginate_by = 10

    def get_queryset(self):
        return Company.objects.order_by('name')

class CompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/company_form.html'
    success_url = reverse_lazy('list')
    success_message = "Company created successfully!"

class CompanyUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/company_form.html'
    success_url = reverse_lazy('list')
    success_message = "Company updated successfully!"

class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'company/company_confirm_delete.html'
    success_url = reverse_lazy('list')

    def get_success_url(self):
        from django.contrib import messages
        messages.success(self.request, "Company deleted successfully!")
        return super().get_success_url()