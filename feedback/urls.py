from django.urls import path

from . import views

urlpatterns = [
    path('feedback/<int:pk>', views.feedback_send, name='feedback_send'),
]
