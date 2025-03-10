from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_images, name='generate_images'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
