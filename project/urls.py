from django.urls import path
from project import views

urlpatterns = [
    path('',views.home,name='home'),
    path('result/<str:value>',views.botresult,name='botresult'),
]
