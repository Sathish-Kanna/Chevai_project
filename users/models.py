from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from PIL import Image
from PIL import ImageFile


ImageFile.LOAD_TRUNCATED_IMAGES = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    location = models.TextField(max_length=500, blank=True)
    pin_regex = RegexValidator(regex=r'\d{5,7}$',
                               message='Pin number must be entered in the format: "605001"')
    pin = models.CharField(validators=[pin_regex], max_length=7, blank=True)
    language = models.CharField(max_length=100, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?\d{10,12}$',
                                 message='Phone number must be entered in the format: "+919876543210"')
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    image = models.ImageField(default='default.png', upload_to='profile_pic')

    def __str__(self):
        return str(self.user.username)+' Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        print('Profile saved in model')

        if img.height > 250 or img.width > 250:
            output_size = (250, 250)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Service(models.Model):
    skill = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(default=0)
    job_done = models.IntegerField(default=0)

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skill_key = models.CharField(unique=True, max_length=160, blank=True)

    def __str__(self):
        return str(self.skill)+' service by \''+str(self.user.name)+'\''

    def save(self, *args, **kwargs):
        super(Service, self).save(*args, **kwargs)


