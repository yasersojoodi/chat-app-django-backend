from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('users/', views.Persons),
    path('users/<str:id>/', views.Person),
    path('send-message/<str:sender>/<str:receiver>/', views.send_message),
    path('edit-message/<int:id>/', views.edit_message),
    path('delete-message/<str:id>/', views.delete_message),
    path('conversation-online/<str:id>/', views.online_conversation_status),
    path('conversation-offline/<str:id>/', views.offline_conversation_status),
    path('user-online/<str:id>/', views.online_person_status),
    path('user-offline/<str:id>/', views.offline_person_status),
    path('offline-all/<str:id>/', views.offline_all),

]
