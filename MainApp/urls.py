from django.urls import path
from . import views, node_auth

app_name = 'MainApp'

urlpatterns = [
    path('AddUser/', views.AddUser, name='AddUser'),
    path('GetUserData/', views.GetUserData, name='GetUserData'),
    path('CreateFolder/', views.CreateFolder, name='CreateFolder'),
    path('SaveFiles/', views.SaveFiles, name='SaveFiles'),
    path('UpdateNodeTokens/', node_auth.UpdateNodeTokens),
]
