from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.SET_NULL, null=True)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.SET_NULL, null=True)
    views = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.subject

class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL)
    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

# wedding shop starts here

class WishList(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Gift(models.Model):
    name = models.CharField(max_length=30, unique=True)
    message = models.TextField(max_length=4000)
    wishList = models.ForeignKey(WishList, related_name='gift', on_delete=models.CASCADE)
    picture = models.CharField(max_length=30, default='img/anka.jpg')
    cost = models.PositiveIntegerField(default = 0)
    costLeft = models.PositiveIntegerField(default = 99999)
    costPayed = models.PositiveIntegerField(default = 0)
    latestPayed = models.PositiveIntegerField(default = 0)
    numberWanted = models.PositiveIntegerField(default = 1)
    numberBought = models.PositiveIntegerField(default = 0)
    bought = models.BooleanField()
    boughtBy_1 = models.TextField(max_length=4000, default='', blank=True)
    boughtBy_2 = models.TextField(max_length=4000, default='', blank=True)
    boughtBy_3 = models.TextField(max_length=4000, default='', blank=True)
    boughtBy_4 = models.TextField(max_length=4000, default='', blank=True)
    boughtBy_5 = models.TextField(max_length=4000, default='', blank=True)
    def __str__(self):
        return self.name
    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))