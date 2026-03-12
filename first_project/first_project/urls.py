"""
URL configuration for first_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from app.views import (
    index,
    get_omlet,
    get_pasta,
    catalog,
    phone,
    SensorListCreateView,
    SensorRetrieveUpdateView,
    MeasurementCreateView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('omlet/', get_omlet),
    path('pasta/', get_pasta),
    path('catalog/', catalog, name='catalog'),
    path('catalog/<slug:slug>/', phone, name='phone'),

     # REST API для датчиков
    path('api/sensors/', SensorListCreateView.as_view()),
    path('api/sensors/<int:pk>/', SensorRetrieveUpdateView.as_view()),
    path('api/measurements/', MeasurementCreateView.as_view()),
]
