from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='chevai_home'),
    path('<int:pk>/Profile/<str:name>', views.profile_details, name='profile_details'),
    path('<int:pk>/Service/<str:name>', views.service_details, name='service_details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
