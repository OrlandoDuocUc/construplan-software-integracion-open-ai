from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre-nosotros/', views.about, name='about'),
    path('tutorial/', views.tutorial, name='tutorial'),
]
