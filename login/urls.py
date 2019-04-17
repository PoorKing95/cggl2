from django.urls import path

from . import views

app_name = 'login'
urlpatterns = [
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('check', views.check, name='check'),
    path('regist',views.regist, name='regist'),
    path('passway',views.passway, name='passway'),
    path('tables',views.tables, name='tables'),
    path('logout/', views.logout, name='logout')
]