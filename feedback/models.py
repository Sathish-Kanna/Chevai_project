from django.db import models

from request.exceptions import AlreadyExistsError
from users.models import Service
from request.models import Request


class FeedbackManagement:
    def can_feedback_send(self, detail):
        if not Feedback.objects.filter(detail=detail).exists():
            return False
        return True

    def send_feedback(self, detail, feed, id):
        if self.can_feedback_send(detail):
            raise AlreadyExistsError("Feedback given")

        request, created = Feedback.objects.get_or_create(detail=detail)

        if created is False:
            raise AlreadyExistsError("Feedback given")

        request.feedback = feed['data']
        request.rating = feed['rating']
        request.save()

        service = Service.objects.get(id=request.detail.to_service.pk)
        rating = service.rating
        job_done = service.job_done-1
        service.rating = (rating*job_done + feed['rating']) / (job_done+1)
        service.save()

        request = Request.objects.get(id=id)

        request.status = 'done'
        request.save()

        return request


class Feedback(models.Model):
    feedback = models.CharField(max_length=200, blank=True)
    rating = models.IntegerField(blank=True, null=True)

    detail = models.OneToOneField(Request, on_delete=models.CASCADE)

    obj = FeedbackManagement()

    def __str__(self):
        return 'feedback for '+str(self.detail.to_service)+' for \''+str(self.detail.from_user)+'\''

    def save(self, *args, **kwargs):
        super(Feedback, self).save(*args, **kwargs)