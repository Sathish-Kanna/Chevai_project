try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages

from users.models import Service
from .models import Request
from .exceptions import AlreadyExistsError


@login_required
def request_send(request, pk):
    to_service = Service.objects.get(pk=pk)
    from_user = request.user
    date = {}
    if request.method == 'GET':
        if 'date' in request.GET and 'time' in request.GET:
            date = {
                'date': request.GET['date'],
                'time': request.GET['time']
            }
    try:
        Request.obj.send_request(from_user=from_user, to_service=to_service, date=date)
    except AlreadyExistsError:
        message = "Already requested"
    except ValidationError:
        message = "Users cannot request for themselves."
    else:
        message = str(from_user.profile.name)+' requests for \''+str(to_service.skill)+'\' service.'
    messages.success(request, message)
    return redirect('chevai_home')


@login_required
def request_accept(request, pk):
    Request.obj.accept_request(id=pk)
    return redirect('chevai_home')


@login_required
def request_reject(request, pk):
    Request.obj.reject_request(id=pk)
    return redirect('chevai_home')


@login_required
def request_cancel(request, pk):
    Request.obj.cancel_request(id=pk)
    return redirect('chevai_home')


@login_required
def service_accept(request, pk):
    Request.obj.accept_service(id=pk)
    return redirect('chevai_home')


@login_required
def service_reject(request, pk):
    Request.obj.reject_service(id=pk)
    return redirect('chevai_home')

