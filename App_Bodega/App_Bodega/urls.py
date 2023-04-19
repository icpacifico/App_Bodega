"""
URL configuration for App_Bodega project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from usuario.views import Login, Inicio, logoutUsuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vale_consumo/', include(('vale_consumo.urls', 'vale_consumo'))),
    path('', login_required(Inicio.as_view()),name='index'),
    # path('inicio', login_required(Inicio.as_view()), name="index"),
    path('accounts/login/', Login.as_view(), name='login'),
    path('logout/', login_required(logoutUsuario), name='logout'),
]