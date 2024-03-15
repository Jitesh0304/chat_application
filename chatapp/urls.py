from django.urls import path
from .views import create_chatgroup

urlpatterns = [
    path('creategroup/<int:sender>/<int:receiver>/', create_chatgroup, name="create_chatgroup")
]