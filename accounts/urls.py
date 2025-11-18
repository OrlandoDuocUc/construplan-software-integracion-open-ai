from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('registro/', views.SignUpView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('perfil/', views.ProfileView.as_view(), name='profile'),
    path('recuperar/', views.ForgotPasswordView.as_view(), name='forgot_password'),
]
