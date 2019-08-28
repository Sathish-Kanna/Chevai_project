from django.urls import path

from . import views as user_view

urlpatterns = [
    path('requested/<int:pk>', user_view.request_send, name='request_sent'),
    path('accept/<int:pk>', user_view.request_accept, name='request_accept'),
    path('reject/<int:pk>', user_view.request_reject, name='request_reject'),
    path('cancel/<int:pk>', user_view.request_cancel, name='request_cancel'),
    path('conform/<int:pk>', user_view.service_accept, name='service_accept'),
    path('decline/<int:pk>', user_view.service_reject, name='service_reject'),
]
