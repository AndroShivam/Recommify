from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.main_home, name = 'main_home'),
    path('get_response/', views.get_response , name = 'get_response' ),
    path('authenticate_user/', views.authenticate_user, name = 'authenticate_user'),
    path('result/', views.result, name = 'result'),
    # path('/result/get_result/', views.get_result, name = '/result/get_result/')
]