from django.urls import path
from . import views

urlpatterns = [
    path('update/', views.update_kpis, name='update_kpis'),
    path('', views.show_dashboard, name='show_dashboard'),
]
