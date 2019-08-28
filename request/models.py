from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from users.models import Service, User
from .exceptions import AlreadyExistsError


class RequestManagement:
    def can_request_send(self, from_user, to_user):
        if from_user == to_user:
            return False

        if not Request.objects.filter(
                from_user=from_user, to_service=to_user, status='waiting'
        ).exists():
            return False
        return True

    def send_request(self, from_user, to_service, date):
        if from_user == to_service.user.user:
            raise ValidationError("Users cannot request for themselves.")

        if self.can_request_send(from_user, to_service):
            raise AlreadyExistsError("Already requested")

        request, created = Request.objects.get_or_create(
            from_user=from_user, to_service=to_service, status='waiting', service_date=date['date'],
            service_time=date['time']
        )

        if created is False:
            raise AlreadyExistsError("Already requested")

        message = str(from_user.profile.name)+' requests for \''+str(to_service.skill)+'\' service.'
        request.message = message
        request.status = 'waiting'
        request.save()
        return request

    def accept_request(self, id):
        request = Request.objects.get(id=id)

        request.status = 'accepted'
        request.save()
        return request

    def reject_request(self, id):
        request = Request.objects.get(id=id)

        request.status = 'rejected'
        request.save()
        return request

    def cancel_request(self, id):
        request = Request.objects.get(id=id)

        request.status = 'canceled'
        request.save()
        return request

    def accept_service(self, id):
        request = Request.objects.get(id=id)

        request.status = 'conformed'
        request.save()

        service = Service.objects.get(id=request.to_service.pk)
        service.job_done += 1
        service.save()
        return request

    def reject_service(self, id):
        request = Request.objects.get(id=id)

        request.status = 'declined'
        request.save()
        return request


class Request(models.Model):
    requested = models.DateTimeField(default=timezone.now)
    service_date = models.DateField(blank=True)
    service_time = models.TimeField(blank=True)
    message = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, blank=True)

    to_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)

    obj = RequestManagement()

    def __str__(self):
        return str(self.from_user)+' requests for \''+str(self.to_service.skill)+'\' service by \''+str(self.to_service.user.name)+'\''

    def save(self, *args, **kwargs):
        if self.to_service == self.from_user:
            raise ValidationError("Users cannot request for themselves.")
        super(Request, self).save(*args, **kwargs)
