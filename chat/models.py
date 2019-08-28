from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from users.models import User


class ChatManagement:
    def load_message(self, from_user, to_user):
        if from_user.profile.pk < to_user.profile.pk:
            chatters = from_user.profile.name+'-'+to_user.profile.name
        else:
            chatters = to_user.profile.name + '-' + from_user.profile.name
        chat_list = list(Chat.objects.filter(chatters__icontains=chatters))
        return chat_list

    def send_message(self, from_user, to_user, message):
        if from_user == to_user:
            raise ValidationError("Users cannot chat themselves.")

        chat, created = Chat.objects.get_or_create(
            from_user=from_user, to_user=to_user, status='1'
        )

        chat.message = message
        chat.status = 'waiting'
        if from_user.profile.pk < to_user.profile.pk:
            chat.chatters = from_user.profile.name+'-'+to_user.profile.name
        else:
            chat.chatters = to_user.profile.name + '-' + from_user.profile.name
        chat.save()
        return chat

    def received_message(self, id):
        msg = Chat.objects.get(id=id)

        msg.status = 'delivered'
        msg.save()
        return msg


class Chat(models.Model):
    time = models.DateTimeField(default=timezone.now)
    message = models.CharField(max_length=5000, blank=True)
    status = models.CharField(max_length=20, blank=True)
    chatters = models.CharField(max_length=100, blank=True)

    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')

    obj = ChatManagement()

    def __str__(self):
        return str(self.from_user)+' texted to \''+str(self.to_user)+'\''

    def save(self, *args, **kwargs):
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot request for themselves.")
        super(Chat, self).save(*args, **kwargs)