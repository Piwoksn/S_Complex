from django.shortcuts import render
from myapp.models import User
from .models import SentChats
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.


# @csrf_exempt
@login_required(login_url='superadminlogin')
def createchat(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            people = email.split()
            message = request.POST['chat']
            for p in people:
                chat = SentChats.objects.create(user=request.user,
                                                receiver=p, sentmessages=message)
            messages.success(request, f'Sent to {people}')
            return HttpResponseRedirect(request.path_info)
    except:
        messages.success(request, f'Not Sent')
        return HttpResponseRedirect(request.path_info)
    return render(request, "chats/superadminchat.html")


@login_required(login_url='superadminlogin')
def superadminmessages(request):
    user = request.user
    # chats = SentChats.objects.all()
    chats = SentChats.objects.filter(user=request.user)
    chat = chats.values('receiver').distinct()
    context = {'chats': chat, 'user': user, }
    return render(request, "chats/superadminmessages.html", context)


@login_required(login_url='superadminlogin')
def superadminchatroom(request, email):
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        return HttpResponse("User not found", status=404)

    sender_chats = SentChats.objects.filter(user=request.user, receiver=user)
    receiver_chats = SentChats.objects.filter(user=user, receiver=request.user)

    # Merge sender and receiver chats and order them by timestamp
    all_chats = list(sender_chats) + list(receiver_chats)
    all_chats.sort(key=lambda x: x.timesent)

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            SentChats.objects.create(
                user=request.user, sentmessages=message, receiver=user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {'all_chats': all_chats, 'user': request.user}
    return render(request, 'chats/chat.html', context)


@login_required(login_url='superadminlogin')
def superadminchatdelete(request, email):
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        return HttpResponse("User not found", status=404)

    sender_chats = SentChats.objects.filter(user=request.user, receiver=user)
    receiver_chats = SentChats.objects.filter(user=user, receiver=request.user)
    #
    for sender in sender_chats:
        sender.delete()
    for receiver in receiver_chats:
        receiver.delete()
    messages.success(request, "Chat deleted")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'chats/superadminmessages.html')


# User Chat
@login_required(login_url='loginform')
def userchat(request, email):
    # chat = SentChats.objects.get(user=admin@admin.com)
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        return HttpResponse("User not found", status=404)

    #
    sender_chats = SentChats.objects.filter(user=request.user, receiver=user)
    receiver_chats = SentChats.objects.filter(user=user, receiver=request.user)

    # Merge sender and receiver chats and order them by timestamp
    all_chats = list(sender_chats) + list(receiver_chats)
    all_chats.sort(key=lambda x: x.timesent)

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            SentChats.objects.create(
                user=request.user, sentmessages=message, receiver=user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {'all_chats': all_chats, 'user': request.user}
    #
    return render(request, 'chats/userchat.html', context)
