from django.urls import path
from .views import home, signup, CustomLogoutView, CustomLoginView

urlpatterns = [
    path('home/', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]