from django.db import models
from django.urls import reverse
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

class MyAbout(models.Model):
    name = models.CharField(max_length=250)
    work = models.CharField(max_length=250)
    body = models.TextField()
    email = models.EmailField()
    phone = models.IntegerField(default='+998 99 410 7441', blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    skils = models.CharField(max_length=100, blank=True, null=True)
    skils_1 = models.CharField(max_length=100, blank=True, null=True)
    skils_2 = models.CharField(max_length=100, blank=True, null=True)
    skils_3 = models.CharField(max_length=100, blank=True, null=True)
    skils_4 = models.CharField(max_length=100, blank=True, null=True)
    skils_5 = models.CharField(max_length=100, blank=True, null=True)
    skils_6 = models.CharField(max_length=100, blank=True, null=True)
    skils_7 = models.CharField(max_length=100, blank=True, null=True)
    skils_8 = models.CharField(max_length=100, blank=True, null=True)
    skils_9 = models.CharField(max_length=100, blank=True, null=True)
    skils_10 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    images = models.ImageField(upload_to='post/images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager() # standart boshqaruvchi
    published = PublishedManager() # ilovaga xos menejer
    tags = TaggableManager()


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])
    
class Contact(models.Model):
    info = models.TextField()
    location = models.CharField(max_length=250)
    facebook = models.URLField()
    instagram = models.URLField()
    telegram = models.URLField()

    def __str__(self):
        return self.location
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta: 
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
    
class Portfolio(models.Model):
    images = models.ImageField(upload_to='portfolio/')
    images_1 = models.ImageField(upload_to='portfolio/')
    images_2 = models.ImageField(upload_to='portfolio/')
    url = models.URLField()
    name = models.CharField(max_length=250)
    info = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 
