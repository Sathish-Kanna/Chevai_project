from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import DetailView
from django.http import JsonResponse

from .form import UserRegisterForm, ProfileUpdateForm, UserServiceForm
from .models import Service
from chevai.operation import get_notification


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            user = form.save()
            user.refresh_from_db()
            user.profile.name = form.cleaned_data.get('name')
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.save()

            username = form.cleaned_data.get('username')
            messages.success(request, 'Account has been created for ' + username + '! You can login')
            return redirect('user_login')
    else:
        form = UserRegisterForm()

    form_dict = {'form': form}
    return render(request, 'users/register.html', form_dict)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You are logged out')
    return redirect('user_login')


class ServiceView(DetailView):
    model = Service
    template_name = 'users/service_detail.html'


@login_required
def profile_view(request):
    return render(request, 'users/view_profile.html')


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('name')
            messages.success(request, 'Hi '+username+', Your profile is updated!')
            return redirect('user_profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'form': form
    }
    return render(request, 'users/update.html', context)


@login_required
def service_profile_create(request):
    if request.method == 'POST':
        obj = Service(user=request.user.profile)
        form = UserServiceForm(request.POST, instance=obj)

        if form.is_valid():
            form.instance.skill_key = str(request.user.profile.user)+'_:_'+form.cleaned_data.get('skill')
            form.save()
            username = request.user.profile.name
            messages.success(request, 'Hi '+username+', your service profile is updated!')
            return redirect('view_service')
    else:
        form = UserServiceForm()

    context = {
        'form': form
    }
    return render(request, 'users/update.html', context)


@login_required
def service_profile_view(request):
    profile = request.user.profile
    services = list(Service.objects.filter(user=request.user.profile))
    context = {
        'profile': profile,
        'services': services,
    }

    return render(request, 'users/view_service_profile.html', context)


@login_required
def service_profile_update(request, pk, name):
    if request.method == 'POST':
        obj = Service.objects.get(pk=pk)
        form = UserServiceForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            username = request.user.profile.name
            messages.success(request, 'Hi '+username+', Your service profile is updated!')
            return redirect('view_service')
    else:
        obj = Service.objects.get(pk=pk)
        form = UserServiceForm(instance=obj)

    context = {
        'form': form
    }
    return render(request, 'users/update.html', context)


@login_required
def update_notification(request):
    notification = get_notification(request.user)
    return render(request, 'users/notification.html', {'notification': notification})
