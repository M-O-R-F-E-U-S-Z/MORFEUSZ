from .forms import CreateGroupForm, AddGroupMember
from .models import Group
from django.shortcuts import render, redirect
from users.models import FriendList
from django.contrib.auth.models import User
from django.http import HttpResponse


# def home(request):
#     return render(request, 'morfeusz_app/home.html', {'title': 'Home Page'})


def home(request):
    user = request.user
    context = {}
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            group = Group.objects.create(name=name)
            group.add_member(user)
            # form.save()
            return redirect('morfeusz_app-home')
    else:
        form = CreateGroupForm()
    context['form'] = form

    my_groups = []
    groups = Group.objects.all()
    for group in groups:
        if user in group.members.all():
            my_groups.append(group)
    context['my_groups'] = my_groups
    return render(request, 'morfeusz_app/home.html', context)


def manage_group(request, group_id):
    context = {}
    group = Group.objects.get(id=group_id)
    context['group_name'] = group.name
    user = request.user
    if request.method == "POST":
        # form = AddGroupMember(request.POST)
        # print('sadasdasdsadasdasd')
        # print(request.POST)
        # print(request.POST['friend'])
        member_to_add = User.objects.get(id=request.POST['friend'])
        group.add_member(member_to_add)
        return redirect('morfeusz_app-home')
        # print(request)
        # print(form.cleaned_data.get("friend"))
        # if form.is_valid():
        #     # form.save()
        #     # group.add_member(form.cleaned_data.get("friend"))
        #     return redirect('morfeusz_app-home')
        # else:
        #     return HttpResponse("form is not valid")
    else:
        friends = FriendList.objects.get(user=user)
        friend_list = []
        for index, my_friend in enumerate(friends.friends.all(), start=1):
            friend_list.append((my_friend, my_friend.username))
        form = AddGroupMember(friend_list)

    context['form'] = form
    return render(request, 'morfeusz_app/manage_group.html', context)