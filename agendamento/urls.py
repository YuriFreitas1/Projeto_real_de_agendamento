"""
URL configuration for agendamento project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from agendamentos import views
from agendamentos.views import criar_agendamento,agendamento_sucesso

urlpatterns = [
    path('admin/', admin.site.urls),
    path('agendar/',criar_agendamento,name='criar_agendamento'),
    path('agendamento_sucesso/', views.agendamento_sucesso, name='agendamento_sucesso'),
    path('gerar_disponibilidades/', views.gerar_disponibilidades, name='gerar_disponibilidades')
]

