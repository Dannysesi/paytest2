from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import SalaryComponent, PayGrade, PayGradeComponent
from .forms import SalaryComponentForm, PayGradeForm
from .forms import PayGradeComponentFormSet


# Salary Component Views
class SalaryComponentListView(LoginRequiredMixin, ListView):
    model = SalaryComponent
    template_name = 'salary/component_list.html'
    context_object_name = 'components'
    paginate_by = 10

    def get_queryset(self):
        return SalaryComponent.objects.order_by('name')

class SalaryComponentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SalaryComponent
    form_class = SalaryComponentForm
    template_name = 'salary/component_form.html'
    success_url = reverse_lazy('component_list')
    success_message = "Salary component created successfully!"

class SalaryComponentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SalaryComponent
    form_class = SalaryComponentForm
    template_name = 'salary/component_form.html'
    success_url = reverse_lazy('component_list')
    success_message = "Salary component updated successfully!"

class SalaryComponentDeleteView(LoginRequiredMixin, DeleteView):
    model = SalaryComponent
    template_name = 'salary/component_confirm_delete.html'
    success_url = reverse_lazy('component_list')

# Pay Grade Views
class PayGradeListView(LoginRequiredMixin, ListView):
    model = PayGrade
    template_name = 'salary/paygrade_list.html'
    context_object_name = 'paygrades'
    paginate_by = 10

    def get_queryset(self):
        return PayGrade.objects.order_by('name')

class PayGradeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = PayGrade
    form_class = PayGradeForm
    template_name = 'salary/paygrade_form.html'
    success_url = reverse_lazy('paygrade_list')
    success_message = "Pay grade created successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PayGradeComponentFormSet(
                self.request.POST, 
                instance=self.object,
                prefix='form'
            )
        else:
            # Initialize with at least one empty form
            context['formset'] = PayGradeComponentFormSet(
                instance=self.object,
                prefix='form',
                queryset=PayGradeComponent.objects.none() if not self.object else None
            )
            if not self.object and len(context['formset']) < 1:
                context['formset'].extra = 1
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class PayGradeDetailView(LoginRequiredMixin, DetailView):
    model = PayGrade
    template_name = 'salary/paygrade_details.html'
    context_object_name = 'paygrade'

class PayGradeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PayGrade
    form_class = PayGradeForm
    template_name = 'salary/paygrade_form.html'
    success_url = reverse_lazy('paygrade_list')
    success_message = "Pay grade updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PayGradeComponentFormSet(
                self.request.POST, 
                instance=self.object
            )
        else:
            context['formset'] = PayGradeComponentFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class PayGradeDeleteView(LoginRequiredMixin, DeleteView):
    model = PayGrade
    template_name = 'salary/paygrade_confirm_delete.html'
    success_url = reverse_lazy('paygrade_list')