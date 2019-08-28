from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from request.exceptions import AlreadyExistsError
from request.models import Request
from .models import Feedback


@login_required
def feedback_send(request, pk):
    if request.method == 'GET':
        obj = Request.objects.get(pk=pk)
        if 'feedback' in request.GET and 'rated' in request.GET:
            data = request.GET['feedback']
            rating = int(request.GET['rated'])
            feed = {
                'data': data,
                'rating': rating,
            }
            try:
                Feedback.obj.send_feedback(obj, feed, pk)
            except AlreadyExistsError:
                message = 'Feedback already given'
            else:
                message = 'Feedback successfully given'
            messages.success(request, message)
            return redirect('chevai_home')
    return render(request, 'feedback/feedback.html')
