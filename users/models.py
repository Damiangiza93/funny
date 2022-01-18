from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_resized import ResizedImageField



def upload_bg_location(instance, filename):
    return f'backgrounds/{filename}'
class Background(models.Model):
    name    = models.CharField(max_length=100)
    image   = ResizedImageField(size=[960, 540], crop=['middle', 'center'], quality=99, upload_to=upload_bg_location)

    def __str__(self):
        return f'{self.pk} {self.name}'

@receiver(post_delete, sender=Background)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def upload_location(instance, filename):
    return f'profile_pics/{str(instance.user.username)}/{filename}'
class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    image       = ResizedImageField(size=[125, 125], crop=['top', 'center'], quality=99, upload_to=upload_location, default="default.jpg")
    background  = models.ForeignKey(Background, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

@receiver(post_delete, sender=Profile)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

