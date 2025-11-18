from django.urls import path

from . import views

app_name = 'models_core'

urlpatterns = [
    path('', views.ModelListView.as_view(), name='model_list'),
    path('nuevo/', views.ModelCreateView.as_view(), name='model_create'),
    path('<int:pk>/', views.ModelDetailView.as_view(), name='model_detail'),
    path('<int:pk>/eliminar/', views.ModelDeleteView.as_view(), name='model_delete'),
]
