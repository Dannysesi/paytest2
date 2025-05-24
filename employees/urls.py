from django.urls import path
from . import views

# app_name = 'employees'

urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employees_list'),
    path('create/', views.EmployeeCreateView.as_view(), name='employees_create'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employees_detail'),
    path('<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employees_update'),
    path('<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employees_delete'),
    path('get-paygrade-components/', views.get_paygrade_components, name='get_paygrade_components'),
]