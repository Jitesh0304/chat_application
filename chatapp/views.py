from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Chat, Group
from django.views.decorators.csrf import csrf_protect
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required



# @csrf_protect
# def create_chatgroup(request):
#     all_group = Group.objects.all()
#     if request.method=="POST" and 'group_name' in request.POST:
#         group_name = request.POST.get('group_name')

#         if not all_group.filter(name=group_name).exists():
#             new_group = Group(name = group_name)
#             new_group.save()
#         return HttpResponseRedirect('/')
#     return render(request, 'home.html', {'all_groups':all_group})



@login_required
def create_chatgroup(request, sender, receiver):
    chats = []
    # user_ids = combined_ids.split(',')
    # user1_id = int(user_ids[0])
    # user2_id = int(user_ids[1])

    all_groups = Group.objects.all()
    if all_groups.filter(name= f"{sender}_{receiver}").exists():
        combined_ids = f"{sender}_{receiver}"
        group = Group.objects.get(name= combined_ids)
        chats = Chat.objects.filter(group= group)
    elif all_groups.filter(name= f"{receiver}_{sender}").exists():
        combined_ids = f"{receiver}_{sender}"
        group = Group.objects.get(name= combined_ids)
        chats = Chat.objects.filter(group= group)
    else:
        combined_ids = f"{sender}_{receiver}"
        new_group = Group(name = combined_ids)
        group = new_group.save()
    return render(request, 'chatpage.html', {'GroupName':combined_ids, 'chats':chats})

