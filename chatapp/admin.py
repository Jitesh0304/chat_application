from django.contrib import admin
from .models import Group, Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id','content', 'timestamp', 'group']



@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'display_members']

    def display_members(self, obj):
        # id_list = []
        # for onedata in obj.submit_timesheet.all():
        #     id_list.append(onedata.id)
        return list(obj.members.values_list('id', flat=True))
    
    display_members.short_description = 'Members IDs'