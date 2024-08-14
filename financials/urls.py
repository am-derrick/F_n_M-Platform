from django.urls import path
from .views import financial_analysis_1, financial_analysis_2

urlpatterns = {
    path('page1/', financial_analysis_1, name='page1'),
    path('page2/', financial_analysis_2, name='page2'),
}