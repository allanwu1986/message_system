from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from messages.models import Inbox, CachedMessage, UserMessage

def user_login(request):
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/user/'+username+'/')
        return render(request, 'login.html', {'tried_validation': True})
    return render(request, 'login.html', {'tried_validation': False})

def user_logout(request):
    logout(request)
    return render(request, 'logout.html', {})

def user_page(request, name):
    try:
        u = User.objects.get(username=name)
        if not u.is_active:
            raise User.DoesNotExist('User is inactivated.')
        inbox = None
        try:
            inbox = Inbox.objects.get(owner=u)
        except Inbox.DoesNotExist:
            inbox = Inbox.objects.create(owner=u)
            inbox.save()
        all_messages = inbox.messages.all()
        messages = []
        for m in all_messages:
            try:
                cached_message = CachedMessage.objects.get(id=m.message)
                messages.append({'writer': cached_message.writer.username, 'message': cached_message.message, 'read': m.read, 'exists': True})
            except CachedMessage.DoesNotExist:
                messages.append({'exists': False})
        return render(request, 'user.html', {'username': name, 'current_user': request.user.username, 'messages': messages})
    except User.DoesNotExist:
        raise Http404

def send_message(request, username):
    if request.user.username != username:
        raise Http404
    else:
        users = []
#        user_count = 0
        if 'message_type' in request.POST and 'message' in request.POST:
            message_type = request.POST['message_type']
            message = request.POST['message']
            if len(message) > 1024:
                return render(request, 'message.html', {'username': request.user.username})
            if message_type == 'single':
                if 'users' in request.POST:
                    usernames = request.POST['users'].strip().split(',')
                    nonexistent_users = []
                    for u in usernames:
                        try:
                            users.append(User.objects.get(username=u))
                        except User.DoesNotExist:
                            nonexistent_users.append(u)
                    render(request, 'message.html', {'username': request.user.username, 'nonexistent_users': nonexistent_users})
            if message_type == 'group':
                if 'group' in request.POST:
                    users = set([])
                    groupnames = request.POST['group'].strip().split(',')
                    nonexistent_groups = []
                    for g in groupnames:
                        try:
                            for u in Group.objects.get(name=g).user_set.all():
                                users.add(u)
                        except Group.DoesNotExist:
                            nonexistent_groups.append(g)
                    render(request, 'message.html', {'username': request.user.username, 'nonexistent_groups': nonexistent_groups})
            if message_type == 'broadcast':
                users = User.objects.all()
            m = CachedMessage.objects.create(writer=request.user, message=message)
            m.save()
            for u in users:
                if u.is_active:
                    inbox = None
                    try:
                        inbox = Inbox.objects.get(owner=u)
                    except Inbox.DoesNotExist:
                        inbox = Inbox.objects.create(owner=u)
                        inbox.save()
                    usermessage = UserMessage(read=False,message=m.id)
                    usermessage.save()
                    inbox.messages.add(usermessage)
#                    user_count += 1
        return render(request, 'message.html', {'username': request.user.username, 'users_sent': users})
