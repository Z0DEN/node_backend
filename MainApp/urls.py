from django.urls import path
from . import views, node_auth

app_name = 'MainApp'

urlpatterns = [
    path('AddUser/', views.AddUser, name='AddUser'),
    path('GetUserData/', views.GetUserData, name='GetUserData'),
    path('test/', views.test, name='test'),
    path('UpdateNodeTokens/', node_auth.UpdateNodeTokens),
]
