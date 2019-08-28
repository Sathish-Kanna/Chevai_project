try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages

from users.models import Profile
from .models import Chat


@login_required
def message_load(request):
    from_user = request.user
    to_user = request.user
    if request.method == 'GET':
        if 'pk' in request.GET:
            pk = request.GET['pk']
        to_user = (Profile.objects.get(pk=int(pk))).user

    chat_list = Chat.obj.load_message(from_user=from_user, to_user=to_user)
    return render(request, 'chat/chat_content.html', {'chat_list': chat_list})


@login_required
def message_sent(request):
    from_user = request.user
    to_user = request.user
    message = "--empty--"
    if request.method == 'GET':
        if 'message' in request.GET:
            message = request.GET['message']
        if 'pk' in request.GET:
            pk = request.GET['pk']
            to_user = (Profile.objects.get(pk=int(pk))).user

    try:
        print(message)
        Chat.obj.send_message(from_user=from_user, to_user=to_user, message=message)
    except ValidationError:
        message = "Users cannot texted themselves."
        messages.success(request, message)
    chat_list = Chat.obj.load_message(from_user=from_user, to_user=to_user)
    return render(request, 'chat/chat_content.html', {'chat_list': chat_list})


@login_required
def message_received(request, pk):
    Chat.obj.received_message(id=pk)
    return render(request, 'chevai/samp.html')
