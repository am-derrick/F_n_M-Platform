from django.urls import path
from . import views

app_name = 'macroeconomics'

urlpatterns = [
    path('', views.home, name='home')
]