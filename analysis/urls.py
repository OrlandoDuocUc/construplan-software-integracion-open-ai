from django.urls import path

from . import views

app_name = 'analysis'

urlpatterns = [
    path('procesar/<int:pk>/', views.ProcessModelView.as_view(), name='process_model'),
    path('detalle/<int:pk>/', views.AnalysisDetailView.as_view(), name='analysis_detail'),
    path('test-ai/', views.test_ai, name='test_ai'),
]
