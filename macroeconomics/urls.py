from django.urls import path
from .views import home, inflation_trend, upgrade, membership_upgrade

app_name = 'macroeconomics'

urlpatterns = [
    path('', home, name='home'),
    path('inflation_trend/', inflation_trend, name='inflation_trend'),
    path('upgrade/', upgrade, name='upgrade'),
    path('membership_upgrade/', membership_upgrade, name='membership_upgrade'),
]