from django.urls import path
from . import views

# app_name = 'salary'

urlpatterns = [
    # Salary Component URLs
    path('components/', views.SalaryComponentListView.as_view(), name='component_list'),
    path('components/create/', views.SalaryComponentCreateView.as_view(), name='component_create'),
    path('components/<int:pk>/update/', views.SalaryComponentUpdateView.as_view(), name='component_update'),
    path('components/<int:pk>/delete/', views.SalaryComponentDeleteView.as_view(), name='component_delete'),
    
    # Pay Grade URLs
    path('paygrades/', views.PayGradeListView.as_view(), name='paygrade_list'),
    path('paygrades/create/', views.PayGradeCreateView.as_view(), name='paygrade_create'),
    path('paygrades/<int:pk>/', views.PayGradeDetailView.as_view(), name='paygrade_detail'),
    path('paygrades/<int:pk>/update/', views.PayGradeUpdateView.as_view(), name='paygrade_update'),
    path('paygrades/<int:pk>/delete/', views.PayGradeDeleteView.as_view(), name='paygrade_delete'),
]