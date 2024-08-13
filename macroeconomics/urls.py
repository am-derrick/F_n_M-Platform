from django.urls import path
from .views import home, inflation_trend, upgrade

app_name = 'macroeconomics'

urlpatterns = [
    path('', home, name='home'),
    path('inflation_trend/', inflation_trend, name='inflation_trend'),
    path('upgrade/', upgrade, name='upgrade'),
]