from django.urls import path
from .views import create_chatgroup, create_communitygroup, community_chat

urlpatterns = [
    path('creategroup/<int:sender>/<int:receiver>/', create_chatgroup, name="create_chatgroup"),
    path('community_group/', create_communitygroup, name="create_communitygroup"),
    path('community_group_chat/<str:gpname>/', community_chat, name="community_chat"),
]