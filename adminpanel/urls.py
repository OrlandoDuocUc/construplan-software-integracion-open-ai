from django.urls import path

from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('usuarios/', views.UserListView.as_view(), name='user_list'),
    path('usuarios/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('usuarios/<int:pk>/modelos/', views.UserModelsView.as_view(), name='user_models'),
    path('usuarios/<int:pk>/eliminar/', views.UserDeleteView.as_view(), name='user_delete'),
]
