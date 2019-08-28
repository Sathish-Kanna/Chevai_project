from django.shortcuts import render

from users.models import Service, Profile
from feedback.models import Feedback
from request.models import Request
from .operation import in_search_fun, get_notification


def home(request):
    val = ''
    if request.method == 'GET':
        if 'query' in request.GET and 'category' in request.GET:

            query = request.GET['query']
            category = request.GET['category']
            q_words = query.split()
            val = {'query': query, 'category': category}

            result = in_search_fun(Service, q_words, category)
        else:
            result = list(Service.objects.all())
    else:
        result = []

    context = {
        'contents': result,
        'name': val,
    }

    return render(request, 'chevai/home.html', context)


def profile_details(request, pk, name):
    profile = Profile.objects.get(pk=pk)
    services = list(Service.objects.filter(user=profile))
    context = {
        'profile': profile,
        'services': services,
    }
    return render(request, 'chevai/profile_detail.html', context)


def service_details(request, pk, name):
    feedback = []
    service = Service.objects.get(pk=pk)
    reqsts = list(Request.objects.filter(to_service=service))
    for reqst in reqsts:
        for feed in list(Feedback.objects.filter(detail=reqst)):
            t = {}
            t['profile'] = list(Profile.objects.filter(user=feed.detail.from_user))[0]
            t['feed'] = feed
            feedback.append(t)
    context = {
        'object': service,
        'feedback': feedback,
    }
    return render(request, 'chevai/service_detail.html', context)
