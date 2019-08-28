from django.urls import path

from . import views

urlpatterns = [
    path('chat_box/', views.message_sent, name='message_sent'),
    path('chat_content/', views.message_load, name='message_load'),
    path('chat_received/<int:pk>', views.message_received, name='message_received'),
]
