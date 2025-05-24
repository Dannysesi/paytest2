from django.urls import path
from . import views

# app_name = 'company'

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.dashboard, name='dashboard'),
    path('list/', views.CompanyListView.as_view(), name='list'),
    path('create/', views.CompanyCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.CompanyUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='delete'),
]