from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
# Create your models here.
def localtime():
    return timezone.localtime(timezone.now())

class Book(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    uid = models.CharField(default=uuid.uuid4, max_length=50)
    sold = models.BooleanField(default=False)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='buyer', null=True)
    name = models.CharField(max_length=30, blank=False, null=True)
    price = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    isbn = models.CharField(max_length=30, blank=True)
    pre_tags = models.TextField(blank=True, null=True)
    post_tags = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    dimensions = models.TextField(blank=True, null=True)
    publishing_date = models.DateTimeField(default=localtime)
    post_date = models.DateTimeField(default=localtime)
    update_date = models.DateTimeField(default=localtime)

class ImageBook(models.Model):
    caption = models.CharField(max_length=255, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    default = models.BooleanField(default=False)

class Listing(models.Model):
    isbn = models.CharField(max_length=30, blank=False)
    number = models.CharField(max_length=10, blank=False)
    description = models.TextField(blank=False)

class ComboBook(models.Model):
    group = models.CharField(max_length=50, blank=False)

class ReportedBooks(models.Model):
    seller = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reportedseller')
    reporter = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reporter')
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='book')