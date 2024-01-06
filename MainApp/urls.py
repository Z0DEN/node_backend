from django.urls import path
from . import views, nodes

app_name = 'MainApp'

urlpatterns = [
    path('AddUser/', views.AddUser, name='AddUser'),
    path('test/', views.test, name='test'),
    path('UpdateNodeTokens/', node.test),
]

