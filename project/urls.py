from django.contrib import admin
from django.urls import path,include
from registration import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepg'),
    path('reg/', include('registration.urls')),
    path('chat/', include('chatapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

