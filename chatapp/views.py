from django.shortcuts import render
from .models import Chat, Group
from .forms import GroupForm
# from django.views.decorators.csrf import csrf_protect
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from registration.models import User



@login_required
def create_communitygroup(request):
    fm = GroupForm()
    if request.method=="POST":
        gp_form = GroupForm(request.POST, requested_user=request.user)
        name = None
        if gp_form.is_valid():
            # print(gp_form.cleaned_data)
            name = gp_form.cleaned_data['name']
            allmembers = gp_form.cleaned_data['members']
            gp_form.save()
            # allmembers_ids = list(allmembers.values_list('id', flat=True))
            # new_data.members.set(allmembers_ids)
        return render(request, 'group_greeting.html', {'GroupName':name, 'FORM':fm})
    return render(request, 'group_greeting.html', {'FORM':fm})



@login_required
def create_chatgroup(request, sender, receiver):
    chats = []
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
        userOne = request.user
        userTwo = User.objects.get(id=receiver)
        new_group = Group.objects.create(name = combined_ids)
        group = new_group.members.set([userOne, userTwo])
    return render(request, 'chatpage.html', {'GroupName':combined_ids, 'chats':chats, 'currentUser ':request.user})



@login_required
def community_chat(request, gpname):
    chats = []
    group = Group.objects.get(name= gpname)
    chats = Chat.objects.filter(group= group)
    return render(request, 'chatpage.html', {'GroupName':gpname, 'chats':chats, 'currentUser ':request.user})

