from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
    path('modelo/<int:pk>/pdf/', views.ResultPDFView.as_view(), name='result_pdf'),
]
