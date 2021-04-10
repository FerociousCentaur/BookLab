from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from Books.models import Book

def localtime():
    return timezone.localtime(timezone.now())

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class BannedProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    all_reports = models.TextField()
    warned_for = models.OneToOneField(Book, on_delete=models.CASCADE, blank=True, related_name='warned_for')
    warned = models.BooleanField(default=False)
    warned_by = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='warned_by')
    warn_description = models.TextField(blank=True)
    warn_date = models.DateTimeField(default=localtime)
    banned = models.BooleanField(default=False)
    banned_for = models.OneToOneField(Book, on_delete=models.CASCADE, blank=True, related_name='banned_for')
    banned_by = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name='banned_by')
    ban_description = models.TextField(blank=True)
    ban_date = models.DateTimeField(default=localtime)

    def __str__(self):
        return self.user.username



