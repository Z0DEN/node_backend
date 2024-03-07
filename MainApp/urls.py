from django.urls import path
from . import views, node_auth
from django.conf import settings
from django.conf.urls.static import static


app_name = 'MainApp'

urlpatterns = [
    path('AddUser/', views.AddUser, name='AddUser'),
    path('GetUserData/', views.GetUserData, name='GetUserData'),
    path('CreateFolder/', views.CreateFolder, name='CreateFolder'),
    path('DeleteItem/', views.DeleteItem, name='DeleteItem'),
    path('UploadFiles/', views.UploadFiles, name='UploadFiles'),
    path('DownloadFiles/', views.DownloadFiles, name='DownloadFiles'),
    path('UpdateNodeTokens/', node_auth.UpdateNodeTokens),
] 
#+ static('media/', document_root='/storage/')
