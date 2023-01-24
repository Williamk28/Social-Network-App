import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from .validators import AgeValidator
from .helpers import calculate_age
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    dob = models.DateField(validators=[AgeValidator(16)])
    age = models.IntegerField()
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images')
    friends = models.ManyToManyField('CustomUser', blank=True)
    interests = TaggableManager(verbose_name='interests', blank=True)

    REQUIRED_FIELDS = ['email', 'dob']

    def save(self, *args, **kwargs):
        self.age = calculate_age(self.dob)
        return super().save(*args, **kwargs)


class UserPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=50)
    profile = models.CharField(max_length=50)
    message = models.TextField()
    image = models.ImageField(blank=True, upload_to='post_images')
    post_date = models.DateTimeField(auto_now_add=True)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


class LikePost(models.Model):
    post_id = models.ForeignKey(
        UserPost, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class CommentPost(models.Model):
    post = models.ForeignKey(
        UserPost, related_name='comments', on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    message = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        CustomUser, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        CustomUser, related_name='receiver', on_delete=models.CASCADE)


class ChatRoom(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.name


class LiveChatMessage(models.Model):
    username = models.CharField(max_length=50)
    date = models.DateTimeField(default=datetime.now, blank=True)
    message = models.CharField(max_length=5000)
    chatroom = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE)
    staff = models.BooleanField(default=False)
