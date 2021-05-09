from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from django_resized import ResizedImageField

def upload_location(instance, filename):
    return f'posts_pics/{str(instance.author.id)}/{instance.title}-{filename}'

class Category(models.Model):
    name        = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Post(models.Model):
    title       = models.CharField(max_length=100)
    content     = RichTextUploadingField(blank=True, null=True)
    zajawka     = models.TextField(max_length=200, blank=True, null=True, default=' ')
    date_posted = models.DateTimeField(default=timezone.now)
    author      = models.ForeignKey(User, on_delete=models.CASCADE)
    image       = ResizedImageField(size=[1920, 1080], crop=['middle', 'center'], quality=99, upload_to=upload_location)
    likes       = models.ManyToManyField(User, related_name='blog_post', blank=True)
    unlikes     = models.ManyToManyField(User, related_name='blog_post_u', blank=True)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, default='1')

    STATUS_CHOICES = (('Oczekujace','oczekujące'), ('Zaakceptowane', 'zaakceptowane'))
    status      = models.CharField(max_length=25, choices=STATUS_CHOICES, default='oczekujące')
    
    def total_likes(self):
        return self.likes.count()

    def total_unlikes(self):
        return self.unlikes.count()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 600 or img.width > 1200:
            output_size = (1200, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)

@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

class Comment(models.Model):
    post        = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author      = models.ForeignKey(User, on_delete=models.CASCADE)
    body        = models.TextField()
    date_added  = models.DateTimeField(default=timezone.now)
    parent      = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f'{self.post.title} - {self.author} - {self.body}'

    def child(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True