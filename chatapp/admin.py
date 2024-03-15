from django.contrib import admin
from .models import Group, Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id','content', 'timestamp', 'group']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']