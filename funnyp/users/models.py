from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

class Profile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    image   = ResizedImageField(size=[125, 125], crop=['top', 'center'], quality=99, upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
