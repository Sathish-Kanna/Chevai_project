from django.urls import path
from django.contrib.auth import views as auth_view

from . import views as user_view

urlpatterns = [
    path('register/', user_view.register, name='user_register'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name='user_login'),
    path('logout/', user_view.logout_view, name='user_logout'),

    path('profile/', user_view.profile_view, name='user_profile'),
    path('profile-update/', user_view.profile_update, name='update_profile'),

    path('service-create/', user_view.service_profile_create, name='create_service'),
    path('service-view/', user_view.service_profile_view, name='view_service'),
    path('<int:pk>/service-update/<str:name>', user_view.service_profile_update, name='update_service'),

    path('notification/', user_view.update_notification, name='update_notification')
]
